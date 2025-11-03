from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import time
import joblib

# Environment variables
APP_PORT = int(os.getenv("APP_PORT", "4000"))
MODEL_PATH = os.getenv("MODEL_PATH", "breast_model.pkl")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")


# Initialize Flask app and loading the model
app = Flask(__name__, static_folder="statics")
model = joblib.load(MODEL_PATH)
class_labels = ["Benign", "Malignant"]
FEATURE_NAMES = ["feature_1", "feature_2", "feature_3", "feature_4"]


# Route 1: Home page
@app.route("/")
def home():
    return render_template("predict.html")

# Route 2: Health check
@app.route("/healthz")
def healthz():
    try:
        _ = model.predict(np.zeros((1, len(FEATURE_NAMES))))
        return jsonify(status="ok"), 200
    except Exception as e:
        return jsonify(status="error", error=str(e)), 500

# Route 3: Metadata endpoint
@app.route("/metadata")
def metadata():
    return jsonify(
        model_path=MODEL_PATH,
        model_version=MODEL_VERSION,
        dataset="Breast Cancer Wisconsin",
        class_labels=class_labels,
        server_time=int(time.time())
    )

# Helper function to get feature value from request
def _get_feature(f):
    v = request.form.get(f) if request.form else None
    if v is None:
        v = request.json.get(f) if request.is_json else None
    if v is None:
        raise ValueError(f"Missing field: {f}")
    return float(v)

# Route 4: Prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Accept either form or JSON
        def get_val(name):
            if request.is_json:
                v = request.get_json().get(name)
            else:
                v = request.form.get(name)
            if v is None or v == "":
                raise ValueError(f"Missing field: {name}")
            return float(v)

        x = np.array([[get_val(n) for n in FEATURE_NAMES]])

        # Class prediction
        y_hat = model.predict(x)[0]
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(x)[0]
            if hasattr(model, "classes_") and len(model.classes_) == 2:
                probs_dict = {
                    class_labels[int(cls)]: float(p)
                    for cls, p in zip(model.classes_, proba)
                }
            else:
                probs_dict = {
                    class_labels[0]: float(proba[0]),
                    class_labels[1]: float(proba[1] if len(proba) > 1 else 1.0 - proba[0]),
                }
        else:
            probs_dict = {}

        return jsonify(
            predicted_class=class_labels[int(y_hat)],
            probabilities=probs_dict
        )
    except Exception as e:
        return jsonify(error=str(e)), 400


# Main function to run the flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT, debug=False)
