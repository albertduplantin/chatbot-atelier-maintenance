# 📋 Guide de Déploiement Web Détaillé

Guide étape par étape pour déployer votre chatbot d'atelier sur le web.

## 🎯 Prérequis

- Compte GitHub (gratuit)
- Compte Google avec accès à Google Drive
- (Optionnel) Compte OpenAI pour l'analyse avancée de schémas
- Navigateur web moderne

## 📝 Étape 1 : Configuration Google Drive API

### A. Créer un projet Google Cloud

1. **Allez sur Google Cloud Console**
   - Visitez : https://console.cloud.google.com
   - Connectez-vous avec votre compte Google

2. **Créer un nouveau projet**
   - Cliquez sur "Select a project" en haut
   - Cliquez sur "NEW PROJECT"
   - Nom : "Chatbot-Atelier"
   - Cliquez sur "CREATE"

3. **Activer l'API Google Drive**
   - Menu → APIs & Services → Library
   - Recherchez "Google Drive API"
   - Cliquez sur "Google Drive API"
   - Cliquez sur "ENABLE"

### B. Créer les credentials

1. **Aller dans Credentials**
   - Menu → APIs & Services → Credentials
   - Cliquez sur "CREATE CREDENTIALS" → "OAuth client ID"

2. **Configurer l'écran de consentement** (si demandé)
   - OAuth consent screen → External → CREATE
   - App name : "Chatbot Atelier"
   - User support email : votre email
   - Developer contact : votre email
   - SAVE AND CONTINUE (laisser les autres par défaut)

3. **Créer l'OAuth Client ID**
   - Application type : "Desktop application"
   - Name : "Chatbot Desktop"
   - CREATE

4. **Télécharger le fichier JSON**
   - Cliquez sur le bouton de téléchargement
   - Renommez le fichier en `credentials.json`
   - Placez-le dans le dossier de votre projet

## 📂 Étape 2 : Organiser vos documents Google Drive

### Structure recommandée :
```
📁 ATELIER_DOCS/
├── 📁 TOUR_1/
│   ├── 📄 schema_electrique.pdf
│   ├── 📄 manuel_utilisation.pdf
│   └── 📸 photo_panneau.jpg
├── 📁 FRAISEUSE_DMG/
│   ├── 📄 schemas_puissance.pdf
│   ├── 📄 schemas_commande.pdf
│   └── 📄 guide_maintenance.pdf
├── 📁 PRESSE_HYDRAULIQUE/
│   ├── 📄 schema_hydraulique.pdf
│   └── 📄 procedure_depannage.pdf
└── 📁 COMPRESSEUR_ATLAS/
    ├── 📄 schema_electrique.pdf
    └── 📄 manuel_maintenance.pdf
```

### Obtenir l'ID du dossier :
1. Ouvrez votre dossier dans Google Drive
2. L'URL ressemble à : `https://drive.google.com/drive/folders/1ABC2DEF3GHI4JKL`
3. Copiez la partie après `/folders/` : `1ABC2DEF3GHI4JKL`

## 🚀 Étape 3 : Créer votre repository GitHub

### Sur GitHub.com :
1. **Créer un nouveau repository**
   - Nom : `chatbot-atelier-maintenance`
   - Public (requis pour Streamlit Cloud gratuit)
   - Initialize with README

2. **Uploader les fichiers du projet**
   - Téléchargez tous les fichiers (.py, .txt, .md)
   - **N'uploadez PAS** le fichier credentials.json
   - Drag & drop dans GitHub ou utilisez Git

## 🌐 Étape 4 : Déployer sur Streamlit Cloud

### Configuration Streamlit Cloud :
1. **Allez sur** https://share.streamlit.io
2. **Sign in with GitHub**
3. **New app**
   - Repository : votre chatbot-atelier-maintenance
   - Branch : main
   - Main file path : app.py
4. **Deploy!**

## ✅ Étape 5 : Configuration initiale

1. **Connecter Google Drive**
   - Dans la sidebar, section "Google Drive"
   - Collez l'ID de votre dossier
   - Cliquez sur "Connecter Drive"
   - **Première fois** : une page web s'ouvre pour autoriser l'accès
   - Accordez les permissions

