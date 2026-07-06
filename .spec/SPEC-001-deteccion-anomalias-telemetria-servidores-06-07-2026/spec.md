# SPEC-001: Sistema de Detección de Anomalías en Telemetría de Servidores

**Proyecto:** Sentinel
**Fecha:** 2026-07-06
**Autor:** Rodolfo Giannotti
**Contexto:** Prueba técnica — vacante Técnico Informático IA (TechTitute)

<!--
╔═══════════════════════════════════════════════════════════════════════════╗
║ 📍 QUÉ ES ESTO                                                             ║
║ Sentinel — Detector de anomalías en servidores. Una red neuronal (MLP en   ║
║ PyTorch) predice si un servidor va a fallar a partir de su telemetría, y    ║
║ una capa de IA aplicada (RAG sobre manuales) diagnostica la causa y propone ║
║ la solución.                                                                ║
║                                                                             ║
║ 🏗️ ARQUITECTURA                                                            ║
║ telemetría (CSV) → red neuronal (clasificación) → ¿fallo? → RAG advisor →   ║
║ diagnóstico + recomendación → interfaz web (Streamlit)                      ║
║                                                                             ║
║ 📂 ARCHIVOS CLAVE                                                           ║
║ src/generate_data.py · src/model.py · src/train.py · src/evaluate.py ·      ║
║ src/predict.py · src/rag_advisor.py · app/dashboard.py                      ║
║                                                                             ║
║ ⚠️ CUIDADO                                                                  ║
║ El scaler se ajusta SOLO con train (sin fuga de datos). El modelo devuelve  ║
║ logits (sin sigmoide); la probabilidad se obtiene con torch.sigmoid().      ║
╚═══════════════════════════════════════════════════════════════════════════╝
-->

<!--
🔗 CROSS-REFERENCES ENTRE SPECs
   Proyecto STANDALONE (prueba técnica). Primer y único SPEC del workspace SENTINEL.
   Sin extends / depends_on / replaces / related.
-->

---

## Problema

**TechStream** gestiona una gran flota de servidores y genera continuamente datos de
telemetría (temperatura, uso de CPU, memoria, tráfico de red). Hoy, un fallo de servidor
se detecta **cuando ya ha ocurrido**: el servicio se cae, y solo entonces el equipo reacciona.

### Síntomas actuales:
- **Dolor 1 — Reacción tardía:** los fallos se descubren por su impacto (caída del servicio),
  no por sus síntomas previos. Un servidor caído sin aviso tiene un coste alto.
- **Dolor 2 — Diagnóstico manual:** aunque se detecte un patrón raro, un técnico tiene que
  cruzar los valores con miles de manuales para saber *qué* pasa y *qué* hacer. Lento y
  dependiente de la experiencia de quien esté de guardia.
- **Dolor 3 — Datos desaprovechados:** la telemetría existe pero no alimenta ningún modelo
  predictivo. La información está, pero no se convierte en anticipación.

### Métricas del problema:
| Métrica | Actual | Objetivo |
|---------|--------|----------|
| Momento de detección | tras la caída | antes de la caída |
| Diagnóstico de causa | manual, minutos/horas | automático, segundos |
| Aprovechamiento de la telemetría | 0 (no hay modelo) | modelo predictivo entrenado |

## Solución

Sistema en **dos capas complementarias**, cerradas con una interfaz web.

**Capa 1 — Detección (lo que exige la prueba).** Una red neuronal densa (MLP) en **PyTorch**
clasifica cada lectura de sensores como *normal* o *fallo inminente*. Se entrena sobre datos
de telemetría con lógica física realista y se evalúa con métricas adecuadas a un problema
desbalanceado (precisión, recall, matriz de confusión).

**Capa 2 — Diagnóstico con IA aplicada (valor añadido).** Cuando la Capa 1 marca una anomalía,
un **asistente RAG** recupera el manual técnico más relevante y genera, en lenguaje natural,
la **causa probable** y las **acciones recomendadas**. Es la diferencia entre *"algo va mal"*
y *"esto pasa y esto debes hacer"*.

