## Lab 3 – Airflow Pipeline (K-Means Clustering: Facebook Live Sellers Dataset)

**Goal:**  
Use Apache Airflow to automate an end-to-end ML pipeline that clusters Facebook Live selling posts based on engagement metrics.

**Dataset:**  
[Facebook Live Sellers in Thailand (UCI Repository)](https://archive.ics.uci.edu/ml/datasets/Facebook+Live+Sellers+in+Thailand)

**Pipeline Steps:**
1. **Data Load** – Read the CSV dataset using Airflow’s `PythonOperator`.
2. **Preprocessing** – Normalize engagement features like reactions, comments, and shares.
3. **Modeling** – Run K-Means clustering for different `k` values and calculate SSE and silhouette scores.
4. **Model Selection** – Choose the optimal number of clusters (elbow method).
5. **Outputs** – Save artifacts (cluster summaries, chosen_k, model file, etc.) to `/working_data`.

**Outcome:**  

The DAG executed successfully inside the Docker-based Airflow environment after initial troubleshooting.  
During the first run, I encountered an error in the **`compute_sse_and_silhouette`** task caused by a version mismatch in scikit-learn (`n_init="auto"` not supported in the Airflow image).  
I inspected the Airflow logs, identified the traceback, and fixed it by explicitly setting `n_init=10` for compatibility.  
After updating the code, all tasks — data loading, preprocessing, model building, and evaluation — ran successfully and produced the expected outputs.

<img width="899" height="909" alt="image" src="https://github.com/user-attachments/assets/bf8e5130-475f-434b-a072-e1c689e0d1d9" />

