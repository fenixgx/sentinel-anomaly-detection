# Work Log - Sentinel (Detección de Anomalías) — LIFO Mode

<!--
🎯 LIFO = Last In, First Out — entradas nuevas ARRIBA.
📖 Recuperación rápida: head -50 work_prepend.md da todo el estado.
-->

<!--
╔══════════════════════════════════════════════════════════════════════════════════════╗
║ 🤖 CONTEXTO RÁPIDO                                                                    ║
║ 📍 QUÉ ES: Detector de anomalías en telemetría de servidores. Red neuronal (MLP en    ║
║    PyTorch) + capa de IA aplicada (RAG sobre manuales). Prueba técnica TechTitute.     ║
║ 🏗️ ARQUITECTURA: telemetría → red neuronal → ¿fallo? → RAG advisor → interfaz web.    ║
║ ⚠️ DEPENDENCIAS: PyTorch (CPU), pandas, scikit-learn, streamlit. Venv Python 3.12.     ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
-->

## 🎯 Quick Status

```yaml
timestamp: 2026-07-06 21:45
phase: "ENTREGABLE. Repo público + demo online desplegada y VERIFICADA en vivo. Falta solo: el vídeo"
current_task: "Grabar el vídeo (2 min) + enviar email de entrega"
next_action: "Rodolfo graba el vídeo con el guion; el email de entrega ya preparado"
context_used: "sesión larga"
blockers: none
breakthrough: "Demo online en Streamlit Cloud funcionando: predicción real, diagnóstico RAG, descargas, gráficas pro"
quality: "Demo verificada en vivo por Rodolfo (anomalía 41% detectada; descargas válidas por hash md5)"
rodolfo_approved: "demo SÍ (verificada en vivo); solo falta el vídeo para cerrar la entrega"
entregables_prueba: "generador ✅ · CSV ✅ · código ✅ · modelo entrenado ✅ · demo online ✅ · vídeo ⬜"
```

## 📈 Progress Tracker

🔄 **IMPLEMENTACIÓN EN PROGRESO — 2/11 tareas**

**Archivos del SPEC:**
✅ rules.md - Leído (NO modificar)
✅ spec.md - Completado (problema + solución + R1-R7 mapeados a la prueba)
✅ tasks.md - Completado (7 fases, 11 tareas)
🔄 work_prepend.md - Este archivo, actualizando

**Código:**
- ✅ `src/generate_data.py` — generador con lógica física (VERIFICADO en ejecución)
- ✅ `src/model.py` — clase `AnomalyMLP(nn.Module)` (escrito, aún no entrenado)
- ⬜ `src/eda.py` — análisis exploratorio
- ⬜ `src/train.py` — pipeline de entrenamiento
- ⬜ `src/evaluate.py` — métricas + matriz de confusión
- ⬜ `src/predict.py` — inferencia
- ⬜ `src/rag_advisor.py` — IA aplicada (RAG)
- ⬜ `app/dashboard.py` — interfaz Streamlit
- ⬜ `manuals/*.md` — base de conocimiento

**Fases:**
✅ Fase 1: Datos (1/1)
⬜ Fase 2: EDA (0/1)
🔄 Fase 3: Modelo + Entrenamiento (1/2 — arquitectura ✅, train ⬜)
⬜ Fase 4: Evaluación (0/2)
⬜ Fase 5: Interfaz (0/1)
⬜ Fase 6: IA aplicada RAG (0/1)
⬜ Fase 7: Empaquetado (0/3)

---

## 📜 Session Log (Newest First ⬆️)

### 21:45 - ✅ REPO + DEMO DESPLEGADOS Y VERIFICADOS EN VIVO

- **Action**: Repo público creado, demo desplegada en Streamlit Cloud, gráficas pulidas con
  tema profesional (skill dataviz), descargas en la barra lateral. Verificado en vivo por Rodolfo.
- **Task Reference**: tasks.md Fase 7 (T10 ✅)
- **Entregado / desplegado**:
  - Repo: https://github.com/fenixgx/sentinel-anomaly-detection (público)
  - Demo: https://sentinel-anomaly-detection.streamlit.app (Python 3.12, torch CPU)
  - Gráficas con tema consistente (color por trabajo: categórico / diverging / secuencial)
  - Descargas del dataset + modelo en la barra lateral (siempre visibles) + link al repo
- **Verificado por Rodolfo en vivo**:
  - Predicción real (anomalía 41% con CPU 69 → alerta roja + diagnóstico RAG)
  - Descargas: los dos .pt idénticos por md5 + coinciden con el del repo; CSV 8000 filas correcto
- **Decisión de seguridad**: la clave va en Streamlit Secrets (no en el repo); el dashboard
  propaga el secret a os.environ para que el RAG use el LLM.
- **Next**: Rodolfo graba el vídeo (2 min, guion aparte) + envía el email de entrega.
- **Status**: ✅ ENTREGABLE COMPLETO salvo el vídeo. Demo funcionando y verificada.

### 21:10 - ✅ DIFERENCIADORES + EMPAQUETADO COMPLETOS (R2, R6, R7)