**Interfaz.** Un panel web (**Streamlit**) permite introducir lecturas, ver la probabilidad
de fallo en vivo y, si hay anomalía, leer el diagnóstico del asistente.

**Filosofía:** un modelo en producción no vale por su exactitud aislada, sino por lo útil y
accionable que es para quien lo usa. Por eso el sistema no solo predice: **explica y guía.**
**Estrategia:** cumplir estrictamente los 5 puntos de la prueba (R1-R5) y añadir dos capas de
valor alineadas con el perfil de IA aplicada (R6-R7) sin desviar el foco del núcleo evaluado.

---

## 📁 FILE STRUCTURE (🔴 MANTENER ACTUALIZADA)

**Last Updated:** 2026-07-06

### ✅ Archivos a crear:
- `src/generate_data.py` — Generador de telemetría sintética con lógica física → `data/sensors.csv` ✅ HECHO
- `src/model.py` — Clase `AnomalyMLP` (arquitectura de la red en PyTorch) ✅ HECHO
- `src/eda.py` — Análisis exploratorio (correlaciones, distribuciones) → imágenes en `reports/`
- `src/train.py` — Pipeline de entrenamiento (split, escalado, bucle, guardado)
- `src/evaluate.py` — Métricas (precision/recall/F1 + matriz de confusión)
- `src/predict.py` — Carga del modelo + inferencia sobre lecturas nuevas
- `src/rag_advisor.py` — Capa de IA aplicada: RAG sobre manuales → diagnóstico + recomendación
- `app/dashboard.py` — Interfaz web (Streamlit)
- `manuals/*.md` — Base de conocimiento de manuales técnicos (para el RAG)
- `README.md` · `requirements.txt` · `pyproject.toml` · `.gitignore`

### 📦 Artefactos generados (no versionados):
- `data/sensors.csv` — Dataset generado ✅
- `models/sentinel_model.pt` — Pesos del modelo entrenado
- `models/scaler.joblib` — Normalizador ajustado en train
- `reports/*.png` — Gráficas del EDA y la matriz de confusión

### ⚙️ Config externa (Rodolfo):
- Repositorio GitHub (fenixgx) — para entrega.
- `OPENAI_API_KEY` opcional (el RAG advisor degrada sin ella).

---

## Requirements

<!-- Cada requirement mapea 1:1 con un punto de la prueba técnica. La correspondencia se
     indica explícitamente para que el evaluador vea que cada punto está cubierto. -->

### R1: Generación de datos de telemetría realistas [MVP]

**Mapea a la prueba:** *"Generar con Python un CSV con datos de sensores… Deben tener cierto
sentido para ser utilizados como datos de entrenamiento."*

**Problema:** sin datos con patrón real, el modelo no puede aprender nada útil.
**Solución:** generador que simula la física del servidor — la probabilidad de fallo sube de
forma continua con temperatura, CPU y memoria, y se dispara cuando coinciden calor y carga
(sobrecarga térmica). Ruido añadido para que el problema no sea trivialmente separable.

Comportamiento esperado:
- CUANDO se ejecuta el generador ENTONCES produce un CSV reproducible (semilla fija).
- CUANDO se calculan las correlaciones ENTONCES memoria, CPU y tráfico correlacionan
  positivamente con el fallo (patrón con sentido físico).
- El dataset DEBE ser desbalanceado (fallos ~10-20%), como en un entorno real.

Criterios de aceptación:
- [x] CSV con 4 sensores + etiqueta binaria `failure`.
- [x] Tasa de fallo en rango realista (verificado: 17.6%).
- [x] Correlaciones positivas y coherentes (verificado: memoria +0.19, CPU +0.18, red +0.15, temp +0.11).

🔗 **Tasks:** tasks.md Fase 1
📊 **Status:** ✅ Completado y verificado

---

### R2: Análisis exploratorio de datos (EDA) [MVP]

**Mapea a la prueba:** *"Análisis Exploratorio (EDA): Breve visualización de correlaciones y
preparación de datos."*

