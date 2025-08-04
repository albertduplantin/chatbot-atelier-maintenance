# 🚀 Instructions de Déploiement Rapide

## 📋 Checklist complète (15 minutes)

### ✅ Étape 1 : GitHub (3 min)
1. Créer repository public : `chatbot-atelier-maintenance`
2. Uploader TOUS les fichiers du projet
3. ❌ **NE PAS** uploader `credentials.json`

### ✅ Étape 2 : Google Cloud (5 min)
1. **Console** : https://console.cloud.google.com
2. **Nouveau projet** : "Chatbot-Atelier"
3. **API** : Activer "Google Drive API"
4. **Service Account** :
   - IAM & Admin → Service Accounts
   - CREATE SERVICE ACCOUNT : "chatbot-service"
   - Télécharger fichier JSON
5. **Dossier Drive** :
   - Partager avec email du service account
   - Copier ID du dossier (URL après /folders/)

### ✅ Étape 3 : Streamlit Cloud (2 min)
1. **Site** : https://share.streamlit.io
2. **Login** : GitHub
3. **New app** :
   - Repository : votre-repo
   - File : `app.py`
   - Deploy!

### ✅ Étape 4 : Secrets (5 min)
Dans Streamlit Cloud → Settings → Secrets :

```toml
GOOGLE_DRIVE_FOLDER_ID = "1ABC2DEF3GHI4JKL"

[openai]
api_key = "sk-proj-..."

[google_drive]
{
  "type": "service_account",
  "project_id": "chatbot-atelier-xxxxx",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "chatbot-service@chatbot-atelier-xxxxx.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

## 🧪 Test Final

1. **Ouvrir** : `https://xxx.streamlit.app`
2. **Drive** : Connexion automatique
3. **Documents** : "Recharger documents"
4. **Chat** : "Bonjour" → Réponse
5. **Partage** : URL aux élèves

## 🔗 Liens essentiels

- **GitHub** : https://github.com
- **Google Cloud** : https://console.cloud.google.com
- **Streamlit Cloud** : https://share.streamlit.io
- **OpenAI** : https://platform.openai.com

## 💡 Organisation Drive

```
📁 ATELIER_DOCS/
├── 📁 TOUR_CONVENTIONAL/
│   ├── 📄 schema_electrique.pdf
│   └── 📄 manuel_maintenance.pdf
├── 📁 FRAISEUSE_CNC/
│   └── 📄 documentation_complete.pdf
└── 📁 PRESSE_HYDRAULIQUE/
    └── 📄 schemas_hydrauliques.pdf
```

## ⚡ Résolution problèmes

| Problème | Solution |
|----------|-----------|
| Erreur Google Drive | Vérifier secrets + partage dossier |
| Aucun document | Organisation par machine requise |
| App endormie | Cliquer sur l'URL → réveil auto |
| Erreur OpenAI | Vérifier clé API + crédit |

## 🎯 Résultat Final

✅ **URL publique** : `https://votre-chatbot.streamlit.app`  
✅ **Accessible 24/7** depuis n'importe quel appareil  
✅ **Gratuit** (sauf OpenAI optionnel)  
✅ **Sécurisé** avec HTTPS  
✅ **Maintenance automatique** via GitHub  

---

🎉 **Chatbot d'atelier opérationnel en 15 minutes !**