# 🔧 Chatbot d'Atelier Maintenance

**Application web 100% en ligne** pour aider vos élèves dans le dépannage de machines industrielles, avec analyse automatique de schémas électriques.

🌐 **Déploiement direct sur le web - Pas d'installation locale nécessaire !**

## 🎯 Fonctionnalités

- 💬 **Chat intelligent** : Questions/réponses sur vos machines
- 📁 **Intégration Google Drive** : Accès direct à vos documentations
- 🔍 **Recherche sémantique** : Trouve les infos pertinentes automatiquement
- 📸 **Analyse de schémas** : IA Vision pour interpréter les schémas électriques
- 🛠️ **Aide au dépannage** : Procédures step-by-step personnalisées
- 🏭 **Multi-machines** : Gestion de toutes vos machines par dossiers

## 🚀 Déploiement Web Direct

### 1. Préparer votre repository GitHub
```bash
# Créer un nouveau repository sur GitHub
# Télécharger les fichiers du projet
# Les uploader dans votre repository
```

### 3. Configuration Google Drive

#### A. Créer un projet Google Cloud
1. Allez sur [Google Cloud Console](https://console.cloud.google.com)
2. Créez un nouveau projet
3. Activez l'API Google Drive
4. Créez des credentials OAuth 2.0

#### B. Télécharger le fichier credentials
1. Dans Google Cloud Console → APIs & Services → Credentials
2. Créez un "OAuth 2.0 Client ID" (Application desktop)
3. Téléchargez le fichier JSON
4. Renommez-le `credentials.json` et placez-le dans le dossier du projet

#### C. Obtenir l'ID de votre dossier Drive
1. Ouvrez votre dossier Google Drive avec les documentations
2. Dans l'URL, copiez l'ID (partie après `/folders/`)
   ```
   https://drive.google.com/drive/folders/1ABC2DEF3GHI4JKL
                                          ^^^^^^^^^^^^ (cet ID)
   ```

### 4. Configuration OpenAI (optionnel mais recommandé)
1. Créez un compte sur [OpenAI](https://platform.openai.com)
2. Générez une clé API
3. Ajoutez du crédit (quelques euros suffisent pour des mois d'usage)

### 5. Déployer sur Streamlit Cloud
1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre compte GitHub
3. Sélectionnez votre repository
4. Branch: `main`, File: `app.py`
5. Deploy!

🌐 Votre application sera accessible via une URL publique

## 📁 Organisation des documents dans Google Drive

Organisez vos documents par machine :
```
📁 Dossier_Principal/
├── 📁 Machine_A/
│   ├── 📄 schema_puissance.pdf
│   ├── 📄 schema_commande.pdf
│   └── 📄 manuel_maintenance.pdf
├── 📁 Machine_B/
│   ├── 📸 photo_schema.jpg
│   └── 📄 guide_depannage.pdf
└── 📁 Machine_C/
    └── 📄 documentation_complete.pdf
```

## 🌐 Configuration des secrets Streamlit Cloud

### Configurer les secrets
Une fois votre app déployée, allez dans Settings → Secrets de votre app
Dans Streamlit Cloud, ajoutez vos secrets :

```toml
# .streamlit/secrets.toml
[google_drive]
type = "service_account"
project_id = "votre-project-id"
private_key_id = "votre-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nVOTRE_CLE_PRIVEE\n-----END PRIVATE KEY-----\n"
client_email = "votre-service-account@project.iam.gserviceaccount.com"
client_id = "votre-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"

[openai]
api_key = "sk-votre-cle-openai"

GOOGLE_DRIVE_FOLDER_ID = "votre-folder-id-drive"
```

### Credentials de service (Recommandé pour le web)
1. Google Cloud Console → IAM & Admin → Service Accounts
2. Créez un service account : "chatbot-atelier-service"
3. Téléchargez la clé JSON
4. Partagez votre dossier Drive avec l'email du service account (permissions: Viewer)
5. Copiez le contenu JSON dans les secrets Streamlit Cloud

## 💡 Utilisation

### Accès web
1. **URL publique** : `https://votre-chatbot.streamlit.app`
2. **Premier démarrage** : Les secrets sont pré-configurés
3. **Charger documents** : Cliquez sur "Recharger documents"
4. **Partager** : Donnez l'URL à vos élèves

### Exemples de questions
- "Comment dépanner la machine X qui ne démarre plus ?"
- "Où est le contacteur KM3 sur le schéma de la machine Y ?"
- "La machine Z fait un bruit bizarre, que vérifier ?"
- "Montre-moi la procédure de maintenance de la machine W"

### Analyse de schémas
1. Allez dans l'onglet "Analyse Schémas"
2. Uploadez une photo/scan de schéma
3. Cliquez sur "Analyse générale" ou décrivez un symptôme
4. L'IA vous fournit une analyse détaillée

## 💰 Coûts

### Gratuit
- Streamlit Cloud : hébergement gratuit
- Google Drive API : gratuit
- Embedding et recherche : gratuit

### Payant (optionnel)
- OpenAI GPT-4 Vision : ~1 centime par schéma analysé
- Usage typique : 2-5€/mois pour un atelier

## 🔧 Maintenance et mise à jour

### Ajouter de nouveaux documents
1. Ajoutez les fichiers dans Google Drive
2. Cliquez sur "Recharger documents"
3. Le système met à jour automatiquement

### Réinitialiser la base
1. Cliquez sur "Vider la base" dans la sidebar
2. Rechargez vos documents

### Sauvegarder
La base de connaissances est stockée dans `./chroma_db/`
Sauvegardez ce dossier pour conserver vos données

## 🛠️ Dépannage

### "Credentials Google Drive non configurés"
- Vérifiez que `credentials.json` existe
- Pour Streamlit Cloud : vérifiez les secrets

### "Client OpenAI non initialisé"
- Ajoutez votre clé API OpenAI
- L'analyse de schémas reste possible sans OpenAI (limitée)

### "Aucun fichier trouvé"
- Vérifiez l'ID du dossier Drive
- Vérifiez les permissions du dossier
- Le dossier doit contenir des PDF ou images

### Documents non trouvés
- Vérifiez l'organisation par machine
- Rechargez les documents
- Les noms de dossiers deviennent les noms de machines

## 📚 Architecture technique

```
📦 Application
├── 🌐 app.py (Interface Streamlit)
├── 📁 google_drive_handler.py (Accès Drive)
├── 📄 document_processor.py (Traitement PDF/Images)
├── 🔍 rag_system.py (Recherche intelligente)
├── 👁️ vision_analyzer.py (Analyse schémas)
└── 💾 chroma_db/ (Base de connaissances)
```

### Technologies utilisées
- **Streamlit** : Interface web
- **Google Drive API** : Accès documents
- **ChromaDB** : Base vectorielle
- **SentenceTransformers** : Embeddings français
- **OpenAI GPT-4V** : Analyse d'images
- **PyPDF2** : Extraction PDF
- **Tesseract OCR** : Lecture de texte sur images

## 🤝 Support

Pour toute question ou problème :
1. Vérifiez cette documentation
2. Consultez les logs dans Streamlit
3. Testez avec un petit nombre de documents d'abord

## 📝 Notes importantes

- **Sécurité** : Vos documents restent sur votre Drive
- **Vie privée** : Seuls les extraits nécessaires sont analysés
- **Performance** : Plus de documents = recherche plus précise
- **Coût** : Surveillance recommandée de l'usage OpenAI

---

🎓 **Parfait pour vos élèves en maintenance industrielle !**