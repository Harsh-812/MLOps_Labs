# Lab 4 – Dockerized Machine Learning Model (Breast Cancer Classifier)

### Objective
The goal of this lab was to containerize a small machine learning model using Docker.  
The lab shows how to build, run, and test an ML service inside a container so that the same code works the same way everywhere.  
The final setup trains a breast cancer classifier, serves it through a Flask API, and makes it available as a Docker image.

---

### Changes and Additions 

- Dataset: **Breast Cancer Wisconsin** (binary classification problem).  
- Trained a **Scikit-learn GradientBoostingClassifier** model.  
- Routes:
  - `/healthz` : shows if the app and model are running.
  - `/metadata` : returns dataset, model version, and label info.
- Updated the web page to collect the first four features of the dataset  
  (**Mean Radius**, **Mean Texture**, **Mean Perimeter**, **Mean Area**).  
- Used a multi-stage Dockerfile (first stage trains the model, second serves it with flask) that trains the model and then serves it using Flask + Gunicorn.  
- Added a Docker **HEALTHCHECK** so the container automatically reports when it is healthy.  
- Built and ran the container with `docker compose`.  
- Tagged and pushed the final image to **Docker Hub**:  
  **harshshekar812/breast-cancer-api:v1**

---

### How To Run

**Option 1 – Using Docker Compose**
```bash
docker compose up --build
```

Then open these links in a browser:
- Home UI : http://localhost:4000
- Metadata : http://localhost:4000/metadata
- Health Check : http://localhost:4000/healthz

**Option 2 – Without Docker**
```bash
pip install -r src/requirements.txt
python src/model_training.py
python src/main.py
```

---

### Docker Hub

The image is published publicly:

```bash
docker pull harshshekar812/breast-cancer-api:v1
docker run -p 4000:4000 harshshekar812/breast-cancer-api:v1
```

You can also view it here:
https://hub.docker.com/repository/docker/harshshekar812/breast-cancer-api

---

### Example Inputs and Outputs

#### Set 1 – Likely Benign

| Feature | Value |
|---------|-------|
| Mean Radius | 13.0 |
| Mean Texture | 17.0 |
| Mean Perimeter | 85.0 |
| Mean Area | 550.0 |

**Expected Output:**
```
Predicted: Benign
Benign: 82.3%
Malignant: 17.7%
```

#### Set 2 – Likely Malignant

| Feature | Value |
|---------|-------|
| Mean Radius | 18.0 |
| Mean Texture | 24.0 |
| Mean Perimeter | 120.0 |
| Mean Area | 1000.0 |

**Expected Output:**
```
Predicted: Malignant
Benign: 12.4%
Malignant: 87.6%
```

---

### Example Endpoint Outputs

#### Health Check
```json
{"status": "ok"}
```

#### Metadata
```json
{
  "dataset": "Breast Cancer Wisconsin",
  "model_version": "v1",
  "class_labels": ["Benign", "Malignant"]
}
```

---

