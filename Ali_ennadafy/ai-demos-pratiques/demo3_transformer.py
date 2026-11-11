"""
Démo 3 : Transformer pré-entraîné (Hugging Face)
------------------------------------------------
On charge des modèles déjà entraînés et on réalise des tâches simples en quelques lignes.
Lancement : python demo3_transformer.py
"""
import os
os.environ["HF_DEACTIVATE_ASYNC_LOAD"] = "1"  # évite le chargement parallèle (crash sous Windows)
os.environ["USE_TF"] = "0"  # ignorer TensorFlow, on utilise uniquement PyTorch
os.environ["USE_TORCH"] = "1"

from transformers import pipeline

print("=== 1. Analyse de sentiment ===")
sentiment = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",  # note de 1 à 5 étoiles
)
for phrase in [
    "Ce cours sur l'intelligence artificielle est vraiment passionnant !",
    "La démonstration ne marchait pas, quelle perte de temps.",
]:
    r = sentiment(phrase)[0]
    print(f"  {phrase}\n   -> {r['label']} (confiance {r['score']:.2f})")

print("\n=== 2. Mot masqué (fill-mask) ===")
fill = pipeline("fill-mask", model="distilbert-base-multilingual-cased")
for p in fill(f"Paris est la capitale de la {fill.tokenizer.mask_token}.")[:3]:
    print(f"  {p['token_str']:<12} score={p['score']:.2f}")

print("\n=== 3. Classification zero-shot ===")
zs = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
texte = "Le gouvernement annonce un nouveau plan pour développer les énergies renouvelables."
res = zs(texte, candidate_labels=["politique", "sport", "technologie", "santé"])
for lab, sc in zip(res["labels"], res["scores"]):
    print(f"  {lab:<12} {sc:.2f}")