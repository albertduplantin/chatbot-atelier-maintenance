# 🚀 Quick Start - Déploiement Web

Guide rapide pour avoir votre chatbot d'atelier en ligne en 15 minutes.

## ⚡ Étapes ultra-rapides

### 1. Repository GitHub (2 min)
```bash
1. Créer repository GitHub : "chatbot-atelier"
2. Uploader tous les fichiers du projet
3. Ne PAS uploader credentials.json
```

### 2. Google Drive Setup (5 min)
```bash
1. Google Cloud Console → Nouveau projet
2. API Google Drive → Enable
3. Service Account → Créer → Télécharger JSON
4. Partager dossier Drive avec email du service account
5. Copier ID du dossier Drive
```

### 3. Streamlit Cloud Deploy (3 min)
```bash
1. https://share.streamlit.io
2. GitHub login → New app
3. Repository : votre-repo
4. File : app.py → Deploy
```

### 4. Configuration Secrets (5 min)
```toml
# Dans Streamlit Cloud → Settings → Secrets

GOOGLE_DRIVE_FOLDER_ID = "votre-folder-id"

[openai]
api_key = "sk-votre-cle"  # Optionnel

[google_drive]
# Coller le contenu complet du fichier JSON service account
{
  "type": "service_account",
  "project_id": "...",
  "private_key": "...",
  ...
}
```

## ✅ Test final

1. **Ouvrir votre URL** : `https://xxx.streamlit.app`
2. **Connecter Drive** : Doit marcher automatiquement
3. **Recharger documents** : Voir le compteur augmenter
4. **Tester chat** : "Bonjour" → Réponse

## 🎯 Partage avec élèves

**URL à partager** : `https://votre-chatbot.streamlit.app`

**Instructions élèves** :
```
1. Ouvrir le lien
2. Poser questions : "Machine X ne marche pas"
3. Upload schémas dans onglet "Analyse"
4. Sélectionner machine dans sidebar
```

## 💰 Coût total

- **GitHub** : Gratuit
- **Streamlit Cloud** : Gratuit  
- **Google Drive API** : Gratuit
- **OpenAI** (optionnel) : 2-5€/mois

## 🛠️ Dépannage express

**Erreur Google Drive** :
- Vérifier secrets Streamlit Cloud
- Vérifier partage du dossier

**Aucun document** :
- Vérifier organisation par machine
- Formats : PDF, JPG, PNG seulement

**App endormie** :
- Visiteur l'URL → réveil automatique

---

🎉 **En 15 minutes : chatbot d'atelier accessible partout !**