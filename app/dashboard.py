"""
🧭 MIGA DE PAN: Interfaz web del sistema (Streamlit)
📍 UBICACIÓN: app/dashboard.py

🎯 PORQUÉ EXISTE: Convierte el modelo en una HERRAMIENTA usable. Es el "ejemplo de uso"
   elevado a interfaz: el usuario mueve los sensores y ve en vivo la probabilidad de fallo;
   si hay anomalía, el asistente RAG muestra la causa probable y las acciones recomendadas.
🚨 CUIDADO: se ejecuta con `streamlit run app/dashboard.py` (no con python directo). Reutiliza
   `predict.predict_one` (Capa 1: red neuronal) y `rag_advisor.diagnose` (Capa 2: IA aplicada).
📋 SPEC: SPEC-001-sentinel — R6 (interfaz) — CREATED
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from predict import predict_one       # noqa: E402  (Capa 1: red neuronal)
from rag_advisor import diagnose      # noqa: E402  (Capa 2: IA aplicada / RAG)

st.set_page_config(page_title="Sentinel — Detección de anomalías", page_icon="🛡️", layout="wide")

# En Streamlit Cloud la clave de OpenAI se define en Secrets. La copiamos a las variables de
# entorno para que el asistente RAG (que lee os.environ) la use. Sin clave, funciona igual.
try:
    _openai_key = st.secrets.get("OPENAI_API_KEY", "")
    if _openai_key:
        os.environ["OPENAI_API_KEY"] = _openai_key
except Exception:
    pass

st.title("🛡️ Sentinel")
st.caption("Detección de anomalías en telemetría de servidores · red neuronal (PyTorch) + diagnóstico con IA")

tab_live, tab_model = st.tabs(["🔴 Detección en vivo", "📊 Rendimiento del modelo"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Detección en vivo
# ─────────────────────────────────────────────────────────────────────────────
with tab_live:
    col_in, col_out = st.columns([1, 1.4], gap="large")

    with col_in:
        st.subheader("Lectura de sensores")
        temp = st.slider("🌡️ Temperatura (°C)", 30, 100, 55)
        cpu = st.slider("⚙️ Uso de CPU (%)", 0, 100, 45)
        mem = st.slider("🧠 Uso de memoria (%)", 0, 100, 55)
        net = st.slider("🌐 Tráfico de red (Mbps)", 0, 1000, 300)

    reading = {"temperature": temp, "cpu_usage": cpu, "memory_usage": mem, "network_traffic": net}
    result = predict_one(reading)
    prob = result["probability"]
    threshold = result["threshold"]

    with col_out:
        st.subheader("Predicción")
        st.metric("Probabilidad de fallo", f"{prob:.1%}")
        st.progress(min(prob, 1.0))

        if result["is_anomaly"]:
            st.error(f"🔴 **ANOMALÍA DETECTADA** — el servidor tiene riesgo de fallo "
                     f"(umbral de alerta: {threshold:.0%}).")
        elif prob > threshold * 0.6:
            st.warning("🟡 **Vigilancia** — los indicadores empiezan a subir.")
        else:
            st.success("🟢 **Estado normal** — el servidor opera dentro de parámetros seguros.")

    # Capa 2: diagnóstico con IA aplicada (solo si hay anomalía).
    if result["is_anomaly"]:
        st.divider()
        st.subheader("🔍 Diagnóstico IA — RAG sobre manuales técnicos")
        with st.spinner("Consultando los manuales técnicos…"):
            diag = diagnose(reading)
        st.caption(
            f"Manual recuperado: **{diag['manual'].replace('-', ' ')}** · "
            f"similitud {diag['score']:.2f} · generado vía *{diag['source']}*"
        )
        st.markdown(diag["diagnosis"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Rendimiento del modelo
# ─────────────────────────────────────────────────────────────────────────────
with tab_model:
    st.subheader("Cómo funciona y cómo se evalúa")
    st.markdown(
        "- **Modelo:** red neuronal densa (MLP) en PyTorch — `4 → 32 → 16 → 1`.\n"
        "- **Datos:** telemetría con lógica física (fallos ~16%, clase desbalanceada).\n"
        "- **Métrica prioritaria:** *recall* de la clase «fallo» — no perder servidores que van "
        "a caer es más importante que evitar alguna falsa alarma.\n"
        "- **Umbral operativo calibrado** (recall ≥ 80%): en test, **recall ≈ 0.87**."
    )

    c1, c2 = st.columns(2)
    reports = ROOT / "reports"
    cm = reports / "confusion_matrix.png"
    corr = reports / "correlations.png"
    dist = reports / "distributions.png"

    with c1:
        if cm.exists():
            st.image(str(cm), caption="Matriz de confusión (conjunto de test)")
        if corr.exists():
            st.image(str(corr), caption="Matriz de correlaciones")
    with c2:
        if dist.exists():
            st.image(str(dist), caption="Distribución de cada sensor: normal vs fallo")

    st.info(
        "Arquitectura del sistema: la red neuronal detecta la anomalía (Capa 1) y el asistente "
        "RAG diagnostica la causa y recomienda acciones sobre los manuales técnicos (Capa 2)."
    )

    # --- Descargas: dataset generado + modelo entrenado (entregables de la prueba) ---
    st.divider()
    st.markdown("**Descargar el dataset generado y el modelo entrenado:**")
    dcol1, dcol2 = st.columns(2)
    csv_path = ROOT / "data" / "sensors.csv"
    model_path = ROOT / "models" / "sentinel_model.pt"
    with dcol1:
        if csv_path.exists():
            st.download_button(
                "⬇️  Dataset (sensors.csv)", csv_path.read_bytes(),
                file_name="sensors.csv", mime="text/csv",
            )
    with dcol2:
        if model_path.exists():
            st.download_button(
                "⬇️  Modelo entrenado (.pt)", model_path.read_bytes(),
                file_name="sentinel_model.pt", mime="application/octet-stream",
            )
