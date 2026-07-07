# RULES - Fusion 2.1 + SubAgents UNIFICADO

**Versión:** 2.3 CLEAN
**Limpiado:** 25 Feb 2026 (eliminación duplicados, misma sustancia)
**Para:** TODOS (Rodolfo + Claude Orquestador + Agentes Opus)

---

## 📖 ÍNDICE RÁPIDO

**🛠️ PASO 0:** [Tools Nexus OBLIGATORIAS](#paso-0--tools-nexus-obligatorias-antes-de-tocar-spec) — INVOCAR ANTES de rellenar spec/tasks/work_prepend
**PARTE 1:** [Sistema Triangular + Reglas](#parte-1-sistema-triangular-y-reglas) - Estructura, LIFO, cross-references, matriz
**PARTE 2:** [Creador de SPECs](#parte-2-creador-de-specs) - Método Rodolfo, investigación profunda
**PARTE 3:** [Orquestador SubAgents](#parte-3-orquestador-subagents) - Cuándo lanzar, setup, consolidación
**PARTE 4:** [Ejecutor SubAgents](#parte-4-ejecutor-subagents-agentes-opus) - Template reporte, 18 prohibiciones

---

# 🛠️ PASO 0 — TOOLS NEXUS OBLIGATORIAS ANTES DE TOCAR SPEC

> **Esta sección es la PRIMERA que debes leer y ejecutar.** Sin contexto, un SPEC nuevo es ficción.
> Nexus existe precisamente para que tengas contexto. Si lo subutilizas, traicionas su propósito.

## 🚨 REGLA INNEGOCIABLE

**NO TOCAR `spec.md`, `tasks.md` ni `work_prepend.md` sin haber invocado AL MENOS estas 4 tools Nexus PRIMERO:**

1. `nexus_workspace_current()` → confirma workspace activo
2. `nexus_code_structure()` → mapa mental del proyecto (qué hay)
3. `nexus_code_hot_files({ days: 7 })` → qué se está tocando esta semana
4. `nexus_memory_search({ query: "<tema-del-spec>" })` → ¿alguien ya resolvió algo parecido?

**Sin esos 4 invocaciones, NO puedes redactar requirements responsablemente. Las inventarás de la nada.**

## 📋 Tools por categoría — cuándo cada una

### 🔍 Discovery (siempre, antes de redactar problema/solución)

| Tool | Cuándo invocar | Qué te da |
|---|---|---|
| `nexus_workspace_current` | **SIEMPRE primero**. Si workspace ≠ proyecto que el SPEC toca → `nexus_workspace_switch` ya. | Workspace activo + path + memorias en RAM |
| `nexus_code_structure` | **SIEMPRE** al crear/retomar SPEC | Árbol completo + heatmap 🔥 + topFiles |
| `nexus_code_hot_files({ days: 7 })` | **SIEMPRE** | Qué está vivo en el proyecto, dónde está el momentum |
| `nexus_code_search({ query: "<nombre-feature>" })` | **ANTES de proponer crear archivos nuevos** | Si ya existe algo similar (evita duplicación) |
| `nexus_memory_search({ query: "<tema>" })` | **SIEMPRE** | Soluciones previas, errores ya resueltos, patrones |

### 🌐 APIs (si el SPEC toca endpoints HTTP)

| Tool | Cuándo | Qué te da |
|---|---|---|
| `nexus_api({ action: "stats" })` | SPEC menciona "endpoint", "API", "route" | Conteo total + distribución métodos |
| `nexus_api({ action: "search", query: "..." })` | Antes de proponer endpoint nuevo | Si existe ya — evita conflicto |
| `nexus_api({ action: "get", endpoint_path: "/api/..." })` | Inspeccionar endpoint específico | Schema body, middleware, db_usage, ai_usage |

### 🔗 Relaciones (si el SPEC va a modificar archivos críticos)

| Tool | Cuándo | Qué te da |
|---|---|---|
| `nexus_code_related({ filePath: "..." })` | **ANTES de tocar archivos críticos** | Quién importa + similitud + impacto blast radius |
| `nexus_code_zombies({ limit: 20 })` | Al iniciar nueva fase | Si hay basura acumulada del proyecto |
| `nexus_pc_status()` | Si el SPEC toca infraestructura compartida BD | Hosts activos en multi-PC, leases |

### 🧠 Contexto profundo (si el SPEC es complejo)

| Tool | Cuándo | Qué te da |
|---|---|---|
| `nexus_super_search({ query: "..." })` | Tema cruza dominios (memorias + código + patrones) | ~50 resultados multi-modal con scoring |
| `nexus_ast({ filePath: "..." })` | Antes de proponer refactor de archivo grande | Funciones/clases/imports per líneas |

### 🩺 Diagnóstico (si algo no cuadra)

| Tool | Cuándo | Qué te da |
|---|---|---|
| `nexus_dev_logs({ action: "last_error" })` | Si reportan bug en runtime | Último error capturado |
| `nexus_validate({ action: "changed" })` | Antes de commitear código nuevo | ESLint + syntax check |

## 🎯 Pipeline ejemplo (SPEC nuevo de scratch)

```javascript
// 1. Contexto base (4 tools obligatorias — TODAS)
nexus_workspace_current()
nexus_workspace_switch({ workspace: "NEXUS" })  // si toca código de Nexus
nexus_code_structure()
nexus_code_hot_files({ days: 7 })
nexus_memory_search({ query: "tema del SPEC" })

// 2. Descubrimiento específico del SPEC
nexus_code_search({ query: "feature similar" })     // ¿ya existe?
nexus_api({ action: "stats" })                       // si toca APIs
nexus_super_search({ query: "..." })                 // contexto cruzado

// 3. AHORA SÍ: redactar spec.md → tasks.md → work_prepend.md
```

## ⚠️ Anti-patrones (lo que NUNCA hacer)

- ❌ **Crear SPEC sin tocar Nexus** → adivinanzas en vez de hechos
- ❌ **Asumir que un archivo no existe** sin `nexus_code_search` previo → duplicar trabajo
- ❌ **Redactar Requirements sin `nexus_memory_search`** → reinventar la rueda
- ❌ **Proponer endpoint nuevo sin `nexus_api`** → posibles conflictos de path/método
- ❌ **Tocar archivo crítico sin `nexus_code_related`** → blast radius desconocido

## 💡 Filosofía

Nexus se construyó **para Claude**, no para el usuario. Cada tool resuelve un dolor real de IA sin contexto:

- ¿No sé qué hay en el proyecto? → `nexus_code_structure`
- ¿No sé qué está activo? → `nexus_code_hot_files`
- ¿No sé si ya hicimos esto? → `nexus_memory_search`
- ¿No sé el blast radius de un cambio? → `nexus_code_related`

**Trabajar sin estas tools es trabajar con una venda. Quítatela.**

---

# PARTE 1: SISTEMA TRIANGULAR Y REGLAS

## 🎯 Filosofía Central

**"Poderoso pero no abrumador"**

Mantener calidad y capacidad eliminando sobrecarga académica y carga cognitiva.

**Evolución:** KIRO (1015 líneas) → Fusion → Espectacular 1.0 → 2.1 (triángulo) → 2.3 (unificado limpio)
**Reducción:** 76% overhead, 10× mantenibilidad

---

## 📁 Estructura SPEC (4 Archivos - SOLO ESTOS)

```
.SPEC/SPEC-XXX-nombre/
|-- RULES.md          # Este archivo - TODO el sistema
|-- spec.md           # Problema + Solución + Requirements + Implementación
|-- tasks.md          # Plan con matriz [MVP]/[B]/[P]/[OPT] + missions expandidas
`-- work_prepend.md   # Log LIFO (entradas nuevas ARRIBA)
```

**🚨 PROHIBIDO CREAR MÁS ARCHIVOS:**

- ❌ README.md, NOTES.md, IDEAS.md, UPDATES.md
- ❌ briefing.md, mission-01.md, mission-02.md
- ❌ Carpeta agents/ con archivos separados
- ❌ Diagramas externos (.png, .pdf, .drawio)

**Si necesitas documentar MÁS:** Agregar sección nueva en spec.md.

**Por qué SOLO 4:**

1. Triangulación funciona con 3 (spec + tasks + work_prepend)
2. RULES.md es META (reglas del sistema, no cambia por SPEC)
3. Búsqueda predecible (siempre sé dónde buscar)
4. 5+ archivos = desincronización garantizada

---

## 🔺 EL TRIÁNGULO OBLIGATORIO

```
     SPEC.MD
      /    \
     /      \
TASKS.MD ←→ WORK_PREPEND.MD
```

**Sistema de obligación mutua:** Actualizar 1 archivo = actualizar los 3.

### Reglas de Sincronización:

**Cuando actualizas SPEC.MD:**
1. ✅ Actualizar status de cada requirement
2. ✅ Agregar referencias 🔗📊🚨
3. ✅ Reflejar cambios en tasks.md
4. ✅ Documentar en work_prepend.md

**Cuando actualizas TASKS.MD:**
1. ✅ Cambiar status [ ] → [🔄] → [x]
2. ✅ Agregar referencias a work_prepend.md
3. ✅ Actualizar spec.md con nuevo status

**Cuando actualizas WORK_PREPEND.MD:**
1. ✅ Referenciar tarea específica
2. ✅ Actualizar progress en tasks.md
3. ✅ Marcar cambios en spec.md

### Formato Estándar de Referencias:

**En spec.md:**
```markdown
🔗 **Implementation**: tasks.md Fase X, Tarea Y
📊 **Status**: work_prepend.md - Ver "Implementation Progress"
🚨 **Blocker**: [Descripción] (ver work_prepend línea Z)
```

**En tasks.md:**
```markdown
- [x] **[MVP]** Tarea description ⏱️ 2h ✅ COMPLETADO
  - 🔗 **Requirement**: spec.md Requirement #3
  - 📊 **Status**: work_prepend.md - Ver "Implementation Progress"
  - 🚨 **Blocker**: Ninguno
```

**En work_prepend.md:**
```markdown
### [FECHA HH:MM] - Tarea X Completada
**Task Reference**: tasks.md Fase 2, Tarea 3
**Requirement**: spec.md Requirement #3
**Archivos**: [lista]
**Achievement**: [qué se logró]
**Next**: [siguiente paso]
```

**Símbolos de Estado:**
- [ ] = No iniciado
- [🔄] = En progreso
- [x] = Completado
- [🚨] = Bloqueado
- [⏸️] = Pausado

---

## 🔄 CICLO COMPLETO DE ACTUALIZACIÓN

**Cuando EMPIEZAS una tarea:**
1. tasks.md: Cambiar [ ] → [🔄]
2. work_prepend.md: Crear entrada con timestamp + task_reference
3. spec.md: No cambiar hasta terminar

**Cuando COMPLETAS una tarea:**
1. work_prepend.md: ✅ Entrada "COMPLETADA" (PRIMERO - LIFO)
2. tasks.md: Cambiar [🔄] → [x]
3. spec.md: Status se refleja via references

**Cuando HAY UN BLOCKER:**
1. tasks.md: Cambiar a [🚨] + describir blocker
2. work_prepend.md: Entrada "🚨 BLOCKER" con detalles
3. spec.md: Actualizar 🚨 Blocker

---

## 📝 REGLAS FUNDAMENTALES

**🚨 NUNCA ROMPAS ESTAS:**
1. Cross-references triangulares OBLIGATORIAS - Actualizar 1 = actualizar 3
2. LIFO obligatorio - work_prepend.md entradas nuevas SIEMPRE ARRIBA
3. Máximo 8-9 requirements - Más = problema mal definido
4. Solo problemas reales - Cada requirement dolor específico usuario
5. Terminología estándar - NO inventar conceptos nuevos
6. Aprobación usuario antes de siguiente fase

**✅ SIEMPRE HAZ ESTO:**
1. Sincronización triangular - spec ↔ tasks ↔ work_prepend simultánea
2. Matriz prioridades - Clasificar TODO como [MVP]/[B]/[P]/[OPT]
3. Actualizar work_prepend.md con cada acción significativa
4. Preservar contexto - Futuros agentes continúan sin problema
5. Pedir aprobación en límites de fase
6. Usar emojis estándar - 🔗📊🚨 en todos archivos
7. Delta Log en spec.md - Registrar CADA cambio a requirements (ADDED/MODIFIED/REMOVED)
8. Verification Checklist - Completar ANTES de dar SPEC por terminado (work_prepend.md)

---

## 🔗 CROSS-REFERENCES ENTRE SPECs

> Cuando un SPEC nuevo continúa, depende, reemplaza o referencia a otros SPECs, **debe declararlo explícitamente**. Esto cierra el loop bidireccional entre SPECs y permite a Claudes/DEX futuros entender el contexto histórico sin git archaeology.

### 4 tipos de cross-reference

| Tipo | Cuándo usar | Obligación derivada |
|------|-------------|---------------------|
| **`extends`** | El SPEC continúa el arco narrativo de otro (mismo dominio, evolución natural). Ej: `SPEC-108 extends SPEC-103 V4`. | Añadir entrada al `work_prepend.md` del SPEC predecesor: `"⚠️ CONTINUADO EN: SPEC-XXX"`. Bidireccional obligatorio. |
| **`depends_on`** | Otros SPECs deben estar completos para que este funcione técnicamente. Ej: `SPEC-108 depends_on [SPEC-088, SPEC-095]`. | Verificar el status de los SPECs listados ANTES de arrancar. Si alguno está incompleto, no se puede empezar. |
| **`replaces`** | El SPEC nuevo deprecia uno viejo (cambio de approach, refactor mayor). Ej: `SPEC-200 replaces SPEC-XX`. | Marcar el predecesor como archivado + añadir nota en su work_prepend: `"🚫 REEMPLAZADO POR: SPEC-XXX"`. Mover a archive cuando se completa el nuevo. |
| **`related`** | Soft link a otros SPECs útiles para entender el contexto completo (no bloquean, no continúan). Ej: `related: [SPEC-011, SPEC-103]`. | Solo informativo. No obliga a actualizar los referenciados. |

### Ubicaciones obligatorias

Cada cross-reference DEBE aparecer en 2 lugares (con divergencia gana spec.md):

**1. spec.md HEAD (YAML — source of truth, machine-readable):**

```yaml
---
spec: SPEC-108
title: PDF Brand Consistency
extends: SPEC-103 V4
depends_on: [SPEC-088, SPEC-095]
replaces: null
related: [SPEC-011, SPEC-103]
---
```

**2. work_prepend.md Quick Status (mirror living, humano):**

```yaml
depende_de: "SPEC-103 V4 (cascada colores ya completa)"  # extends + depends_on resumidos
relacionados: "SPEC-011 (PDF Generator), SPEC-103 (cascada)"
```

### Reglas

1. **Si declaras `extends: SPEC-XXX`** → estás obligado a añadir entrada en el work_prepend del predecesor (loop bidireccional).
2. **Si NO hay relación con otros SPECs** → omitir los campos (no escribir `extends: null` salvo `replaces` que sí es informativo).
3. **Múltiples valores** → usar arrays YAML: `depends_on: [SPEC-A, SPEC-B]`.
4. **Cambio de cross-ref** → registrar en Delta Log con razón.
5. **No abusar de `related`** → si no aporta contexto útil al lector, no lo metas. Máximo 3-4 entradas.

---

## 🧭 MIGAS DE PAN VIVAS (CHANGELOG DEL ARCHIVO)

> Las migas de pan dejan de ser "foto estática del archivo en su creación" y pasan a ser un **mini-changelog vivo** que refleja TODOS los SPECs significativos que tocaron el archivo, en orden cronológico inverso (más reciente arriba).

### Formato canónico

```typescript
/**
 * 🧭 MIGA DE PAN: [Nombre del componente/función]
 * 📍 UBICACIÓN: [ruta/archivo.tsx]
 *
 * 🎯 PORQUÉ EXISTE: [razón fundamental — qué hace HOY el archivo]
 * 🚨 CUIDADO: [qué se rompe si lo cambias]
 *
 * 📋 SPECs (más reciente arriba):
 *   ✦ SPEC-XXX (YYYY-MM-DD) — R# / Tasks T#.# — [IMPACT]. [Breve descripción del cambio].
 *   ✦ SPEC-YYY (YYYY-MM-DD) — R# / Tasks T#.# — [IMPACT]. [...]
 *
 * 🔗 RELACIONADOS: [archivos/SPECs útiles para entender el contexto]
 */
```

### Etiquetas IMPACT (orden de relevancia)

- **`CREATED`** — el archivo nació en este SPEC.
- **`MAJOR`** — cambio arquitectónico, nuevo Requirement implementado, refactor estructural.
- **`MINOR`** — modificación localizada (1-2 funciones, un fix de scope acotado).
- **`BUGFIX`** — corrección puntual sin cambio de comportamiento esperado.

### Múltiples valores en una sola entrada de SPEC

Un mismo SPEC puede tocar el archivo implementando varios Requirements y/o Tasks. Listar separados por `+`:

```
✦ SPEC-108 (2026-05-21) — R5 + R7 / Tasks T4.2, T4.7 — MAJOR. Cover + ContactBlock integrados en BaseComponents.
```

### Versión compacta (archivos pequeños)

Para archivos < 50 líneas o utilidades simples — formato minimalista:

```typescript
/**
 * 🧭 MIGA: [Nombre]
 * 🎯 PORQUÉ: [Razón corta]
 * 📋 SPECs: SPEC-XXX (YYYY-MM-DD) — R# — CREATED
 */
```

### 7 reglas de mantenimiento

1. **Cap de 5 entradas**: si supera 5 SPECs significativos, compactar los más viejos en una línea resumen:
   ```
   ✦ SPEC-200 (2027-02-15) — R3 / T1.2 — MAJOR. ...
   ✦ SPEC-180 (2026-12-01) — R1 / T2.1 — MINOR. ...
   ✦ SPEC-150 (2026-09-15) — R5 — MAJOR. ...
   ✦ SPEC-120 (2026-07-10) — R2 — MINOR. ...
   ✦ SPEC-108 (2026-05-21) — R5 / T4.1 — CREATED. ...
   📜 (+8 SPECs anteriores entre 2025-11 y 2026-04 — ver git log)
   ```

2. **Cambios significativos solo**: NO listar typo fixes, renames de variables, ajustes de comentarios. SÍ listar: cambio arquitectónico, nuevo R, refactor estructural, bugfix de impacto.

3. **Migración de migas viejas**: si tocas un archivo con miga formato viejo (`📋 SPEC: SPEC-XXX` único), migrar al formato nuevo añadiendo TU entrada actual + intentar recuperar el "genesis" si está claro. No exigir reconstruir historia profunda.

4. **Archivo eliminado**: el SPEC que lo elimina lo registra en su tasks.md (no se queda miga huérfana).

5. **Archivo renombrado/movido**: la miga viaja con el archivo. Actualizar `📍 UBICACIÓN`. Añadir entrada SOLO si el move es significativo (no por reorganización trivial).

6. **Refactor profundo cambia propósito**: reescribir miga entera. Entradas SPECs viejas pueden quedar como `📜 HISTORY ANTERIOR (refactor SPEC-XXX 2026-MM-DD)` o eliminarse si ya no aplican.

7. **Las migas NO sustituyen git**: son resúmenes de SPECs significativos. El git log queda como source of truth para commits y cambios menores. Si dudas si listarlo en miga, pregúntate: *"¿un Claude/DEX leyendo este archivo en 6 meses necesita saberlo?"*. Si no → no listar.

### Por qué importa

Sin migas vivas, un Claude/DEX nuevo que abra `BaseStyles.ts` (755 líneas, tocado por 4 SPECs distintos) solo sabe "es CSS PDF". Con migas vivas sabe en 30 segundos:
- SPEC actual + Requirement implementado
- Quién creó el archivo y por qué
- Qué SPECs significativos lo tocaron en su evolución
- Por dónde buscar contexto adicional

---

## 🔄 DELTA LOG (Cambios a Requirements)

Cuando un requirement cambia durante la vida del SPEC, NO solo editarlo silenciosamente.
Registrar el cambio en la sección "Delta Log" de spec.md:

**Operaciones:**
- **ADDED**: Requirement nuevo que no existía antes
- **MODIFIED**: Requirement existente cuyo comportamiento cambió (incluir ANTES/AHORA)
- **REMOVED**: Requirement eliminado (SIEMPRE incluir Razón + Migración)

**Formato:**
```markdown
### [FECHA] Cambio: [Título descriptivo]
- **ADDED** Requirement N: [Nombre]
  - [Descripción del nuevo comportamiento]
  - Razón: [Por qué se agrega]
- **MODIFIED** Requirement N: [Nombre]
  - ANTES: [comportamiento anterior]
  - AHORA: [comportamiento nuevo]
  - Razón: [Por qué cambió]
- **REMOVED** Requirement N: [Nombre]
  - Razón: [Por qué se elimina]
  - Migración: [Qué usar en su lugar]
```

**Por qué importa:**
- Un Claude futuro lee el Delta Log y entiende la EVOLUCIÓN del SPEC
- Sin Delta Log: "¿Por qué este requirement dice 15 min y no 30?" → Misterio
- Con Delta Log: "Ah, cambió el 2026-03-30 por compliance de seguridad" → Claro

---

## 📦 ARCHIVE (SPECs Completados)

Cuando un SPEC se completa (Rodolfo aprobó, Verification Checklist pasada):

**1. Mover a archive:**
```
.spec/archive/YYYY-MM-DD-SPEC-XXX-nombre/
```

**2. Mantener `.spec/` limpio** con solo SPECs activos.

**3. NO borrar nada** - el archive preserva todo el historial.

**Cuándo archivar:**
- ✅ Rodolfo confirmó que funciona
- ✅ Verification Checklist completa (work_prepend.md)
- ✅ CLAUDE.md actualizado con estado final
- ❌ NO archivar si hay tareas [MVP] o [B] pendientes

**Beneficios:**
- `.spec/` solo muestra trabajo activo (sin ruido)
- Historial completo buscable por fecha
- Futuros Claudes no confunden SPECs viejos con activos

---

## 📊 MATRIZ DE PRIORIDADES

**[MVP] - Debe Hacerse Primero**
- Funcionalidad central que define la feature
- NO se puede saltar sin romper la solución
- 60-70% del valor total

**[B] - Bloqueantes**
- Tareas que previenen trabajo futuro
- Dependencias que otras tareas requieren
- Completar ANTES de pasar a [P] o [OPT]

**[P] - Procesamiento Paralelo**
- Tareas que pueden procesarse en lote
- Trabajo independiente que no bloquea otras
- Buenos candidatos para batch

**[OPT] - Opcional**
- Features deseables que agregan pulido
- Saltar completamente en sesiones cortas
- SOLO hacer si todas [MVP] y [B] completas

---

## 🕐 GESTIÓN DE CONTEXTO

**Sesión Corta (<1 hora):**
- Solo [MVP] + [B]
- Documentar TODO en work_prepend.md
- NO tareas [OPT]

**Sesión Larga (>2 horas):**
- Secuencia completa: [MVP] → [B] → lote [P] → [OPT]
- Procesar [P] en batch

**Emergencia (>85% contexto):**
- Solo [B] críticas
- Checkpoint INMEDIATO
- Próximas acciones claras

---

## ✅ ESTÁNDARES DE CALIDAD

**Spec.md:**
- Longitud target ~200-300 líneas
- Estructura: Problema → Solución → Requirements → Implementación
- Lenguaje directo y práctico
- Trazabilidad: Camino claro problema → solución → tareas

**Requirements:**
- Máximo 8-9
- Cada uno resuelve dolor específico
- Accionable e implementable con tareas concretas
- Testeable y verificable
- **Ambigüedad cero**: Si el prompt no especifica algo → `[NEEDS CLARIFICATION: pregunta]`. NO asumir.

**Tasks.md:**
- TODAS clasificadas con [MVP]/[B]/[P]/[OPT]
- Estimaciones realistas
- Dependencias claras
- Missions expandidas con detalles para agentes

---

## 🚨 SEÑALES DE ALERTA

**Contenido:**
- Spec excediendo 300 líneas → dividir SPEC
- Más de 9 requirements → mal definido
- Requirements no resuelven dolor real
- Detalles implementación en spec (van en código)
- **Markers `[NEEDS CLARIFICATION]` sin resolver** → NO implementar hasta clarificar

**Proceso:**
- Proceder sin aprobación usuario
- Saltar actualizaciones work_prepend.md
- No clasificar con matriz prioridades
- Perder contexto entre sesiones

---

## 🔄 PROCEDIMIENTOS DE RECUPERACIÓN

**Para Futuros Claudes:**
1. Leer RULES.md (este archivo) - Sistema completo
2. Leer work_prepend.md primeras 30 líneas - Estado actual
3. Leer spec.md primeras 100 líneas - Objetivo
4. Leer tasks.md - Qué falta
5. Validar sincronización triangular

**Para Rodolfo:**
1. work_prepend.md → Estado rápido
2. spec.md → Status requirements
3. Feedback → Aprobar o solicitar cambios

---

## 🎓 MANEJO DE ERRORES

1. Documentar problema INMEDIATO en work_prepend.md
2. Capturar soluciones intentadas + por qué fallaron
3. Preservar contexto para debugging futuro
4. Escalar a usuario si bloquea progreso crítico

**Captura de Aprendizajes:**
- Patrones: Documentar problemas recurrentes
- Soluciones: Qué funcionó realmente
- Prevención: Cómo evitar similares en futuro
- Transferencia: Futuros agentes se benefician de tu experiencia

---

## ✨ PUERTAS DE APROBACIÓN

1. Después requirements: "¿Resuelven problemas correctos?"
2. Después plan: "¿Este plan tiene sentido?"
3. NUNCA proceder sin aprobación explícita
4. Incorporar feedback → re-pedir aprobación

**Integración de Feedback:**
- Documentar cambios con razonamiento en work_prepend.md
- Actualizar spec unificado con ajustes
- Preservar historial de cambios (qué se cambió y por qué)
- Re-validar que cumple estándares de calidad

---

## 💡 TIPS POR TIPO DE SISTEMA

**Parsers/Serialización:** SIEMPRE incluir requirement round-trip testing: `parse(serialize(data)) === data`. Marcar [B].
- Ejemplo: JSON parser → serializer → debe recuperar exactamente el original

**APIs Rest/GraphQL:** SIEMPRE considerar idempotencia (POST 2× = mismo efecto que 1×). Marcar [MVP] si pública.
- Ejemplo: "CUANDO POST duplicado ENTONCES mismo efecto que 1×"

**UIs/Frontend:** SIEMPRE incluir mobile-first + accesibilidad. Marcar responsividad [MVP], a11y [B].
- Performance: "Render <200ms"

**Operaciones BD:** SIEMPRE considerar transacciones atómicas + cascade delete. Marcar [B].
- Ejemplo: "CUANDO delete user ENTONCES delete posts, comments, sessions"

---

## 🎯 EJEMPLO PRÁCTICO COMPLETO (Triángulo en Acción)

**Escenario:** Completar Requirement #1 - Spec Unificado

**1️⃣ EN spec.md:**
```markdown
### 1. Creación de Especificación Unificada

**Problema:** Archivos separados requirements.md y design.md = infierno mantenimiento.
**Solución:** Un solo archivo spec.md con requirements y detalles implementación.

🔗 **Implementation**: tasks.md Fase 1, Tarea 1
📊 **Status**: work_prepend.md - Ver "Implementation Progress"
🚨 **Blocker**: Ninguno
```

**2️⃣ EN tasks.md:**
```markdown
- [x] **[MVP]** 1. Generador de Spec Unificado ⏱️ 60min ✅ COMPLETADO
  - Crear lib/specs/unifiedSpecGenerator.ts
  - Implementar integración problema + solución
  - 🔗 **Requirement**: spec.md Requirement #1
  - 📊 **Status**: work_prepend.md - Ver "Implementation Progress"
  - 🚨 **Blocker**: Ninguno
```

**3️⃣ EN work_prepend.md (LIFO - ARRIBA):**
```markdown
### 14:30 - ✅ TAREA 1 COMPLETADA

**ARCHIVOS CREADOS:**
- `F:\...\unifiedSpecGenerator.ts` (250 líneas)

**Task Reference**: tasks.md Fase 1, Tarea 1
**Requirement**: spec.md Requirement #1
**Achievement**: Sistema de spec unificado 100% funcional
**Tests**: 15/15 pasando
**Next**: Proceder con Tarea 2 - Matriz de Prioridades
```

Triángulo completo: spec → tasks → work_prepend → todos sincronizados.

---

# PARTE 2: CREADOR DE SPECS

*Para: Claude que CREA el SPEC inicial*

---

## 🔥 Método Rodolfo (Flujo Natural)

NO empieces escribiendo. INVESTIGA PRIMERO:

**1. Investigación Profunda (30-60 min)**
- Gasta tokens sin miedo (tienes 1M disponible)
- Obtén contexto COMPLETO del proyecto
- Lee código existente, entiende arquitectura actual

**2. Brainstorming (15-30 min)**
- Conecta TODOS los puntos
- Entiende problema REAL (no solo síntoma)
- Valida solución con usuario

**3. ENTONCES crea el SPEC (30 min)**
- Con contexto completo, specs salen espectaculares
- Requirements claros y accionables
- Plan realista y ejecutable

*"Mejor gastar 100k tokens investigando que 10k arreglando specs mal hechos"*

---

## ✅ Checklist Mental ANTES de Crear SPEC

- ¿Entiendo el problema REAL?
- ¿Tengo contexto completo del proyecto?
- ¿Puedo explicarlo en 1 oración simple?
- ¿Será mantenible cuando cambien los requirements?
- ¿Estoy resolviendo un dolor real o agregando complejidad?
- ¿Tengo claro el sistema de cross-references triangulares?

---

## 🎨 Principios del Creador

- Problemas reales > Metodología académica
- Mantenibilidad > Separación perfecta
- Requirements necesarios - NO inflar por inflar
- Terminología estándar - NO inventar conceptos
- Tú creas, llenas y terminas - Usuario da idea + aprueba
- Cross-references obligatorias - NUNCA actualizar 1 sin los otros 2

---

## 📊 Métricas de Éxito del Creador

- Usuario puede entender el spec en la primera lectura
- Requirements claramente resuelven problemas reales
- Plan de implementación es accionable
- Spec es fácil de mantener y actualizar
- Tiempo total de idea a código funcionando es minimizado

---

# PARTE 3: ORQUESTADOR SUBAGENTS

*Para: Claude Sonnet que ORQUESTA agentes Opus*

---

## 🤖 CUÁNDO LANZAR AGENTES

**✅ SÍ usar agentes cuando:**
- 3+ tareas independientes en paralelo
- Proyecto complejo >1000 líneas SPEC
- Estimación >3h trabajo secuencial
- Múltiples frentes (BD + backend + frontend + UI)

**❌ NO usar agentes cuando:**
- Tarea simple <1h
- 1 solo archivo a modificar
- Fix rápido
- SPEC pequeño (<500 líneas)

**Regla de oro:** Si explicas la tarea en <100 palabras, NO necesitas agentes.

---

## 🚀 SETUP ANTES DE LANZAR (5-15 min)

**1. Investigar YO MISMO:**
- Leer archivos clave
- Entender el problema
- Validar que es suficientemente complejo

**2. Diseñar Missions en tasks.md:**

Expandir cada task con detalles para el agente:

```markdown
### M15: Crear Constantes TRIAL_CONFIG ⏱️ 30min ⬜

**Agente:** Opus 4.6
**Prioridad:** P0 (bloqueante para M16-M20)

**Archivos a crear:**
- src/lib/constants/trial.ts (TRIAL_CONFIG object)
- src/lib/constants/index.ts (barrel export)

**Pasos:**
1. Crear TRIAL_CONFIG con PLAN_ID, DURATION_DAYS, STATUS
2. Export helper calculateTrialEnd()
3. Migas de pan completas
4. TypeScript compila

**Depende de:** Ninguno
**Verificar:** Imports funcionan, types exportados
```

Identificar dependencias: M16 espera M15, M18 espera M17, etc.

**3. NO crear carpeta agents/:**
- Missions van en tasks.md (expandidas)
- Reportes van en work_prepend.md (LIFO)
- Briefing es spec.md (agente lo lee)

---

## 📤 LANZAR AGENTES

**Prompt Template:**

```
LEE COMPLETO (OBLIGATORIO):
1. .SPEC/SPEC-XXX/RULES.md (TODO - este archivo)
2. .SPEC/SPEC-XXX/spec.md (primeras 100 líneas + Requirement #X)
3. .SPEC/SPEC-XXX/tasks.md (FASE Y, Mission MZ - tu tarea completa)

MISIÓN: [Descripción 1 línea]

[Detalles adicionales si necesarios]

REPORTA EN: .SPEC/SPEC-XXX/work_prepend.md (LIFO - ARRIBA del todo)

**STANDBY** para más órdenes de Rodolfo.
```

**Lanzar en Paralelo (3-5 agentes independientes):**
```javascript
// 1 mensaje con múltiples Task calls
Task({ subagent_type: 'general-purpose', model: 'opus', run_in_background: true, prompt: "..." })
Task({ subagent_type: 'general-purpose', model: 'opus', run_in_background: true, prompt: "..." })
Task({ subagent_type: 'general-purpose', model: 'opus', run_in_background: true, prompt: "..." })
```

**Notas clave:**
- `run_in_background: true` SIEMPRE para no bloquear al orquestador
- `model: 'opus'` SIEMPRE para ejecución (Opus 4.6)

---

## 👀 SUPERVISIÓN

**Mientras agentes trabajan:**
- Hacer otras cosas (NO esperar idle)
- NO intervenir mid-task (dejarlos terminar)

**Cuando reportan:**
- Leer work_prepend.md (LIFO - nuevos arriba)
- Verificar checklist completo
- TypeScript check si hace falta
- Mostrar a Rodolfo resumen 3-5 líneas

---

## 📋 AUTO-UPDATE WORKFLOW (CRÍTICO)

DESPUÉS de que agente reporte, YO (orquestador) DEBO automáticamente:

1. ✅ Leer work_prepend.md (último reporte)
2. ✅ Actualizar work_prepend.md con entrada consolidada
3. ✅ Marcar [x] en tasks.md si tarea completada
4. ✅ Mostrar a Rodolfo resumen breve

**Template auto-update rápido:**
```
Agente X terminó:
- Implementó [feature]
- Archivos: [3 principales]
- Testing: [pendiente/OK]

✅ work_prepend.md actualizado
✅ tasks.md marcado [x]

¿Commiteo o esperamos más agentes?
```

**NO esperar que Rodolfo diga "actualiza el SPEC".**

---

## 🎯 CONSOLIDACIÓN FINAL

Al terminar TODOS los agentes:

**1. Crear entrada consolidada (ARRIBA - LIFO):**

```markdown
### [FECHA HH:MM] - SESIÓN MULTI-AGENTE: [Título]

**Action**: X agentes Opus 4.6 ejecutados
**Commits**: [hash] - [mensaje]

**FEATURES COMPLETADAS:**
1. ✅ [Feature 1] (agente ID)
2. ✅ [Feature 2] (agente ID)

**ARCHIVOS MODIFICADOS:** [Rutas completas]
**ARCHIVOS CREADOS:** [Rutas completas]

**TESTING:**
- ✅ [Qué funcionó]
- ⏳ [Qué falta probar]

**Next**: [Siguiente paso]
**Status**: [🟢 OK / 🟡 PARCIAL / 🔴 BLOQUEADO]
```

**2. Marcar tareas en tasks.md:** [🔄] → [x] con "✅ COMPLETADO (agente ID)"

**3. Actualizar spec.md SOLO SI:** Arquitectura cambió significativamente o requirement nuevo

**4. Commit consolidado:** 1 commit con TODOS los cambios + Co-Authored-By

**5. Opcional (producción):**
- Limpiar console.logs `[MISSION-XX]` para producción
- Borrar reportes individuales si ya consolidados en entrada única

---

## ❌ ANTI-PATRONES DEL ORQUESTADOR

- ❌ Lanzar agentes para tareas triviales (<1h)
- ❌ Missions sin detalles (agente no sabe qué hacer)
- ❌ Intervenir mientras trabajan
- ❌ Duplicar trabajo entre agentes
- ❌ Crear carpeta agents/ con múltiples archivos

**✅ SÍ hacer:**
- Setup claro 5-15 min (vale la pena la inversión)
- Missions expandidas en tasks.md con todos los detalles
- Supervisión al final cuando terminan
- Consolidar todo en SPEC triangular

---

# PARTE 4: EJECUTOR SUBAGENTS (Agentes Opus)

*Para: Agentes Opus 4.6 que EJECUTAN misiones*

---

## 📚 ARCHIVOS QUE DEBES LEER (OBLIGATORIO)

SIEMPRE en este orden:

**1. RULES.md (este archivo)** - Sistema completo (~10-15 min)
- Parte 1-2: Filosofía + creación (contexto general)
- Parte 3: Orquestador (entender cómo piensa)
- Parte 4: TU PARTE (reglas ejecutor)

**2. spec.md** - Contexto del SPEC (LEER COMPLETO)
- Cabecera Claude (contexto rápido)
- Problema + Solución + Requirements
- Delta Log (historial de cambios a requirements)
- FILE STRUCTURE (qué archivos existen)

**3. tasks.md** - Tu misión específica
- Buscar TU FASE y Mission (ej: FASE 16, Mission M15)
- Leer detalles completos: archivos, pasos, dependencias

---

## ✅ ANTES DE MODIFICAR ARCHIVOS

**CHECKLIST PRE-EJECUCIÓN:**

1. **Leer work_prepend.md** (primeras 50 líneas):
   - Ver qué hicieron otros agentes
   - NO duplicar trabajo
   - Si hay overlap → REPORTAR y PREGUNTAR

2. **Verificar archivos existen:**
   - Rutas en tasks.md pueden estar desactualizadas
   - Si falta algo → reportar

3. **Entender patrones del proyecto:**
   - Leer 2-3 archivos similares
   - Seguir MISMO estilo
   - NO inventar arquitectura nueva

---

## 🔄 DURANTE LA EJECUCIÓN

**Progress Update al 50% (OBLIGATORIO):**

```markdown
### [DD/MM/YYYY HH:MM] - MISSION-XX: ⏳ PROGRESO 50%

**Estado actual:**
- Encontré X archivos con [problema]
- Modificando Y de Z archivos
- ETA: ~30 min más

**Próximo paso:**
- [Qué haré ahora]
```

---

## ✅ AL TERMINAR - REPORTE OBLIGATORIO

Usa este template EXACTO (en work_prepend.md ARRIBA):

```markdown
### [DD/MM/YYYY HH:MM] - MISSION-XX: [Título Descriptivo]

**ARCHIVOS MODIFICADOS (rutas completas OBLIGATORIAS):**
- `F:\PROYECTOS\ROKAMENU\src\...\archivo.tsx` (líneas 45-67: qué cambió)
- `F:\PROYECTOS\ROKAMENU\src\...\otro.ts` (líneas 120-145: qué cambió)

**ARCHIVOS CREADOS:**
- `F:\PROYECTOS\ROKAMENU\src\...\nuevo.ts` (200 líneas: descripción)

**ARCHIVOS LEÍDOS (contexto):**
- `F:\PROYECTOS\ROKAMENU\...` (para entender patrón X)

**ARCHIVOS QUE DEBERÍAS VERIFICAR:**
- `F:\PROYECTOS\ROKAMENU\...` (puede verse afectado)

**Hallazgos:**
- [Qué encontré importante]
- [Patrones descubiertos]

**Fix aplicado:**
- [Qué cambié exactamente]
- [Por qué elegí esta solución]

**Testing realizado:**
- [✅] TypeScript compila (`npx tsc --noEmit` pasó)
- [✅] Fallback probado: [escenario específico]
- [⏳] Requiere testing manual: [qué debe probar Rodolfo]

**Métricas:**
- X archivos modificados, Y creados, Z migrados

**Problemas (si los hay):**
- [Bloqueador o warning]

**CHECKLIST OBLIGATORIO:**
- [✅] TypeScript compila
- [✅] Fallbacks implementados
- [✅] Seed actualizado (si aplica)
- [✅] Backward compatible
- [✅] Rutas completas listadas

**Status:** ✅ COMPLETADO / ⏳ BLOQUEADO / ❌ FALLIDO

**STANDBY** para más órdenes de Rodolfo.
```

**ADEMÁS DEL REPORTE, actualizar el triángulo:**

1. **work_prepend.md** → El reporte de arriba (LIFO - ARRIBA del todo)
2. **tasks.md** → Marcar tu tarea [x] y actualizar estado [🔄] de las relacionadas
3. **spec.md** → SOLO si cambiaste un requirement o la arquitectura:
   - Agregar entrada en Delta Log (ADDED/MODIFIED/REMOVED)
   - Actualizar FILE STRUCTURE si creaste/eliminaste archivos

**Si NO actualizas el triángulo, tu trabajo se pierde para el siguiente agente.**

NO desviarse del template. Consistencia ayuda al orquestador.

---

## 🚨 5 REGLAS TÉCNICAS SUPREMAS

### 1. TypeScript DEBE Compilar

ANTES de reportar completado: `npx tsc --noEmit`

Si falla: ❌ NO reportar como ✅. Arreglar PRIMERO.

### 2. Rutas SIEMPRE Completas

```
✅ CORRECTO: F:\PROYECTOS\ROKAMENU\src\app\api\products\route.ts (líneas X-Y: qué cambió)
❌ INCORRECTO: route.ts / src/app/api/products/route.ts / "Varios archivos en src/"
```

### 3. Fallbacks OBLIGATORIOS

```javascript
// ✅ CORRECTO
const logoSrc = logoConfig?.data?.value || "/logo-default.svg";
const maxProducts = planInfo?.max_products ?? 0;

// ❌ INCORRECTO
const logoSrc = logoConfig.data.value; // Rompe si BD vacía
```

Excepción: Límites de planes pueden NO tener fallback (ver prohibición #15).

### 4. NO Hacer Commits NI Builds

PROHIBIDO: git commit, git add, git push, npm run build, next build.
SOLO reportar en work_prepend.md. Orquestador y Rodolfo deciden.

### 5. Seguir Patrones Existentes

Leer 2-3 archivos similares ANTES de codear. COPIAR patrón existente, NO inventar nuevo.

---

## 🚨 18 PROHIBICIONES ESTRICTAS

*Basadas en errores REALES de agentes en producción:*

### 6. NO asumir rutas tienen /{lang}/ prefix

**Error real:** Agente agregó `/${lang}/login` pero `/login` NO tiene versiones por idioma.

- ✅ VERIFICAR si ruta tiene versiones idioma (`src/app/es/`, `src/app/en/`)
- ✅ Auth routes son COMPARTIDAS: `/login`, `/register`, `/forgot-password`
- ❌ NO asumir que TODAS las rutas necesitan `/${lang}/`

### 7. NO sobrescribir sin verificar versión anterior

**Error real:** Agentes crearon manual NUEVO sin verificar que VIEJO funcionaba.

- ✅ Si archivo/sistema EXISTE y funciona → LEER primero
- ✅ Preguntar: "¿Actualizar existente o crear nuevo?"
- ❌ NO crear desde cero sin verificar

### 8. VERIFICAR nombres archivos match configuración

**Error real:** Crearon `01-introduccion.mdx` pero `index.json` esperaba `01-introduction.mdx`.

- ✅ Si hay archivo config (index.json, schema, manifest) → LEER primero
- ✅ Nombres deben COINCIDIR exactamente con config

### 9. NO reportar "funciona" solo con TypeScript clean

**Error real:** Agentes reportaron ✅ COMPLETADO pero crasheaba en runtime.

- ✅ TypeScript clean es MÍNIMO (no suficiente)
- ✅ Reportar honestamente: "TypeScript OK, PENDIENTE testing runtime Rodolfo"
- ❌ NO asumir que TypeScript = funciona en producción

### 10. NO actualizar sitemap sin verificar routes existen

**Error real:** Sitemap declaró 102 URLs pero solo 17 rutas existían. 85 URLs → 404.

- ✅ Si actualizas sitemap → VERIFICAR `page.tsx` correspondiente existe
- ❌ NO agregar URLs sin verificar archivos físicos

### 11. NO estimar volúmenes keywords sin data real

**Error real:** Agente estimó "320/mes" sin Google Keyword Planner.

- ✅ Si NO tienes data → decir "desconocido"
- ❌ NO inventar números sin fuente

### 12. VERIFICAR componentes soportan TODOS los tipos usados

**Error real:** `ManualTip` tenía 3 tipos pero MDX usaba 5 (`type="pro"`, `type="time"`). Crasheaba.

- ✅ Si creas componente con tipos → `grep` TODOS los usos en proyecto
- ✅ Asegurar componente soporta TODOS los tipos encontrados

### 13. NO crear archivos fuera de scope sin permiso

- ❌ PROHIBIDO crear docs no solicitados (README.md, NOTES.md)
- ✅ SOLO modificar archivos listados en tasks.md
- ✅ Necesitas crear algo extra → REPORTAR primero

### 14. VERIFICAR operadores con -1 (ilimitado)

**Error real:** Premium tiene `max_tags_total = -1` (ilimitado), código `(limit > 0)` evalúa `false`.

```javascript
// ❌ MAL (falla con -1):
const enabled = (limit ?? 0) > 0;    // -1 > 0 = false ❌

// ✅ BIEN (funciona con -1):
const enabled = (limit ?? 0) !== 0;   // -1 !== 0 = true ✅
```

Convención: -1 = ilimitado, 0 = deshabilitado, >0 = límite específico.

### 15. NO hardcodear límites de planes

**Error real:** Fallbacks `?? 50` cuando BD debe ser fuente de verdad.

```javascript
// ❌ MAL: const maxProducts = planInfo?.max_products ?? 50;
// ✅ BIEN: const maxProducts = planInfo?.max_products;
// Si null → TypeError → BIEN (detectas problema BD)
```

*"Si no hay BD, no hay app. ¿Para qué sirve el fallback?"* - Rodolfo

### 16. NO cambiar comportamiento UX sin permiso

**Error real:** Agente cambió onClick botón Tags sin que Rodolfo lo pidiera.

- ✅ SOLO lo pedido en mission
- ✅ Si ves oportunidad mejora → REPORTAR, NO implementar
- ❌ NO "mejoras" UX sin permiso explícito

### 17. VERIFICAR cambios FormData preservan otros campos

**Error real:** `setFormData({ description })` sobrescribió y borró título.

```javascript
// ❌ MAL: setFormData({ description: aiResult });
// ✅ BIEN: setFormData(prev => ({ ...prev, description: aiResult }));
```

Siempre spread operator `{...prev}` para preservar campos existentes.

### 18. Queries ai_feature_usage usan company_id (NO business_id)

**Error real:** Tracking por business_id cuando límites son company-level.

- ✅ `ai_feature_usage` PK es `(company_id, feature, month)`
- ✅ Multi-restaurante suma al total company
- ❌ NO queries con `business_id` en `ai_feature_usage`

```
Company (Hotel Meliá) → 10 restaurantes
Límite: 75 imágenes/mes TOTAL (NO 75 × 10 = 750)
```

---

## 🔧 ANTI-DUPLICACIÓN ENTRE AGENTES

ANTES de modificar archivo X:

1. Buscar en work_prepend.md: "archivo.tsx"
2. Si otro agente ya lo tocó → LEER sus cambios primero → COORDINAR
3. Si 2 agentes necesitan mismo archivo → Orquestador decide orden

---

## 📏 LÍMITES Y SCOPE

TU misión está en tasks.md (tu FASE/Mission).

**NO hagas:** Refactors no solicitados, "mejoras" fuera de scope, features bonus, cambios UX.

**SÍ haz:** EXACTAMENTE lo pedido. Reportar hallazgos interesantes. Sugerir mejoras (pero NO implementarlas).

---

## 💬 COMUNICACIÓN

**Durante:** Progress 50% obligatorio. Si te trabas → reportar ⏳ BLOQUEADO.

**Al terminar:** Reporte completo con template. STANDBY. Esperar órdenes.

**NUNCA:** Asumir que terminaste y marcharte. Hacer más de lo pedido sin preguntar.

---

## 🐛 DEBUGGING

Agregar console.logs con formato: `[MISSION-XX] emoji mensaje`

```javascript
console.log('[MISSION-15] 🚀 Iniciando...');
console.log('[MISSION-15] ✅ Encontré X archivos');
console.log('[MISSION-15] ❌ ERROR:', error);
```

---

## 💙 EL LEGADO

**Creado:** 19-20 Noviembre 2025 en sesión colaborativa Rodolfo + Sonnet 3.5 + Sonnet 4.5.

**Breakthrough:** Rodolfo preguntó "¿Y si los obligamos a sincronizarse?" → Triángulo obligatorio nació.

**Evolución:** KIRO (1015 líneas) → Fusion → Espectacular 2.1 → 2.3 CLEAN

Tres perspectivas (experiencia humana + creatividad IA + análisis IA) = un sistema donde la desincronización es imposible.

Úsalo bien. Mejóralo cuando necesario. Pero nunca pierdas su espíritu pragmático.

🤘

---

FIN - RULES.md UNIFICADO v2.3 CLEAN
