import os
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

if __name__ == "__main__":
    # load data
    data = load_breast_cancer()
    X, y = data.data, data.target
    # Using only first 4 features for demo 
    X = X[:, :4]

    test_size = float(os.getenv("TEST_SIZE", "0.2"))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # training a boosting model
    model = GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.08, max_depth=2, random_state=42
    )
    model.fit(X_train, y_train)

    # evaluate
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
    }

    # save artifacts
    joblib.dump(model, "breast_model.pkl")
    print("Breast-cancer model trained and saved (metrics):", metrics)

    

    
    
    