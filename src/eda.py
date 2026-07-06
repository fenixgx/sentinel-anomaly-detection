"""
🧭 MIGA DE PAN: Análisis Exploratorio de Datos (EDA)
📍 UBICACIÓN: src/eda.py

🎯 PORQUÉ EXISTE: Cubre el punto "Análisis Exploratorio (EDA): visualización de correlaciones
   y preparación de datos" de la prueba. Genera las gráficas y deja por escrito las decisiones
   de preparación (por qué escalar, por qué estratificar, por qué priorizar recall).
🚨 CUIDADO: usa backend 'Agg' (guarda a archivo, no abre ventana) para poder correr en
   servidores/CI sin entorno gráfico. Depende de que exista `data/sensors.csv`.
📋 SPEC: SPEC-001-sentinel — R2 (EDA) — CREATED
"""

from __future__ import annotations
import sys
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_data import FEATURES, TARGET  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sensors.csv"
REPORTS = ROOT / "reports"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    REPORTS.mkdir(exist_ok=True)

    # --- Balance de clases ---
    fail_rate = df[TARGET].mean()
    n_fail = int(df[TARGET].sum())
    print("=" * 60)
    print("ANÁLISIS EXPLORATORIO (EDA)")
    print("=" * 60)
    print(f"Muestras: {len(df)}  |  Fallos: {n_fail} ({fail_rate:.1%})  |  Normales: {len(df)-n_fail}")
    print("→ Clase DESBALANCEADA: la accuracy engaña, priorizaremos el recall de la clase 'fallo'.")

    # --- 1) Matriz de correlaciones ---
    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True,
                cbar_kws={"shrink": 0.8})
    plt.title("Matriz de correlaciones")
    plt.tight_layout()
    plt.savefig(REPORTS / "correlations.png", dpi=120)
    plt.close()

    print("\nCorrelación de cada sensor con 'failure':")
    for name, val in corr[TARGET].drop(TARGET).sort_values(ascending=False).items():
        print(f"  {name:18s} {val:+.3f}")

    # --- 2) Distribución de cada sensor por clase (normal vs fallo) ---
    fig, axes = plt.subplots(1, len(FEATURES), figsize=(16, 4))
    for ax, feat in zip(axes, FEATURES):
        sns.boxplot(data=df, x=TARGET, y=feat, ax=ax, hue=TARGET,
                    palette=["#4c72b0", "#c44e52"], legend=False)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["normal", "fallo"])
        ax.set_xlabel("")
        ax.set_title(feat)
    plt.suptitle("Distribución de cada sensor: servidores normales vs fallos", y=1.02)
    plt.tight_layout()
    plt.savefig(REPORTS / "distributions.png", dpi=120, bbox_inches="tight")
    plt.close()

    # --- Conclusiones (decisiones de preparación de datos) ---
    print("\nConclusiones del EDA (decisiones de preparación):")
    print("  1. Desbalanceo (~15% fallos) → usar recall como métrica prioritaria + pos_weight.")
    print("  2. Los sensores correlacionan POSITIVAMENTE con el fallo (memoria y CPU los más fuertes).")
    print("  3. Escalas muy dispares (temp ~decenas °C, red ~cientos de Mbps) → StandardScaler.")
    print("  4. Split ESTRATIFICADO para mantener la misma tasa de fallo en train/val/test.")
    print(f"\n✅ Gráficas guardadas: {REPORTS/'correlations.png'} · {REPORTS/'distributions.png'}")


if __name__ == "__main__":
    main()
