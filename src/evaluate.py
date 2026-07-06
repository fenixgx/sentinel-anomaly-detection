"""
🧭 MIGA DE PAN: Evaluación del modelo (métricas + matriz de confusión)
📍 UBICACIÓN: src/evaluate.py

🎯 PORQUÉ EXISTE: Mide el modelo sobre el conjunto de TEST (datos que nunca vio en el
   entrenamiento), como pide la prueba: precisión, recall y matriz de confusión.
🚨 CUIDADO: En un problema DESBALANCEADO la *accuracy* engaña — un modelo que nunca predice
   "fallo" acierta el ~84% y es inútil. Por eso el foco está en el RECALL de la clase "fallo"
   (no perder servidores que van a caer). Se incluye un análisis de umbral para mostrar el
   trade-off recall/precisión, que es una decisión de negocio, no solo técnica.
📋 SPEC: SPEC-001-sentinel — R5 (evaluación) — CREATED
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")  # backend sin ventana (guarda a archivo, no abre GUI)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import load_splits, MODEL_PATH  # noqa: E402  (reutiliza el MISMO split, misma semilla)
from model import AnomalyMLP  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
CLASS_NAMES = ["normal", "fallo"]


def load_trained_model() -> tuple[AnomalyMLP, dict]:
    """Carga el checkpoint guardado y reconstruye el modelo en modo evaluación."""
    checkpoint = torch.load(MODEL_PATH, weights_only=False)
    model = AnomalyMLP(n_features=checkpoint["n_features"])
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, checkpoint


def main() -> None:
    # Reproduce el MISMO split que el entrenamiento (misma semilla) y coge el TEST.
    _, _, (X_test, y_test), _ = load_splits()
    model, checkpoint = load_trained_model()

    # Inferencia: logits -> probabilidad de fallo con la sigmoide.
    with torch.no_grad():
        logits = model(torch.from_numpy(X_test).float())
        probs = torch.sigmoid(logits).numpy()

    threshold = checkpoint.get("threshold", 0.5)
    preds = (probs >= threshold).astype(int)

    # --- Informe principal (umbral por defecto) ---
    print("=" * 60)
    print(f"EVALUACIÓN SOBRE TEST (n={len(y_test)}, umbral={threshold})")
    print("=" * 60)
    print(classification_report(y_test, preds, target_names=CLASS_NAMES, digits=3))

    cm = confusion_matrix(y_test, preds)
    tn, fp, fn, tp = cm.ravel()
    print("Matriz de confusión:")
    print(f"                 predicho NORMAL   predicho FALLO")
    print(f"  real NORMAL          {tn:5d}            {fp:5d}")
    print(f"  real FALLO           {fn:5d}            {tp:5d}")

    # --- Interpretación en términos de negocio ---
    print("\nInterpretación:")
    print(f"  • Fallos detectados (TP): {tp}  -> avisamos antes de la caída.")
    print(f"  • Fallos NO detectados (FN): {fn}  -> servidores que caerían sin aviso (lo caro).")
    print(f"  • Falsas alarmas (FP): {fp}  -> revisiones innecesarias (molestas, pero baratas).")
    print(f"  • Recall (fallo): {recall_score(y_test, preds):.3f}  <- métrica prioritaria aquí.")
    print(f"  • Precision (fallo): {precision_score(y_test, preds):.3f}")

    # --- Análisis de umbral: el trade-off recall/precisión es una decisión de negocio ---
    print("\nAnálisis de umbral (cómo cambia el modelo según lo agresivo que seamos):")
    print("  umbral   recall   precision")
    for t in [0.30, 0.40, 0.50, 0.60, 0.70]:
        p = (probs >= t).astype(int)
        r = recall_score(y_test, p, zero_division=0)
        pr = precision_score(y_test, p, zero_division=0)
        marca = "  <- por defecto" if abs(t - threshold) < 1e-9 else ""
        print(f"   {t:.2f}    {r:.3f}     {pr:.3f}{marca}")
    print("  → Bajar el umbral captura más fallos (más recall) a costa de más falsas alarmas.")
    print("    En detección de anomalías se suele priorizar el recall.")

    # --- Guardar matriz de confusión como imagen ---
    REPORTS_DIR.mkdir(exist_ok=True)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=[f"pred. {c}" for c in CLASS_NAMES],
        yticklabels=[f"real {c}" for c in CLASS_NAMES],
    )
    plt.title("Matriz de confusión — Sentinel")
    plt.tight_layout()
    out = REPORTS_DIR / "confusion_matrix.png"
    plt.savefig(out, dpi=120)
    plt.close()
    print(f"\n✅ Matriz de confusión guardada en {out}")


if __name__ == "__main__":
    main()