- **Action**: Escritos y verificados el EDA, la interfaz Streamlit, la capa de IA aplicada (RAG)
  y el empaquetado. Pipeline completo verificado end-to-end (6/6). Proyecto listo para entregar.
- **Task Reference**: tasks.md Fase 2 (T2 ✅), Fase 5 (T7 ✅), Fase 6 (T8 ✅), Fase 7 (T9 ✅)
- **Requirement**: spec.md #R2 (✅), #R6 (✅), #R7 (✅)
- **Files Created**:
  - ✅ `src/eda.py` — correlaciones + distribuciones (verificadas visualmente)
  - ✅ `app/dashboard.py` — interfaz Streamlit (arranca, HTTP 200)
  - ✅ `src/rag_advisor.py` + `manuals/*.md` — RAG (retrieval TF-IDF + LLM opcional con respaldo)
  - ✅ `README.md`, `requirements.txt`, `pyproject.toml`, `.gitignore`
- **Verificación end-to-end**: generate → eda → train → evaluate → predict → rag = 6/6 sin errores.
- **Decisión de seguridad**: la API key NO va al repo (GitHub la revocaría + sería un red flag).
  El RAG degrada sin clave; el README documenta OPENAI_API_KEY como variable de entorno.
- **Next**: crear repo público + push. Luego guion del vídeo.
- **Status**: ✅ PROYECTO COMPLETO (R1-R7). Falta push del repo + vídeo.

### 20:45 - ✅ NÚCLEO ML COMPLETO Y VERIFICADO (R4 + R5)

- **Action**: Escrito y verificado el pipeline ML completo: entrenamiento, evaluación e inferencia.
- **Task Reference**: tasks.md Fase 3 (T4 ✅), Fase 4 (T5 ✅, T6 ✅)
- **Requirement**: spec.md #R4 (✅), #R5 (✅)
- **Files Created**:
  - ✅ `src/train.py` — split estratificado + StandardScaler (sin fuga) + DataLoader + bucle
    PyTorch (zero_grad→forward→backward→step) + BCEWithLogitsLoss(pos_weight) + Adam +
    calibración automática del umbral operativo
  - ✅ `src/evaluate.py` — classification_report + matriz de confusión + análisis de umbral +
    interpretación de negocio; guarda `reports/confusion_matrix.png`
  - ✅ `src/predict.py` — inferencia con caché (singleton); ejemplo de uso (sano/cargado/crítico)
- **Resultado en TEST (n=1200)**:
  - Recall clase fallo: 0.866 (174/201 fallos detectados, solo 27 perdidos)
  - Precisión: 0.455 · Accuracy: 0.804 · Umbral operativo calibrado: 0.25
  - predict.py: sano 3.6% 🟢 · cargado 99.4% 🔴 · crítico 100% 🔴
- **LOOP DE AJUSTE (3 iteraciones, todas verificadas en ejecución)**:
  1. Dataset con señal muy débil (corr ~0.15) → recall techo 0.66. Subí la señal física.
  2. pos_weight completo (5.3) → recall 0.82 pero precisión 0.38 (demasiado gritón). Usé la raíz.
  3. Umbral 0.5 a ciegas no era óptimo → calibración de umbral con política recall-first (dominio).
- **Next**: T2 (EDA), luego los diferenciadores T7 (dashboard Streamlit) + T8 (RAG advisor).
- **Status**: ✅ NÚCLEO ML (R1,R3,R4,R5) COMPLETO — falta EDA + interfaz + IA aplicada + empaquetado.
- **Quality Check**: pipeline verificado end-to-end en ejecución (no solo "compila").

### 20:05 - ✅ SPEC RELLENADO + GENERADOR Y MODELO LISTOS

- **Action**: Montado el entorno, creado y verificado el generador de datos, escrita la clase
  de la red, y rellenado el triángulo del SPEC (spec/tasks/work_prepend) con todo detallado.
- **Task Reference**: tasks.md Fase 1 (T1 ✅), Fase 3 (T3 ✅)
- **Requirement**: spec.md #R1 (✅), #R3 (✅)
- **Files Created**:
  - ✅ `src/generate_data.py` — generador de telemetría (verificado en ejecución)
  - ✅ `src/model.py` — `AnomalyMLP(nn.Module)`
  - ✅ `data/sensors.csv` — 8000 muestras
- **Entorno montado**:
  - venv con Python 3.12 (vía `uv`) + PyTorch 2.12.1 (CPU), pandas, scikit-learn, streamlit,
    matplotlib, seaborn, joblib. Todo importa OK.
  - Nota: el CDN CPU de PyTorch dio HandshakeFailure (red) → se instaló desde PyPI (funciona igual).
- **Implementation Details**:
  - 🔥 Primer intento del generador: correlaciones ~0 (umbrales de estrés demasiado altos, solo
    la cola extrema activaba señal). Detectado en el loop de verificación.
  - 🔧 Fix: estrés CONTINUO (cada sensor por encima de su valor normal suma) + interacción
    no lineal calor×CPU. Resultado: correlaciones con sentido (memoria +0.19, CPU +0.18,
    red +0.15, temp +0.11) y tasa de fallo 17.6% (desbalanceo realista).
