"""
🧭 MIGA DE PAN: Inferencia — usar el modelo entrenado sobre una lectura nueva
📍 UBICACIÓN: src/predict.py

🎯 PORQUÉ EXISTE: Es el "ejemplo de uso de la solución" que pide la prueba. Carga el modelo
   y el scaler guardados y, dada una lectura de sensores, devuelve la probabilidad de fallo y
   si es una anomalía (según el umbral calibrado). Lo reutiliza el dashboard (app/dashboard.py).
🚨 CUIDADO: hay que aplicar EL MISMO scaler del entrenamiento (por eso se guardó). El modelo
   devuelve un logit; la probabilidad se obtiene con torch.sigmoid(). Carga perezosa + caché
   (singleton) para no releer el modelo del disco en cada predicción.
📋 SPEC: SPEC-001-sentinel — R5 (inferencia / ejemplo de uso) — CREATED
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import torch
import joblib

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model import AnomalyMLP  # noqa: E402
from generate_data import FEATURES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "sentinel_model.pt"
SCALER_PATH = ROOT / "models" / "scaler.joblib"

# Caché en memoria (se carga una vez y se reutiliza).
_cache: dict = {}


def _load():
    """Carga perezosa del modelo + scaler + umbral (una sola vez)."""
    if not _cache:
        checkpoint = torch.load(MODEL_PATH, weights_only=False)
        model = AnomalyMLP(n_features=checkpoint["n_features"])
        model.load_state_dict(checkpoint["state_dict"])
        model.eval()
        _cache["model"] = model
        _cache["scaler"] = joblib.load(SCALER_PATH)
        _cache["threshold"] = checkpoint.get("threshold", 0.5)
        _cache["features"] = checkpoint.get("feature_names", FEATURES)
    return _cache


def predict_one(reading: dict) -> dict:
    """
    Predice el riesgo de fallo de una lectura de sensores.

    reading: {'temperature':.., 'cpu_usage':.., 'memory_usage':.., 'network_traffic':..}
    Devuelve: {'probability': float, 'is_anomaly': bool, 'threshold': float}
    """
    c = _load()
    x = np.array([[reading[f] for f in c["features"]]], dtype=np.float32)
    x = c["scaler"].transform(x)  # mismo escalado que en el entrenamiento
    with torch.no_grad():
        logit = c["model"](torch.from_numpy(x).float())
        prob = torch.sigmoid(logit).item()
    return {
        "probability": prob,
        "is_anomaly": prob >= c["threshold"],
        "threshold": c["threshold"],
    }


def main() -> None:
    ejemplos = {
        "Servidor sano":      {"temperature": 52, "cpu_usage": 40, "memory_usage": 50, "network_traffic": 280},
        "Servidor cargado":   {"temperature": 70, "cpu_usage": 78, "memory_usage": 80, "network_traffic": 520},
        "Servidor crítico":   {"temperature": 90, "cpu_usage": 96, "memory_usage": 94, "network_traffic": 880},
    }
    print("Ejemplo de uso — predicción sobre lecturas nuevas:\n")
    for nombre, lectura in ejemplos.items():
        r = predict_one(lectura)
        estado = "🔴 ANOMALÍA" if r["is_anomaly"] else "🟢 Normal"
        print(f"  {nombre:18s} {estado:14s}  prob. fallo {r['probability']:5.1%}  (umbral {r['threshold']:.0%})")


if __name__ == "__main__":
    main()
