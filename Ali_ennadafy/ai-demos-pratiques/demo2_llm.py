"""
Démo 2 : utiliser un LLM
------------------------
Deux modes :
  - API   : python demo2_llm.py api     (nécessite ANTHROPIC_API_KEY)
  - Local : python demo2_llm.py local   (modèle Hugging Face téléchargé une fois)
Option : python demo2_llm.py ollama     (si Ollama est installé : ollama pull llama3.2)
"""
import os
import sys

QUESTION = "Explique en 3 phrases simples ce qu'est un LLM, pour un étudiant en informatique."


def demo_api():
    import anthropic
    client = anthropic.Anthropic()  # lit ANTHROPIC_API_KEY dans l'environnement
    resp = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=400,
        system="Tu es un assistant pédagogique. Réponds en français.",
        messages=[{"role": "user", "content": QUESTION}],
    )
    print(resp.content[0].text)
    print(f"\n[tokens entrée={resp.usage.input_tokens}, sortie={resp.usage.output_tokens}]")


def demo_local():
    from transformers import pipeline
    # Petit modèle (~1 Go) qui tourne sur CPU
    gen = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")
    messages = [{"role": "user", "content": QUESTION}]
    out = gen(messages, max_new_tokens=200, do_sample=False)
    print(out[0]["generated_text"][-1]["content"])


def demo_ollama():
    import requests
    r = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": "llama3.2",
              "messages": [{"role": "user", "content": QUESTION}],
              "stream": False},
        timeout=120,
    )
    print(r.json()["message"]["content"])


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "api"
    if mode == "api" and not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("Définissez d'abord ANTHROPIC_API_KEY (ou lancez : python demo2_llm.py local)")
    {"api": demo_api, "local": demo_local, "ollama": demo_ollama}[mode]()
