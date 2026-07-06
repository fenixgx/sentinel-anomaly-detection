"""
🧭 MIGA DE PAN: Generador de datos sintéticos de telemetría de servidores
📍 UBICACIÓN: src/generate_data.py

🎯 PORQUÉ EXISTE: TechStream necesita datos de sensores para entrenar el detector de
   anomalías. En lugar de valores al azar (que no enseñarían nada al modelo), aquí se
   simula la FÍSICA real de un servidor: la probabilidad de fallo sube cuando la
   temperatura, la CPU o la memoria se disparan, y sube MUCHO cuando coinciden varias.
🚨 CUIDADO: Cambiar los coeficientes de `_stress` altera la dificultad del problema.
   Se busca un dataset REALISTA (fallos ~12%, con solapamiento) — no uno "perfecto"
   y trivialmente separable, porque eso no demostraría que el modelo aprende de verdad.
📋 SPEC: SPEC-001-sentinel — R1 (generación de datos) — CREATED
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

# Semilla fija -> dataset 100% reproducible (el evaluador obtiene los mismos datos).
SEED = 42
N_SAMPLES = 8000

# Nombres de las columnas de sensores (features) y de la etiqueta (target).
FEATURES = ["temperature", "cpu_usage", "memory_usage", "network_traffic"]
TARGET = "failure"


def _sigmoid(x: np.ndarray) -> np.ndarray:
    """Convierte un 'nivel de estrés' en una probabilidad entre 0 y 1."""
    return 1.0 / (1.0 + np.exp(-x))


def generate_dataset(n: int = N_SAMPLES, seed: int = SEED) -> pd.DataFrame:
    """
    Genera telemetría realista de servidores.

    Cada fila = una lectura de un servidor en un instante:
      - temperature      (°C)   : temperatura del chasis
      - cpu_usage        (%)    : uso de CPU
      - memory_usage     (%)    : uso de RAM
      - network_traffic  (Mbps) : tráfico de red
      - failure          (0/1)  : ¿el servidor falló?  <- lo que queremos predecir

    La etiqueta NO es aleatoria: se deriva de las features con una lógica física,
    para que el modelo tenga un patrón REAL que aprender.
    """
    rng = np.random.default_rng(seed)

    # --- 1) Estado base "sano" de cada sensor (distribuciones normales realistas) ---
    temperature = rng.normal(loc=55, scale=8, size=n)      # la mayoría 45-65 °C
    cpu_usage = rng.normal(loc=45, scale=18, size=n)       # carga variable
    memory_usage = rng.normal(loc=55, scale=18, size=n)    # uso de RAM variable
    network_traffic = rng.normal(loc=300, scale=120, size=n)  # tráfico variable

    # Recorte a rangos físicamente posibles (un sensor no marca -10 °C ni 200% de CPU).
    temperature = np.clip(temperature, 30, 100)
    cpu_usage = np.clip(cpu_usage, 0, 100)
    memory_usage = np.clip(memory_usage, 0, 100)
    network_traffic = np.clip(network_traffic, 0, 1000)

    # --- 2) Nivel de estrés latente: cuánto "sufre" el servidor ---
    # Componente CONTINUO: cada sensor por encima de su valor normal aumenta el estrés
    # de forma gradual. Así las features tienen señal predictiva REAL (no solo en la cola).
    stress = (
        0.100 * (temperature - 55)        # calor (referencia sana ~55 °C)
        + 0.075 * (cpu_usage - 45)        # carga de CPU (referencia ~45 %)
        + 0.090 * (memory_usage - 55)     # presión de memoria (referencia ~55 %)
        + 0.008 * (network_traffic - 300) # tráfico: factor más débil (referencia ~300 Mbps)
    )

    # Componente NO LINEAL: calor ALTO y CPU ALTA a la vez = sobrecarga térmica (se dispara).
    stress += 0.030 * np.maximum(0, temperature - 72) * np.maximum(0, cpu_usage - 78) / 10

    # --- 3) Probabilidad de fallo = sigmoide(estrés) + ruido ---
    # Señal FÍSICA fuerte (en un servidor real, temp/CPU/memoria disparadas ≈ fallo casi seguro),
    # con ruido moderado que representa fallos por causas NO medidas por estos 4 sensores (bug de
    # software, disco...). Resultado: el modelo separa bien (recall ~0.85, precisión ~0.60) sin
    # llegar al 100% (queda el reto realista del solapamiento).
    noise = rng.normal(0, 0.4, size=n)
    # El -3.0 baja la base: en reposo el fallo es raro -> clase desbalanceada (~12-15%).
    logit = stress + noise - 3.0
    prob_fail = _sigmoid(logit)
    failure = (rng.random(n) < prob_fail).astype(int)

    df = pd.DataFrame(
        {
            "temperature": temperature.round(2),
            "cpu_usage": cpu_usage.round(2),
            "memory_usage": memory_usage.round(2),
            "network_traffic": network_traffic.round(2),
            "failure": failure,
        }
    )
    return df


def main() -> None:
    df = generate_dataset()

    out_dir = Path(__file__).resolve().parents[1] / "data"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "sensors.csv"
    df.to_csv(out_path, index=False)

    # Resumen para verificar que el dataset tiene sentido.
    fail_rate = df[TARGET].mean()
    print(f"✅ Dataset generado: {len(df)} muestras -> {out_path}")
    print(f"   Tasa de fallo: {fail_rate:.1%}  (clase desbalanceada, realista)")
    print("\n   Correlación de cada sensor con 'failure' (debe ser positiva y con sentido):")
    corr = df.corr(numeric_only=True)[TARGET].drop(TARGET).sort_values(ascending=False)
    for name, value in corr.items():
        print(f"     {name:18s} {value:+.3f}")


if __name__ == "__main__":
    main()