- **Next**: T4 — escribir `src/train.py` y entrenar el modelo.
- **Status**: 🔄 FASE 3 EN PROGRESO (arquitectura lista, falta entrenamiento)
- **Quality Check**: generador verificado en ejecución; modelo pendiente de entrenar.

<!-- ⬆️⬆️⬆️ AGREGAR NUEVAS ENTRADAS ARRIBA DE ESTA LÍNEA ⬆️⬆️⬆️ -->

---

## 🚀 Key Innovations This Session

### 💡 Generador con lógica física (no random)
- **Qué se hizo**: la etiqueta de fallo se deriva de las features con una función de estrés
  continua + interacción no lineal (calor alto × CPU alta = sobrecarga térmica), no al azar.
- **Por qué importa**: el modelo aprende un patrón REAL; el dataset "tiene sentido" (como pide
  la prueba) y no es trivialmente separable (correlaciones 0.1-0.2 con ruido → recall realista).
- **Archivos**: `src/generate_data.py`
- **100% implementado**: Sí (verificado en ejecución).

### 💡 Dos capas: detección (red) + diagnóstico (IA aplicada RAG)
- **Qué se hizo**: además de la red que pide la prueba, una capa RAG que diagnostica la causa y
  recomienda la acción sobre los "manuales técnicos" del propio enunciado.
- **Por qué importa**: demuestra el perfil de IA aplicada del candidato al lado de lo pedido;
  convierte "algo va mal" en "esto pasa y esto debes hacer".
- **Archivos**: `src/rag_advisor.py` (pendiente), `manuals/*.md` (pendiente)
- **100% implementado**: No — planificado (R7 / Fase 6).

---

## 💡 Lessons Learned

### ✅ What Works
- **Loop de verificación**: ejecutar el generador y mirar las correlaciones cazó de inmediato
  que la señal era nula. Sin ejecutar, habría entrenado un modelo sobre ruido.
- **`uv` para el entorno**: instaló Python 3.12 + dependencias en minutos, aislado del sistema.

### ❌ What Doesn't Work
- **Umbrales de estrés solo en la cola extrema**: si el umbral está lejos de la media de la
  feature, casi ninguna muestra lo supera → correlación ~0 → modelo no aprende. Usar señal continua.

### 🎯 Success Factors
- **Datos con sentido físico**: la calidad del dataset determina si el modelo puede aprender algo.
- **Cumplir lo pedido + añadir valor alineado**: R1-R5 cubren la prueba al pie de la letra;
  R6-R7 (interfaz + IA aplicada) diferencian sin desviar el foco.

---

## ✅ Verification Checklist (Pre-Entrega)

### Completeness (¿Está todo?)
- [ ] Los 5 puntos de la prueba (R1-R5) implementados en código
- [ ] Tareas [MVP] de tasks.md marcadas [x]
- [ ] FILE STRUCTURE de spec.md coincide con archivos reales
- [ ] Los 5 entregables listos (generador, CSV, código, modelo entrenado, vídeo)
- [ ] 0 markers `[NEEDS CLARIFICATION]` sin resolver

### Correctness (¿Funciona bien?)
- [ ] Pipeline `generate → train → evaluate` corre sin errores
- [ ] Recall de la clase "fallo" en rango objetivo
- [ ] El modelo NO usa sklearn (solo PyTorch) — requisito explícito de la prueba
- [ ] Rodolfo probó y aprobó

### Coherence (¿Tiene sentido junto?)
- [ ] Migas de pan en cada archivo Python con referencia al SPEC
- [ ] Naming consistente entre spec.md y código
- [ ] README explica cómo ejecutar y qué se entrega
- [ ] Cross-references triangulares intactas (🔗📊🚨)

---

## 🔄 Recovery Instructions (para retomar)

1. Leer `rules.md` (reglas del sistema).
2. Este Quick Status → estado actual + próxima acción.
3. `spec.md` → problema, solución, R1-R7 (cada uno mapeado a la prueba).
4. `tasks.md` → matriz de prioridades, qué falta (siguiente: **T4 entrenamiento**).
5. Ejecutar con el intérprete del venv: `/home/fenix/proyectos/sentinel/.venv/bin/python`.

### Comandos verificados
```bash
# Regenerar dataset
/home/fenix/proyectos/sentinel/.venv/bin/python src/generate_data.py
```

---

## 📊 Metrics & Stats

- **Archivos de código creados**: 2 (generate_data.py, model.py)
- **Dataset**: 8000 muestras, 17.6% fallos
- **Tareas completadas**: 2/11 (T1 generador, T3 arquitectura)
- **Aprobaciones de Rodolfo**: 0 (pendiente)

---

**Created**: 2026-07-06
**Last Updated**: 2026-07-06 20:05
**Status**: 🔄 EN PROGRESO — Fase 3 (falta entrenamiento). Siguiente: T4.
**Cross-references**: spec.md ↔ tasks.md ↔ work_prepend.md (SINCRONIZADO)
