"""
🧭 MIGA DE PAN: Tema visual y paleta consistente para las gráficas
📍 UBICACIÓN: src/viz_style.py

🎯 PORQUÉ EXISTE: Da a todas las gráficas (EDA + matriz de confusión) un aspecto profesional
   y coherente — se leen "como un sistema", no como capturas sueltas. Cada color se asigna
   según su TRABAJO: categórico (normal vs fallo), secuencial (magnitud), diverging (±correlación).
🚨 CUIDADO: llamar `apply_style()` UNA vez antes de crear las figuras. El color de "fallo" es
   rojo a propósito (semántica de estado crítico); "normal" es azul sobrio.
📋 SPEC: SPEC-001-sentinel — R2/R5 (pulido visual de las gráficas) — CREATED
"""

from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns

# --- Paleta categórica (identidad: normal vs fallo) ---
COLOR_NORMAL = "#4C78A8"   # azul sobrio  -> servidor normal
COLOR_FALLO = "#E45756"    # rojo/coral   -> servidor en fallo (estado crítico)

# --- Tintas de texto (el texto NUNCA lleva el color de la serie) ---
INK = "#2B2B2B"
MUTED = "#6E6E6E"

# --- Colormaps por trabajo ---
CMAP_SEQUENTIAL = "Blues"    # magnitud (conteos de la matriz de confusión)
CMAP_DIVERGING = "RdBu_r"    # polaridad (correlaciones de -1 a +1, gris neutro en 0)


def apply_style() -> None:
    """Configura un tema limpio y profesional para matplotlib + seaborn."""
    sns.set_theme(style="white")
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.edgecolor": "#D8D8D8",
        "axes.linewidth": 1.0,
        "axes.grid": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.titlepad": 12,
        "axes.labelsize": 11,
        "axes.labelcolor": MUTED,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.dpi": 120,
    })
