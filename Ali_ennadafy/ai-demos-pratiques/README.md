# Démonstrations pratiques : RAG, LLM, Transformers

## Installation
```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Les 3 démos
| Fichier | Thème | Commande |
|---|---|---|
| `demo1_rag.py` | Mini-chatbot RAG sur une base documentaire (`docs/*.txt`) | `python demo1_rag.py` |
| `demo2_llm.py` | Appel d'un LLM via API ou en local | `python demo2_llm.py api` / `local` / `ollama` |
| `demo3_transformer.py` | Transformers pré-entraînés (sentiment, mot masqué, zero-shot) | `python demo3_transformer.py` |

## Clé API (démos 1 et 2, mode API)
```bash
export ANTHROPIC_API_KEY="votre_clé"     # Windows : set ANTHROPIC_API_KEY=votre_clé
```
Sans clé : la démo 1 fonctionne en mode « recherche seule », la démo 2 en mode `local`.

## Plan de présentation suggéré (≈ 15 min)
1. **Transformer pré-entraîné (3 min)** : montrer qu'on charge un modèle en 1 ligne et qu'il réalise une tâche.
2. **LLM (4 min)** : même question en API puis en local ; comparer qualité, vitesse, coût, confidentialité.
3. **RAG (8 min)** : poser une question hors du savoir du modèle, montrer les passages retrouvés puis la réponse ; ajouter un fichier dans `docs/` en direct.

## Schéma du RAG
Question -> embedding -> recherche des chunks proches -> prompt (contexte + question) -> LLM -> réponse