**Problema:** hay que entender los datos antes de modelar (qué sensores importan, si hay
desbalanceo, si las escalas son dispares).
**Solución:** script que visualiza distribuciones, matriz de correlaciones y balance de clases,
y documenta las decisiones de preparación (escalado, split estratificado).

Comportamiento esperado:
- CUANDO se ejecuta el EDA ENTONCES genera matriz de correlaciones + distribuciones por clase
  guardadas como imágenes en `reports/`.
- El EDA DEBE evidenciar el desbalanceo y justificar el uso de recall como métrica prioritaria.

Criterios de aceptación:
- [ ] Heatmap de correlaciones guardado.
- [ ] Distribuciones de cada sensor por clase (normal vs fallo).
- [ ] Conclusiones escritas (qué sensores predicen, por qué escalar, por qué estratificar).

🔗 **Tasks:** tasks.md Fase 2
📊 **Status:** ✅ Completado y verificado en ejecución

---

### R3: Arquitectura de red neuronal en PyTorch [MVP]

**Mapea a la prueba:** *"Diseñar una red neuronal densa (MLP)… utilizando PyTorch. No basta
con usar sklearn. Queremos ver cómo construyes la clase de la arquitectura y cómo gestionas
los tensores."*

**Problema:** el requisito central — demostrar dominio de PyTorch a bajo nivel, no una caja negra.
**Solución:** clase `AnomalyMLP(nn.Module)` con `__init__` (capas) y `forward` (paso adelante),
gestión explícita de la forma de los tensores, salida en logits (la sigmoide la aplica la
función de pérdida, por estabilidad numérica).

Comportamiento esperado:
- CUANDO se instancia el modelo ENTONCES define una red `4 → 32 → 16 → 1` con ReLU y Dropout.
- CUANDO entra un batch `(N, 4)` ENTONCES `forward` devuelve `(N,)` logits.
- El modelo NO DEBE usar `sklearn` para la red (solo PyTorch).

Criterios de aceptación:
- [x] Clase `nn.Module` con `__init__` y `forward` explícitos.
- [x] Gestión de tensores visible (`squeeze` de la forma de salida).
- [x] Dropout para regularización + justificación de MLP frente a LSTM.

🔗 **Tasks:** tasks.md Fase 3
📊 **Status:** ✅ Completado (integrado y entrenado)

---

### R4: Entrenamiento del modelo [MVP]

**Mapea a la prueba:** *"Implementar el bucle de entrenamiento, incluyendo una función de
pérdida adecuada (ej. BCELoss) y un optimizador."*

**Problema:** entrenar la red gestionando el desbalanceo y evitando la fuga de datos.
**Solución:** split estratificado (train/val/test), escalado ajustado solo con train,
`DataLoader`, bucle de épocas (`zero_grad` → `forward` → `loss.backward()` → `step`),
`BCEWithLogitsLoss` con `pos_weight` para penalizar más los fallos no detectados, y Adam.

Comportamiento esperado:
- CUANDO se entrena ENTONCES la pérdida de validación desciende y el modelo se guarda en `models/`.
- El escalado DEBE ajustarse SOLO con train (sin mirar validación/test).
- La pérdida DEBE ponderar la clase minoritaria (`pos_weight`) por el desbalanceo.

Criterios de aceptación:
- [ ] Bucle de entrenamiento en PyTorch (no `.fit()` de sklearn).
- [ ] `BCEWithLogitsLoss` + Adam + `pos_weight`.
- [ ] Modelo y scaler guardados; semilla fija para reproducibilidad.

🔗 **Tasks:** tasks.md Fase 3
📊 **Status:** ✅ Completado y verificado en ejecución

---

### R5: Evaluación con métricas adecuadas [MVP]

**Mapea a la prueba:** *"Mostrar métricas de precisión, recall y la matriz de confusión."*

**Problema:** en un problema desbalanceado la *accuracy* engaña (un modelo que nunca predice
fallo acierta el 82%). Hay que medir lo que importa: no perder fallos (recall).
**Solución:** informe con precision, recall, F1 y matriz de confusión, **interpretados en
términos de negocio** (un falso negativo = servidor que cae sin aviso).

