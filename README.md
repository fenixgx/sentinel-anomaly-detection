# 🛡️ Sentinel — Detección de anomalías en telemetría de servidores

Sistema que **anticipa fallos de servidor** a partir de su telemetría (temperatura, CPU,
memoria, tráfico de red) con una **red neuronal en PyTorch**, y **diagnostica la causa** con un
**asistente de IA (RAG sobre manuales técnicos)**. Todo accesible desde una **interfaz web**.

> Prueba técnica — vacante Técnico Informático IA.

---

## Qué hace

Dos capas complementarias:

1. **Detección (red neuronal).** Un MLP en PyTorch clasifica cada lectura de sensores como
   *normal* o *fallo inminente*.
2. **Diagnóstico (IA aplicada).** Cuando se detecta una anomalía, un asistente RAG recupera el
   manual técnico relevante y explica la **causa probable** y las **acciones recomendadas**.

La idea de fondo: un modelo en producción no vale solo por su exactitud, sino por lo **útil y
accionable** que es. Sentinel no solo predice — **explica y guía**.

## Arquitectura

```
telemetría (CSV) → red neuronal (PyTorch) → ¿fallo? → RAG advisor (manuales) → interfaz web
```

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
# 1. Entorno + dependencias
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
#  (alternativa rápida con uv:  uv venv && uv pip install -r requirements.txt)

# 2. Pipeline completo (reproducible — semilla fija)
python src/generate_data.py   # genera data/sensors.csv
python src/eda.py             # análisis exploratorio -> reports/
python src/train.py           # entrena el modelo    -> models/
python src/evaluate.py        # métricas + matriz de confusión
python src/predict.py         # ejemplo de uso (predicción sobre lecturas nuevas)

# 3. Interfaz web
streamlit run app/dashboard.py
```

El repositorio ya incluye el **modelo entrenado** (`models/`) y los **datos** (`data/`), así que
puedes ir directo a `evaluate.py`, `predict.py` o el dashboard **sin reentrenar**.

## Estructura del proyecto

```
sentinel/
├── src/
│   ├── generate_data.py   # generador de telemetría con lógica física realista
│   ├── eda.py             # análisis exploratorio (correlaciones, distribuciones)
│   ├── model.py           # arquitectura de la red neuronal (clase nn.Module)
│   ├── train.py           # entrenamiento en PyTorch + calibración de umbral
│   ├── evaluate.py        # precision/recall/F1 + matriz de confusión + análisis de umbral
│   ├── predict.py         # inferencia (el "ejemplo de uso")
│   └── rag_advisor.py     # IA aplicada: RAG sobre los manuales técnicos
├── app/dashboard.py       # interfaz web (Streamlit)
├── manuals/               # base de conocimiento: manuales técnicos de fallos
├── data/    sensors.csv   # datos generados
├── models/  *.pt, *.joblib# modelo entrenado + normalizador
├── reports/ *.png         # gráficas (EDA + matriz de confusión)
└── .spec/                 # documentación del proyecto (metodología de trabajo)
```

## Resultados (sobre el conjunto de test)

| Métrica | Valor |
|---|---|
| **Recall (clase «fallo»)** | **≈ 0.87** |
| Muestras / tasa de fallo | 8000 / ~16 % (clase desbalanceada) |
| Correlación de los sensores con el fallo | memoria +0.34 · CPU +0.30 · red +0.21 · temp +0.18 |

Se **prioriza el recall**: en detección de anomalías, no detectar un fallo (un servidor que cae
sin aviso) es más caro que una falsa alarma. La matriz de confusión y el análisis del trade-off
recall/precisión están en `evaluate.py` y `reports/`.

## Decisiones de diseño (el porqué)

- **MLP y no LSTM:** cada lectura se clasifica de forma independiente (datos tabulares); el MLP
  es más simple, interpretable y mantenible. El LSTM correspondería a predecir el fallo desde la
  *evolución* temporal de cada servidor — anotado como trabajo futuro.
- **`BCEWithLogitsLoss`** en vez de `Sigmoid + BCELoss`: numéricamente más estable.
- **`pos_weight` (raíz del ratio de desbalanceo):** compensa las clases sin volver el modelo
  demasiado "gritón" (equilibrio recall/precisión).
- **Escalado sin fuga de datos:** el `StandardScaler` se ajusta **solo** con el train.
- **Umbral operativo calibrado:** no se usa 0.5 a ciegas; se elige sobre validación con una
  política de dominio (recall objetivo ≥ 80 %).

## IA aplicada (RAG) — con y sin LLM

El asistente funciona **sin ninguna clave**: recupera el manual relevante (TF-IDF + similitud
coseno) y responde con su contenido. Para activar la generación en lenguaje natural con un LLM:

```bash
export OPENAI_API_KEY="tu-clave"   # opcional
```

Sin la clave, el sistema **degrada con elegancia** a una respuesta basada en el manual
recuperado. En ningún caso inventa causas o acciones fuera de los manuales.

## Metodología

El proyecto está documentado con un sistema de **SPECs** (carpeta `.spec/`): problema,
requisitos, plan de tareas y una bitácora con las decisiones tomadas (incluido el proceso de
ajuste del modelo). Es la forma en que estructuro y dejo trazable el desarrollo asistido por IA.

## Entregables de la prueba

- [x] Generador de datos inicial — `src/generate_data.py`
- [x] Datos generados — `data/sensors.csv`
- [x] Código de la tarea — este repositorio
- [x] Modelo entrenado — `models/sentinel_model.pt`
- [ ] Vídeo explicativo
