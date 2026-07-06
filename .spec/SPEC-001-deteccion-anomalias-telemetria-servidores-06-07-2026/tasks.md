# Plan de Implementación — Sentinel (Detección de Anomalías)

## Guía de Matriz de Prioridades

- **[MVP]** = Núcleo evaluado en la prueba (datos, EDA, red, entrenamiento, evaluación).
- **[B]** = Bloqueante / diferenciador de alto valor (interfaz, IA aplicada).
- **[P]** = Paralelo — empaquetado (README, migas, requirements, repo).
- **[OPT]** = Opcional — pulido (vídeo, extras).

## Estado global

**Núcleo + diferenciadores COMPLETOS y verificados end-to-end.** Falta: push del repo + vídeo.
Entregables de la prueba: **generador ✅ · CSV ✅ · código ✅ · modelo entrenado ✅ · vídeo ⬜**.

---

## FASE 1: Datos — Fundación (R1)

- [x] **[MVP]** T1. Generador de datos con lógica física ⏱️ 45min ✅ COMPLETADO
  - Distribuciones realistas + estrés continuo + interacción calor×CPU + ruido
  - Semilla fija → `data/sensors.csv` reproducible (8000 muestras, 16.8% fallos)
  - Requirement: spec.md #R1 · Verificado: correlaciones con sentido físico

## FASE 2: Análisis Exploratorio (R2)

- [x] **[MVP]** T2. Script de EDA ⏱️ 40min ✅ COMPLETADO
  - `reports/correlations.png` + `reports/distributions.png` (verificadas visualmente)
  - Conclusiones: desbalanceo → recall; escalado; split estratificado
  - Crea: `src/eda.py` · Requirement: spec.md #R2

## FASE 3: Modelo y Entrenamiento (R3, R4)

- [x] **[MVP]** T3. Arquitectura de la red (`nn.Module`) ⏱️ 30min ✅ COMPLETADO
  - `AnomalyMLP` 4→32→16→1, ReLU + Dropout, salida en logits
  - Crea: `src/model.py` · Requirement: spec.md #R3

- [x] **[MVP]** T4. Pipeline de entrenamiento ⏱️ 60min ✅ COMPLETADO
  - Split estratificado + StandardScaler (sin fuga) + DataLoader + bucle PyTorch
  - BCEWithLogitsLoss(pos_weight=√ratio) + Adam + **calibración de umbral (recall-first)**
  - Guarda `models/sentinel_model.pt` + `models/scaler.joblib`
  - Crea: `src/train.py` · Requirement: spec.md #R4

## FASE 4: Evaluación (R5)

- [x] **[MVP]** T5. Evaluación + matriz de confusión ⏱️ 40min ✅ COMPLETADO
  - classification_report + confusion_matrix + análisis de umbral + interpretación
  - `reports/confusion_matrix.png` · **recall 0.87 en test**
  - Crea: `src/evaluate.py` · Requirement: spec.md #R5

- [x] **[MVP]** T6. Script de inferencia (ejemplo de uso) ⏱️ 25min ✅ COMPLETADO
  - `predict_one()` con caché; ejemplos sano/cargado/crítico verificados
  - Crea: `src/predict.py` · Requirement: spec.md #R5

## FASE 5: Interfaz de uso (R6) — Diferenciador

- [x] **[B]** T7. Dashboard Streamlit ⏱️ 60min ✅ COMPLETADO
  - Sliders → predicción en vivo (verde/ámbar/rojo) + pestaña de métricas + diagnóstico RAG
  - Arranca sin errores (HTTP 200). Verificación visual: por Rodolfo en su navegador
  - Crea: `app/dashboard.py` · Requirement: spec.md #R6

## FASE 6: IA aplicada — RAG Advisor (R7) — Diferenciador

- [x] **[B]** T8. Base de manuales + RAG advisor ⏱️ 60min ✅ COMPLETADO
  - 4 manuales técnicos + retrieval TF-IDF/coseno + generación LLM con respaldo sin clave
  - Recupera el manual correcto en cada caso (verificado)
  - Crea: `src/rag_advisor.py`, `manuals/*.md` · Requirement: spec.md #R7

## FASE 7: Empaquetado y Entrega (Transversal)

- [x] **[P]** T9. README + reproducibilidad ⏱️ 40min ✅ COMPLETADO
  - README completo + requirements.txt + pyproject.toml + .gitignore + migas en todos los archivos

- [🔄] **[P]** T10. Repositorio GitHub ⏱️ 15min EN PROGRESO
  - Repo público `sentinel-anomaly-detection` (fenixgx) + commit + push

- [ ] **[OPT]** T11. Guion del vídeo (1.5-2 min)
  - 4 beats: problema → solución con criterio → cómo trabajo → cierre honesto

### Checkpoint Final
- [x] Pipeline completo corre de principio a fin sin errores (6/6 verificado)
- [x] README claro
- [🔄] Repo subido
- [x] Triángulo sincronizado (spec ↔ tasks ↔ work_prepend)
- [ ] Rodolfo revisó y aprobó la entrega
- [ ] Vídeo grabado

---

## Ruta Crítica — ESTADO

**Núcleo evaluado (MVP):** T1 ✅ → T2 ✅ → T3 ✅ → T4 ✅ → T5 ✅ → T6 ✅
**Diferenciadores (B):** T7 ✅ (interfaz) + T8 ✅ (IA aplicada)
**Empaquetado:** T9 ✅ · T10 🔄 (push) · T11 ⬜ (vídeo)

**10/11 tareas completadas.** Falta el push del repo y el vídeo.

---

**Triángulo SPEC:** spec.md ↔ tasks.md ↔ work_prepend.md (SINCRONIZADO)