Comportamiento esperado:
- CUANDO se evalúa sobre test ENTONCES muestra precision/recall/F1 + matriz de confusión.
- El informe DEBE priorizar y explicar el recall de la clase "fallo".

Criterios de aceptación:
- [ ] Precision, recall, F1 y matriz de confusión sobre test.
- [ ] Interpretación de falsos negativos/positivos en contexto.
- [ ] Recall de la clase "fallo" en rango objetivo (~0.80-0.92).

🔗 **Tasks:** tasks.md Fase 4
📊 **Status:** ✅ Completado y verificado en ejecución

---

### R6: Interfaz interactiva de uso [B]

**Mapea a la prueba:** *"un ejemplo de uso de dicha solución"* (elevado a interfaz real).

**Problema:** un modelo en un notebook no lo usa nadie. Hay que poder *usarlo*.
**Solución:** panel Streamlit con sliders de los 4 sensores → predicción de probabilidad de
fallo en vivo (indicador verde/ámbar/rojo), pestaña con las métricas del modelo, y el panel
de diagnóstico (R7) cuando hay anomalía.

Comportamiento esperado:
- CUANDO el usuario ajusta los sensores ENTONCES la app predice la probabilidad al instante.
- CUANDO la probabilidad supera el umbral ENTONCES se muestra alerta + diagnóstico (R7).

Criterios de aceptación:
- [ ] App Streamlit funcional que carga el modelo entrenado.
- [ ] Predicción en vivo con indicador visual.
- [ ] Pestaña de métricas del modelo.

🔗 **Tasks:** tasks.md Fase 5
📊 **Status:** ✅ Completado y verificado en ejecución

---

### R7: Diagnóstico con IA aplicada — RAG sobre manuales [B]

**Mapea a la prueba:** contexto *"miles de manuales técnicos"* + valor diferencial del perfil
(IA aplicada / LLMs / RAG).

**Problema:** detectar el fallo no basta; el técnico necesita la causa y la acción. Ese
conocimiento vive en los manuales.
**Solución:** asistente RAG que, dada una anomalía y sus valores, recupera el manual más
relevante (búsqueda por similitud) y genera diagnóstico + recomendación en lenguaje natural.
Funciona con un LLM si hay clave de API; si no, degrada a una respuesta basada en el manual
recuperado (ejecutable por cualquiera).

Comportamiento esperado:
- CUANDO hay anomalía ENTONCES recupera el manual pertinente y devuelve causa + acciones.
- CUANDO no hay clave de LLM ENTONCES usa un generador de respaldo basado en reglas + manual.
- El sistema NO DEBE inventar acciones fuera de los manuales (respuesta anclada al contexto).

Criterios de aceptación:
- [ ] Base de manuales técnicos (markdown) sobre causas de fallo.
- [ ] Recuperación del manual relevante según la anomalía.
- [ ] Diagnóstico en lenguaje natural anclado al manual (con y sin LLM).

🔗 **Tasks:** tasks.md Fase 6
📊 **Status:** ✅ Completado y verificado en ejecución

---

## Implementación

### Componentes Principales

**Generador de datos** (`src/generate_data.py`) — simula telemetría con física realista;
fuente única del esquema de features. Ya implementado y verificado.
- Responsabilidad: producir `data/sensors.csv` reproducible.
- Afecta a: train, eda, evaluate (todos consumen su esquema de columnas).

**Modelo** (`src/model.py`) — `AnomalyMLP(nn.Module)`, red densa `4→32→16→1`. Ya implementado.
- Responsabilidad: definir la arquitectura de la red.
- Afecta a: train (la entrena), predict y dashboard (la cargan).

**Entrenamiento** (`src/train.py`) — split estratificado + `StandardScaler` (solo train) +
`DataLoader` + bucle PyTorch + `BCEWithLogitsLoss(pos_weight)` + Adam. Guarda modelo y scaler.

**Evaluación** (`src/evaluate.py`) — `classification_report` + `confusion_matrix` de sklearn
(solo para MÉTRICAS; el modelo es PyTorch) + interpretación.

