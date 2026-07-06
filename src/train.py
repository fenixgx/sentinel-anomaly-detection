"""
🧭 MIGA DE PAN: Pipeline de entrenamiento de la red neuronal
📍 UBICACIÓN: src/train.py

🎯 PORQUÉ EXISTE: Entrena la red `AnomalyMLP` sobre la telemetría. Implementa el bucle de
   entrenamiento en PyTorch a mano (no `.fit()` de sklearn), como exige la prueba: gestión
   de tensores, función de pérdida, optimizador y bucle de épocas explícitos.
🚨 CUIDADO:
   - El `StandardScaler` se ajusta SOLO con el conjunto de train (evita fuga de datos: si se
     ajustara con todo, el modelo "vería" estadísticas del test → métricas infladas y falsas).
   - Se usa `BCEWithLogitsLoss` (no `Sigmoid + BCELoss`) por estabilidad numérica: combina la
     sigmoide y la pérdida en una operación estable. El modelo, por tanto, devuelve LOGITS.
   - `pos_weight` compensa el desbalanceo (hay ~5 servidores sanos por cada uno que falla).
     Usamos la RAÍZ del ratio, no el ratio completo: penalizar ×5 dispara las falsas alarmas
     (recall alto pero precisión pésima); la raíz (~2.3) da un equilibrio recall/precisión útil.
📋 SPEC: SPEC-001-sentinel — R4 (entrenamiento) — CREATED
"""

from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import recall_score, precision_score
import joblib

# En detección de anomalías, no detectar un fallo (falso negativo) es mucho más caro que una
# falsa alarma. Política de negocio: no perder más del 20% de los fallos -> recall objetivo 0.80.
TARGET_RECALL = 0.80

# Permite ejecutar `python src/train.py` desde la raíz del proyecto importando los módulos
# hermanos (generate_data, model) sin instalar el paquete.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_data import FEATURES, TARGET  # noqa: E402
from model import AnomalyMLP  # noqa: E402

# --- Configuración reproducible ---
SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

EPOCHS = 80
BATCH_SIZE = 64
LEARNING_RATE = 1e-3

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sensors.csv"
MODELS_DIR = ROOT / "models"
MODEL_PATH = MODELS_DIR / "sentinel_model.pt"
SCALER_PATH = MODELS_DIR / "scaler.joblib"


def load_splits():
    """
    Carga el CSV y lo parte en train/val/test de forma ESTRATIFICADA (mantiene la proporción
    de fallos en cada subconjunto — clave con clases desbalanceadas) y escala las features.
    """
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES].values.astype(np.float32)
    y = df[TARGET].values.astype(np.float32)

    # 70% train, 15% val, 15% test. stratify=y -> misma tasa de fallo en los tres.
    X_train, X_tmp, y_train, y_tmp = train_test_split(
        X, y, test_size=0.30, random_state=SEED, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.50, random_state=SEED, stratify=y_tmp
    )

    # Escalado: ajustar SOLO con train, aplicar a los tres (sin fuga de datos).
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)
    X_test = scaler.transform(X_test)

    return (X_train, y_train), (X_val, y_val), (X_test, y_test), scaler


def make_loader(X, y, shuffle: bool) -> DataLoader:
    """Convierte arrays de numpy en tensores de PyTorch y los envuelve en un DataLoader."""
    dataset = TensorDataset(torch.from_numpy(X).float(), torch.from_numpy(y).float())
    return DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=shuffle)


@torch.no_grad()
def evaluate_recall(model: nn.Module, loader: DataLoader, device: str) -> tuple[float, float]:
    """Calcula pérdida media y recall de la clase 'fallo' sobre un loader (modo evaluación)."""
    model.eval()
    tp = fn = 0
    total_loss = 0.0
    n_batches = 0
    bce = nn.BCEWithLogitsLoss()
    for xb, yb in loader:
        xb, yb = xb.to(device), yb.to(device)
        logits = model(xb)
        total_loss += bce(logits, yb).item()
        n_batches += 1
        preds = (torch.sigmoid(logits) >= 0.5).float()
        tp += ((preds == 1) & (yb == 1)).sum().item()
        fn += ((preds == 0) & (yb == 1)).sum().item()
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return total_loss / max(n_batches, 1), recall


