"""
Démo 1 : mini-chatbot RAG (Retrieval-Augmented Generation)
-----------------------------------------------------------
Principe :
  1. On découpe les documents en morceaux (chunks)
  2. On transforme chaque chunk en vecteur (embedding)
  3. Pour une question, on retrouve les chunks les plus proches (similarité cosinus)
  4. On donne ces chunks + la question à un LLM qui rédige la réponse

Lancement :  python demo1_rag.py
Mettre vos propres fichiers .txt dans le dossier "docs/".
"""
import os
import glob
import numpy as np
from sentence_transformers import SentenceTransformer

DOCS_DIR = "docs"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # marche en français
TOP_K = 3

# ---------- 0. Base documentaire d'exemple (créée si le dossier est vide) ----------
SAMPLE = {
    "transformers.txt": (
        "Un Transformer est une architecture de réseau de neurones introduite en 2017 "
        "dans l'article 'Attention Is All You Need'. Elle repose sur le mécanisme "
        "d'auto-attention, qui permet de relier tous les mots d'une phrase entre eux.\n\n"
        "BERT est un Transformer de type encodeur, adapté à la compréhension de texte. "
        "GPT est un Transformer de type décodeur, adapté à la génération de texte."
    ),
    "rag.txt": (
        "Le RAG (Retrieval-Augmented Generation) combine un moteur de recherche et un LLM. "
        "Les documents sont découpés en chunks, transformés en embeddings et stockés dans "
        "une base vectorielle. À chaque question, les chunks les plus pertinents sont "
        "injectés dans le prompt du modèle.\n\n"
        "Le RAG réduit les hallucinations et permet d'utiliser des données récentes ou "
        "privées sans ré-entraîner le modèle."
    ),
    "llm.txt": (
        "Un LLM (Large Language Model) est un modèle de langage de grande taille entraîné "
        "à prédire le mot suivant. On peut l'utiliser via une API (cloud) ou en local "
        "avec des outils comme Ollama ou Hugging Face Transformers.\n\n"
        "Le fine-tuning adapte un modèle à une tâche précise, alors que le prompt "
        "engineering consiste à mieux formuler les instructions données au modèle."
    ),
}


def ensure_sample_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)
    if not glob.glob(os.path.join(DOCS_DIR, "*.txt")):
        for name, text in SAMPLE.items():
            with open(os.path.join(DOCS_DIR, name), "w", encoding="utf-8") as f:
                f.write(text)
        print(f"[info] Documents d'exemple créés dans '{DOCS_DIR}/'")


def load_chunks():
    chunks = []  # (source, texte)
    for path in sorted(glob.glob(os.path.join(DOCS_DIR, "*.txt"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for para in text.split("\n\n"):
            para = para.strip()
            if para:
                chunks.append((os.path.basename(path), para))
    return chunks


def retrieve(question, model, chunk_vecs, chunks, k=TOP_K):
    q = model.encode([question], normalize_embeddings=True)[0]
    scores = chunk_vecs @ q  # vecteurs normalisés => produit scalaire = cosinus
    best = np.argsort(-scores)[:k]
    return [(chunks[i][0], chunks[i][1], float(scores[i])) for i in best]


def generate(question, context_chunks):
    context = "\n\n".join(f"[{src}] {txt}" for src, txt, _ in context_chunks)
    prompt = (
        "Réponds à la question en utilisant UNIQUEMENT le contexte ci-dessous. "
        "Si la réponse n'y est pas, dis que tu ne sais pas.\n\n"
        f"Contexte :\n{context}\n\nQuestion : {question}"
    )
    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    # Mode sans API : on montre simplement le meilleur passage retrouvé
    return ("(Pas de clé API : mode 'retrieval seul')\n"
            "Passage le plus pertinent : " + context_chunks[0][1])


def main():
    ensure_sample_docs()
    chunks = load_chunks()
    print(f"{len(chunks)} chunks chargés. Chargement du modèle d'embeddings...")
    model = SentenceTransformer(EMBED_MODEL)
    chunk_vecs = model.encode([c[1] for c in chunks], normalize_embeddings=True)

    print("\nChatbot RAG prêt. Tapez 'exit' pour quitter.\n")
    while True:
        q = input("Question > ").strip()
        if q.lower() in {"exit", "quit", "q"}:
            break
        if not q:
            continue
        found = retrieve(q, model, chunk_vecs, chunks)
        print("\n--- Passages retrouvés ---")
        for src, txt, score in found:
            print(f"  ({score:.2f}) [{src}] {txt[:90]}...")
        print("\n--- Réponse ---")
        print(generate(q, found), "\n")


if __name__ == "__main__":
    main()