**Inferencia** (`src/predict.py`) — carga modelo + scaler, aplica `torch.sigmoid` al logit,
devuelve probabilidad de fallo. Es el "ejemplo de uso" que pide la prueba.

**IA aplicada** (`src/rag_advisor.py`) — recuperación sobre `manuals/` + generación LLM con
respaldo. Capa diferencial.

**Interfaz** (`app/dashboard.py`) — Streamlit; orquesta predicción + diagnóstico en vivo.

### Flujo de Datos

```
generate_data.py → data/sensors.csv
                        │
        ┌───────────────┼────────────────┐
     eda.py         train.py  ──────►  models/sentinel_model.pt + scaler.joblib
   (reports/)           │                    │
                    evaluate.py          predict.py ◄── lectura nueva de sensores
                  (métricas + matriz)         │
                                          rag_advisor.py (si anomalía → manual → diagnóstico)
                                              │
                                        app/dashboard.py (interfaz)
```

### Decisiones de diseño clave

1. **MLP, no LSTM:** cada lectura se clasifica de forma independiente (tabular); el MLP es más
   simple, interpretable y mantenible. El LSTM correspondería a predecir el fallo desde la
   *evolución* temporal — anotado como trabajo futuro.
2. **`BCEWithLogitsLoss` en vez de `Sigmoid + BCELoss`:** numéricamente más estable (la prueba
   sugería `BCELoss`; esta es la práctica recomendada equivalente).
3. **`pos_weight` por el desbalanceo:** penaliza más no detectar un fallo → sube el recall, la
   métrica que importa en detección de anomalías.
4. **Escalado sin fuga de datos:** el `StandardScaler` se ajusta solo con train.

---

## Estándares de Calidad

- [ ] El pipeline completo se ejecuta de principio a fin sin errores (`generate → train → evaluate`).
- [ ] Reproducibilidad total (semilla fija, `requirements.txt`, instrucciones en README).
- [ ] Migas de pan en cada archivo de código Python.
- [ ] Código legible y comentado (el evaluador debe entenderlo sin ejecutar).
- [ ] Recall de la clase "fallo" en rango objetivo.
- [ ] Interfaz y asistente RAG funcionales.
- [ ] FILE STRUCTURE de este spec.md coincide con los archivos reales.
- [ ] Cross-references triangulares: spec ↔ tasks ↔ work_prepend.
- [ ] **Ambigüedad cero**: 0 markers `[NEEDS CLARIFICATION]` sin resolver.

---

## 📊 Métricas de Éxito

| Métrica | Actual | Target | Verificación |
|---------|--------|--------|--------------|
| Tasa de fallo del dataset | 16.8% ✅ | 10-20% (realista) | generate_data.py |
| Recall clase "fallo" (test) | 0.87 ✅ | ≥ 0.80 | evaluate.py |
| Pipeline reproducible | ✅ | 0 errores extremo a extremo | ejecución limpia (6/6) |
| Entregables de la prueba | 4/5 | 5/5 | falta solo el vídeo |

---

## 🔄 Delta Log (Cambios a Requirements)

### [2026-07-06] Creación inicial
- **ADDED** R1-R5: Requisitos que mapean 1:1 con los cinco puntos de la prueba técnica
  (generación de datos, EDA, arquitectura de red, entrenamiento, evaluación).
- **ADDED** R6: Interfaz interactiva (Streamlit) — eleva el "ejemplo de uso" pedido a una
  herramienta usable real. Diferenciador.
- **ADDED** R7: Capa de IA aplicada (RAG sobre manuales) — diferenciador de perfil; aprovecha
  el contexto "miles de manuales técnicos" de la prueba para demostrar IA aplicada.
- Razón: cumplir estrictamente lo pedido (R1-R5) y añadir valor alineado con el perfil (R6-R7)
  sin desviar el foco del núcleo evaluado.

---

🔗 **Triángulo SPEC 2.1:**
- spec.md ↔ tasks.md (R1-R7 se implementan en las Fases 1-6)
- tasks.md ↔ work_prepend.md (las fases se ejecutan y se registran en LIFO)
- work_prepend.md ↔ spec.md (los cambios de requirements se anotan en el Delta Log)
