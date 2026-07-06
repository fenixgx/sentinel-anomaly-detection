"""
🧭 MIGA DE PAN: Asistente de diagnóstico con IA aplicada (RAG sobre manuales técnicos)
📍 UBICACIÓN: src/rag_advisor.py

🎯 PORQUÉ EXISTE: Es la CAPA DE VALOR sobre la red neuronal. La red dice "este servidor va a
   fallar"; este asistente dice "por QUÉ y qué HACER". Implementa un RAG clásico sobre los
   manuales técnicos (manuals/): recupera el manual más relevante para la anomalía detectada y
   genera un diagnóstico + recomendaciones en lenguaje natural.
🚨 CUIDADO:
   - Retrieval = TF-IDF + similitud coseno (100% local, sin dependencias externas). En
     producción se escalaría a embeddings + base vectorial (como en un RAG real), pero aquí se
     mantiene local para que el evaluador pueda ejecutarlo sin claves ni servicios.
   - Generación = LLM de OpenAI SI existe OPENAI_API_KEY; si no, degrada a una respuesta
     basada en el manual recuperado. La respuesta SIEMPRE está anclada al manual (no inventa).
📋 SPEC: SPEC-001-sentinel — R7 (IA aplicada / RAG) — CREATED
"""

from __future__ import annotations
import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
MANUALS_DIR = ROOT / "manuals"

# Umbrales que marcan un sensor como "elevado" (para construir la consulta de recuperación).
HIGH = {"temperature": 72, "cpu_usage": 78, "memory_usage": 82, "network_traffic": 650}

# Vocabulario por sensor -> se usa como consulta para el retrieval (términos que aparecen en
# los manuales). Cuanto mejor describa la anomalía, mejor recupera el manual pertinente.
QUERY_TERMS = {
    "temperature": "temperatura alta chasis sobrecalentamiento calor refrigeración ventiladores",
    "cpu_usage": "cpu saturada uso elevado cómputo procesos carga",
    "memory_usage": "memoria saturada uso alto swapping fugas ram",
    "network_traffic": "red saturación tráfico ancho de banda latencia",
}


def _load_manuals() -> list[dict]:
    """Carga los manuales técnicos (nombre + texto)."""
    manuals = []
    for path in sorted(MANUALS_DIR.glob("*.md")):
        manuals.append({"name": path.stem, "text": path.read_text(encoding="utf-8")})
    return manuals


def _build_query(reading: dict) -> str:
    """Construye la consulta de recuperación describiendo qué sensores están elevados."""
    parts = [QUERY_TERMS[s] for s, thr in HIGH.items() if reading.get(s, 0) >= thr]
    return " ".join(parts) if parts else "estado general del servidor"


def retrieve_manual(reading: dict) -> tuple[dict, float]:
    """
    Recupera el manual más relevante para la anomalía (TF-IDF + similitud coseno).
    Devuelve (manual, score de similitud 0-1).
    """
    manuals = _load_manuals()
    query = _build_query(reading)
    corpus = [m["text"] for m in manuals] + [query]
    tfidf = TfidfVectorizer().fit_transform(corpus)
    # Similitud de la consulta (última fila) contra cada manual.
    sims = cosine_similarity(tfidf[-1], tfidf[:-1]).ravel()
    best = int(sims.argmax())
    return manuals[best], float(sims[best])


def _fallback_diagnosis(reading: dict, manual: dict) -> str:
    """Respuesta sin LLM: resume el manual recuperado + los valores de la anomalía."""
    elevated = [f"{s}={reading[s]}" for s, thr in HIGH.items() if reading.get(s, 0) >= thr]
    elevated_txt = ", ".join(elevated) if elevated else "valores en rango"
    return (
        f"Anomalía detectada. Sensores elevados: {elevated_txt}.\n\n"
        f"Manual más relevante: «{manual['name'].replace('-', ' ')}».\n\n"
        f"{manual['text']}"
    )


def _llm_diagnosis(reading: dict, manual: dict) -> str | None:
    """
    Genera el diagnóstico con un LLM (OpenAI) usando el manual como contexto.
    Devuelve None si no hay clave o el paquete no está disponible (para degradar con gracia).
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI
    except ImportError:
        return None
    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            "Eres un técnico de sistemas. A partir de la lectura de sensores y del MANUAL "
            "TÉCNICO proporcionado, redacta un diagnóstico breve (2-3 frases) de la causa "
            "probable y una lista de 3 acciones concretas. Usa SOLO la información del manual; "
            "no inventes causas ni acciones que no aparezcan en él.\n\n"
            f"LECTURA DE SENSORES: {reading}\n\n"
            f"MANUAL TÉCNICO:\n{manual['text']}"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=350,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        # Cualquier fallo de red/API -> degradar al fallback (no romper el sistema).
        return None


def diagnose(reading: dict) -> dict:
    """
    Orquesta el RAG: recupera el manual relevante y genera el diagnóstico.
    Devuelve {'manual', 'score', 'diagnosis', 'source'}.
    """
    manual, score = retrieve_manual(reading)
    llm_text = _llm_diagnosis(reading, manual)
    if llm_text:
        return {"manual": manual["name"], "score": score, "diagnosis": llm_text, "source": "llm"}
    return {
        "manual": manual["name"],
        "score": score,
        "diagnosis": _fallback_diagnosis(reading, manual),
        "source": "plantilla",
    }


def main() -> None:
    ejemplos = {
        "Memoria y CPU altas": {"temperature": 65, "cpu_usage": 92, "memory_usage": 94, "network_traffic": 400},
        "Sobrecalentamiento":  {"temperature": 90, "cpu_usage": 70, "memory_usage": 60, "network_traffic": 350},
        "Saturación de red":   {"temperature": 58, "cpu_usage": 55, "memory_usage": 60, "network_traffic": 880},
    }
    for nombre, lectura in ejemplos.items():
        r = diagnose(lectura)
        print("=" * 60)
        print(f"CASO: {nombre}   (manual recuperado: {r['manual']}, similitud {r['score']:.2f}, vía {r['source']})")
        print("-" * 60)
        print(r["diagnosis"][:400])
        print()


if __name__ == "__main__":
    main()