2. **Charger vos documents**
   - Cliquez sur "Recharger documents"
   - Attendez le traitement (peut prendre plusieurs minutes)
   - Vérifiez que le compteur "Documents" augmente

3. **Test rapide**
   - Tapez : "Quelles machines avons-nous ?"
   - Le chatbot devrait lister vos machines

## 🔧 Configuration OpenAI (Optionnel)

### Obtenir une clé API :
1. Allez sur https://platform.openai.com
2. Créez un compte ou connectez-vous
3. Allez dans "API Keys"
4. Créez une nouvelle clé secrète
5. Copiez la clé (sk-...)

### Ajouter la clé :
Créez un fichier `.streamlit/secrets.toml` :
```toml
[openai]
api_key = "sk-votre-cle-ici"
```

### Ajouter du crédit :
- Allez dans "Billing" sur OpenAI
- Ajoutez 5-10€ (suffisant pour des mois)

## 🌐 Déploiement sur Internet (Gratuit)

### Option 1 : Streamlit Cloud (Recommandé)

1. **Préparer le code**
   - Créez un repository GitHub
   - Uploadez votre code (SANS credentials.json)
   - Commit et push

2. **Déployer**
   - Allez sur https://share.streamlit.io
   - Connectez GitHub
   - Sélectionnez votre repo
   - App path : `app.py`
   - Deploy!

3. **Configurer les secrets**
   - Dans Streamlit Cloud, allez dans Settings → Secrets
   - Ajoutez votre configuration :
   ```toml
   GOOGLE_DRIVE_FOLDER_ID = "votre-folder-id"
   
   [openai]
   api_key = "sk-votre-cle"
   
   [google_drive]
   # Contenu de votre fichier credentials.json
   type = "service_account"
   project_id = "votre-project-id"
   # ... etc
   ```

### Option 2 : Compte de service (Pour production)

1. **Créer un service account**
   - Google Cloud Console → IAM & Admin → Service Accounts
   - CREATE SERVICE ACCOUNT
   - Nom : "chatbot-service"
   - Téléchargez le fichier JSON

2. **Partager votre dossier Drive**
   - Ouvrez votre dossier Google Drive
   - Clic droit → Share
   - Ajoutez l'email du service account
   - Permissions : Viewer

3. **Utiliser dans Streamlit Cloud**
   - Copiez le contenu JSON dans les secrets
   - Plus sécurisé pour la production

## 🔍 Vérification et tests

### Tests de base :
```
✅ "Bonjour" → Réponse du chatbot
✅ "Quelles machines ?" → Liste des machines
✅ "Machine X ne démarre pas" → Suggestions
✅ Upload schéma → Analyse (si OpenAI configuré)
```

### Dépannage courant :

**Erreur credentials** :
- Vérifiez le fichier `credentials.json`
- Première fois : autorisez l'accès dans le navigateur

**Aucun document trouvé** :
- Vérifiez l'ID du dossier Drive
- Vérifiez que le dossier contient des PDF/images
- Vérifiez les permissions du dossier

**Erreur OpenAI** :
- Vérifiez la clé API
- Vérifiez le crédit sur votre compte

## 📊 Monitoring et maintenance

### Statistiques à surveiller :
- Nombre de documents chargés
- Nombre de machines détectées
- Usage OpenAI (si configuré)

### Maintenance régulière :
- Ajouter nouveaux documents → Recharger
- Vérifier les logs d'erreur
- Sauvegarder le dossier `chroma_db/`

## 💡 Conseils d'optimisation

1. **Nommage des fichiers** :
   - `machine_schema_electrique.pdf`
   - `machine_manuel_maintenance.pdf`

2. **Organisation Drive** :
   - Un dossier par machine
   - Noms de dossiers clairs

3. **Qualité des documents** :
   - PDFs avec texte sélectionnable = meilleur
   - Images nettes pour l'OCR
   - Schémas haute résolution

4. **Performance** :
   - Plus de documents = recherche plus précise
   - Rechargement uniquement si nouveaux docs

---

🎯 **Vous êtes maintenant prêt à utiliser votre chatbot d'atelier !**