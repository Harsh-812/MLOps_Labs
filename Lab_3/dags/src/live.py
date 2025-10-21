import os, json, base64, pickle, warnings
from typing import Dict, Any, List

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from kneed import KneeLocator

warnings.filterwarnings("ignore", category=FutureWarning)

WD = "/opt/airflow/working_data"
os.makedirs(WD, exist_ok=True)

def _b64(obj) -> str:
    return base64.b64encode(pickle.dumps(obj)).decode("ascii")

def _unb64(s: str):
    return pickle.loads(base64.b64decode(s))


def load_data() -> str:
    here = os.path.dirname(__file__)                   
    csv_path = os.path.abspath(os.path.join(here, "..", "data", "Live.csv"))
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Put Live.csv at {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8")
    df.columns = [c.strip().lower() for c in df.columns]
    return _b64(df)


def data_preprocessing(df_b64: str) -> str:
    df: pd.DataFrame = _unb64(df_b64)

    num_cols = [c for c in df.columns if c.startswith("num_")]
    if len(num_cols) == 0:
        candidates = ["num_reactions", "num_comments", "num_shares"]
        num_cols = [c for c in candidates if c in df.columns]
    if len(num_cols) < 2:
        raise ValueError("Need at least two numeric columns like num_reactions, num_comments, num_shares.")

    X = df[num_cols].copy()
    X = X.dropna(how="all").fillna(0)

    upper = X.quantile(0.99)
    X = X.clip(upper=upper, axis=1)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X.values.astype(float))

    np.save(os.path.join(WD, "preprocessed.npy"), Xs)
    with open(os.path.join(WD, "feature_columns.json"), "w") as f:
        json.dump(num_cols, f)

    return _b64(Xs)


def build_save_model(X_b64: str, tmp_model_name: str = "model_tmp.pkl") -> Dict[str, Any]:
    Xs: np.ndarray = _unb64(X_b64)

    ks = list(range(2, 11))
    sse: List[float] = []
    sil: List[float] = []

    last = None
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        km.fit(Xs)
        sse.append(float(km.inertia_))
        sil.append(float(silhouette_score(Xs, km.labels_)))
        last = km

    tmp_path = os.path.join(WD, tmp_model_name)
    with open(tmp_path, "wb") as f:
        pickle.dump(last, f)

    with open(os.path.join(WD, "sse.json"), "w") as f:
        json.dump({"ks": ks, "sse": sse}, f)
    with open(os.path.join(WD, "silhouette.json"), "w") as f:
        json.dump({"ks": ks, "silhouette": sil}, f)

    return {"ks": ks, "sse": sse, "silhouette": sil, "tmp_model_path": tmp_path}

def choose_k_and_finalize(upstream: Dict[str, Any], final_model_name: str = "model.pkl") -> Dict[str, Any]:
    ks = upstream["ks"]; sse = upstream["sse"]; sil = upstream["silhouette"]

    knee = KneeLocator(ks, sse, curve="convex", direction="decreasing")
    chosen_k = int(knee.knee) if knee.knee is not None else int(ks[int(np.argmax(sil))])

    Xs = np.load(os.path.join(WD, "preprocessed.npy"))
    final = KMeans(n_clusters=chosen_k, n_init=10, random_state=42).fit(Xs)

    model_path = os.path.join(WD, final_model_name)
    with open(model_path, "wb") as f:
        pickle.dump(final, f)
    with open(os.path.join(WD, "chosen_k.txt"), "w") as f:
        f.write(str(chosen_k))

    labels_path = os.path.join(WD, "cluster_labels.csv")
    pd.DataFrame({"label": final.labels_}).to_csv(labels_path, index=False)

    with open(os.path.join(WD, "feature_columns.json")) as f:
        cols = json.load(f)
    summary = (
        pd.DataFrame(Xs, columns=cols)
        .assign(cluster=final.labels_)
        .groupby("cluster")
        .mean()
        .reset_index()
        .sort_values("cluster")
    )
    summary_path = os.path.join(WD, "cluster_summary.csv")
    summary.to_csv(summary_path, index=False)

    return {"chosen_k": chosen_k, "model_path": model_path, "labels_path": labels_path, "summary_path": summary_path}