@torch.no_grad()
def select_operating_threshold(model, X_val, y_val, device) -> tuple[float, float, float]:
    """
    Calibra el umbral operativo sobre VALIDACIÓN (no usamos 0.5 a ciegas).

    Política orientada al DOMINIO (detección de anomalías): priorizar recall, porque no
    detectar un fallo es mucho más caro que una falsa alarma. Entre los umbrales que consiguen
    recall >= TARGET_RECALL, se elige el de MAYOR precisión (el umbral más alto que aún cumple
    el objetivo → menos falsas alarmas sin sacrificar el recall). Si ninguno llega al objetivo,
    se coge el de mayor recall disponible.
    """
    model.eval()
    logits = model(torch.from_numpy(X_val).float().to(device))
    probs = torch.sigmoid(logits).cpu().numpy()

    candidates = []  # (umbral, recall, precisión)
    for t in np.arange(0.20, 0.71, 0.05):
        preds = (probs >= t).astype(int)
        r = recall_score(y_val, preds, zero_division=0)
        p = precision_score(y_val, preds, zero_division=0)
        candidates.append((round(float(t), 2), r, p))

    ok = [c for c in candidates if c[1] >= TARGET_RECALL]
    if ok:
        best = max(ok, key=lambda c: c[2])   # mayor precisión entre los que cumplen el recall
    else:
        best = max(candidates, key=lambda c: c[1])  # si ninguno llega, el de mayor recall
    return best  # (umbral, recall, precisión)


def main() -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🖥️  Dispositivo: {device}")

    (X_train, y_train), (X_val, y_val), (X_test, y_test), scaler = load_splits()
    print(f"📊 Split -> train:{len(y_train)}  val:{len(y_val)}  test:{len(y_test)}")

    train_loader = make_loader(X_train, y_train, shuffle=True)
    val_loader = make_loader(X_val, y_val, shuffle=False)

    model = AnomalyMLP(n_features=len(FEATURES)).to(device)

    # pos_weight compensa el desbalanceo. Usamos la RAÍZ del ratio neg/pos (no el ratio
    # completo): el ratio completo (~5) hace el modelo demasiado "gritón" (mucho recall, poca
    # precisión); la raíz (~2.3) da un equilibrio recall/precisión mucho más útil en la práctica.
    n_pos = float(y_train.sum())
    n_neg = float(len(y_train) - n_pos)
    imbalance = n_neg / n_pos
    pos_weight = torch.tensor([imbalance ** 0.5], device=device)
    print(f"⚖️  desbalanceo neg/pos: {imbalance:.2f}  ->  pos_weight (raíz): {pos_weight.item():.2f}")

    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-5)

    best_val_loss = float("inf")
    best_state = None

    for epoch in range(1, EPOCHS + 1):
        # --- Entrenamiento ---
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()          # 1) limpiar gradientes acumulados
            logits = model(xb)             # 2) paso adelante -> logits
            loss = criterion(logits, yb)   # 3) pérdida ponderada por el desbalanceo
            loss.backward()                # 4) retropropagación (calcula gradientes)
            optimizer.step()               # 5) actualizar los pesos

        # --- Validación (guardamos el MEJOR modelo, no el último) ---
        val_loss, val_recall = evaluate_recall(model, val_loader, device)
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}

        if epoch % 10 == 0 or epoch == 1:
            print(f"  época {epoch:3d}  val_loss={val_loss:.4f}  val_recall={val_recall:.3f}")

    # --- Cargar el mejor modelo y CALIBRAR el umbral operativo sobre validación ---
    model.load_state_dict(best_state)
    best_threshold, best_recall, best_precision = select_operating_threshold(
        model, X_val, y_val, device
    )
    print(f"\n🎯 Umbral operativo calibrado (recall objetivo ≥ {TARGET_RECALL:.0%}, en validación): "
          f"{best_threshold:.2f}  (recall={best_recall:.3f}, precisión={best_precision:.3f})")

    # --- Guardado del modelo entrenado + scaler + metadatos ---
    MODELS_DIR.mkdir(exist_ok=True)
    checkpoint = {
        "state_dict": best_state,
        "feature_names": FEATURES,
        "n_features": len(FEATURES),
        "threshold": best_threshold,  # umbral calibrado, no 0.5 a ciegas
        "seed": SEED,
    }
    torch.save(checkpoint, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ Modelo guardado en {MODEL_PATH}")
    print(f"✅ Scaler guardado en {SCALER_PATH}")
    print(f"   Mejor val_loss: {best_val_loss:.4f}")


if __name__ == "__main__":
    main()
