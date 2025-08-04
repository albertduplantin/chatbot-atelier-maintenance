# 🌐 Guide de Déploiement Web

Guide pour déployer votre chatbot d'atelier directement sur le web avec Streamlit Cloud (100% gratuit).

## 🎯 Avantages du déploiement web

- ✅ **Accès universel** : Accessible depuis n'importe quel appareil avec internet
- ✅ **Pas d'installation** : Vos élèves utilisent directement depuis leur navigateur
- ✅ **Mise à jour centralisée** : Une seule version à maintenir
- ✅ **Gratuit** : Hébergement gratuit sur Streamlit Cloud
- ✅ **Sécurisé** : HTTPS automatique, gestion des secrets

## 📋 Prérequis

- Compte GitHub (gratuit)
- Compte Google avec accès à Google Drive
- Compte OpenAI (optionnel, pour l'analyse de schémas)

## 🚀 Étape 1 : Préparer votre code sur GitHub

### A. Créer un repository GitHub

1. **Allez sur GitHub.com**
   - Connectez-vous ou créez un compte
   - Cliquez sur "New repository"

2. **Configurer le repository**
   - Nom : `chatbot-atelier-maintenance`
   - Description : `Chatbot pour maintenance industrielle`
   - Public ✅ (requis pour Streamlit Cloud gratuit)
   - Initialize with README ✅

### B. Uploader les fichiers

1. **Télécharger tous les fichiers du projet**
   - `app.py`, `requirements.txt`, etc.
   - **IMPORTANT** : Ne pas uploader `credentials.json` !

2. **Uploader sur GitHub**
   - Drag & drop dans votre repository
   - Ou utilisez GitHub Desktop / git en ligne de commande

## 🔧 Étape 2 : Configuration Google Drive pour le web

### A. Créer un Service Account (Recommandé pour le web)

1. **Google Cloud Console**
   - Allez sur https://console.cloud.google.com
   - Créez un projet : "Chatbot-Atelier"
   - Activez l'API Google Drive

2. **Créer le Service Account**
   - IAM & Admin → Service Accounts
   - "CREATE SERVICE ACCOUNT"
   - Nom : `chatbot-atelier-service`
   - Description : `Service account pour chatbot atelier`
   - CREATE AND CONTINUE

3. **Télécharger la clé**
   - Cliquez sur le service account créé
   - Onglet "KEYS" → ADD KEY → Create new key
   - Type : JSON
   - Téléchargez le fichier JSON

### B. Partager votre dossier Drive

1. **Préparer vos documents**
   ```
   📁 ATELIER_DOCS/
   ├── 📁 TOUR_1/
   │   ├── 📄 schema_electrique.pdf
   │   └── 📄 manuel.pdf
   ├── 📁 FRAISEUSE_DMG/
   │   └── 📄 schemas.pdf
   └── 📁 PRESSE_HYDRAULIQUE/
       └── 📄 hydraulique.pdf
   ```

2. **Partager avec le service account**
   - Clic droit sur votre dossier → Share
   - Coller l'email du service account (dans le fichier JSON)
   - Permissions : **Viewer**
   - Send

3. **Copier l'ID du dossier**
   - URL : `https://drive.google.com/drive/folders/1ABC2DEF3GHI4JKL`
   - ID : `1ABC2DEF3GHI4JKL` (partie après /folders/)

## 🌐 Étape 3 : Déployer sur Streamlit Cloud

### A. Créer l'application

1. **Allez sur Streamlit Cloud**
   - https://share.streamlit.io
   - Sign in with GitHub

2. **Créer une nouvelle app**
   - "New app"
   - Repository : votre `chatbot-atelier-maintenance`
   - Branch : `main`
   - Main file path : `app.py`
   - App URL (optionnel) : `votre-atelier-chatbot`

3. **Deploy!**
   - L'application va se déployer (2-3 minutes)
   - URL publique générée automatiquement

### B. Configurer les secrets

1. **Accéder aux Settings**
   - Dans votre app Streamlit Cloud
   - Menu hamburger → Settings
   - Onglet "Secrets"

2. **Ajouter les secrets**
   ```toml
   # ID de votre dossier Google Drive
   GOOGLE_DRIVE_FOLDER_ID = "1ABC2DEF3GHI4JKL"
   
   # Configuration OpenAI (optionnel)
   [openai]
   api_key = "sk-votre-cle-openai-ici"
   
   # Service Account Google (copier le contenu du fichier JSON)
   [google_drive]
   type = "service_account"
   project_id = "votre-project-id"
   private_key_id = "votre-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nVOTRE_CLE_COMPLETE_ICI\n-----END PRIVATE KEY-----\n"
   client_email = "chatbot-atelier-service@votre-project.iam.gserviceaccount.com"
   client_id = "123456789"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/chatbot-atelier-service%40votre-project.iam.gserviceaccount.com"
   ```

3. **Sauvegarder**
   - L'app va redémarrer automatiquement
   - Vérifiez qu'il n'y a pas d'erreurs

## ✅ Étape 4 : Test et validation

### Tests de base :

1. **Accéder à votre URL**
   - Ex: `https://votre-atelier-chatbot.streamlit.app`

2. **Connecter Google Drive**
   - Sidebar → Section Google Drive
   - L'ID du dossier devrait être pré-rempli
   - Cliquez "Connecter Drive"
   - ✅ Doit afficher "Connecté à Google Drive"

3. **Charger les documents**
   - Cliquez "Recharger documents"
   - Attendez le traitement
   - ✅ Le compteur "Documents" doit augmenter

4. **Test du chat**
   - "Bonjour" → ✅ Réponse du chatbot
   - "Quelles machines avons-nous ?" → ✅ Liste des machines
   - "Comment dépanner la machine X ?" → ✅ Suggestions

5. **Test analyse schéma** (si OpenAI configuré)
   - Onglet "Analyse Schémas"
   - Upload une image de schéma
   - ✅ Analyse détaillée

## 🔧 Maintenance et mise à jour

### Ajouter de nouveaux documents :
1. Ajoutez les fichiers dans votre dossier Google Drive
2. Dans l'app web → "Recharger documents"
3. ✅ Nouveaux documents intégrés

### Modifier le code :
1. Modifiez les fichiers dans GitHub
2. Commit les changements
3. Streamlit Cloud redéploie automatiquement
4. ✅ Mise à jour en ligne

### Monitoring :
- Streamlit Cloud → Analytics : utilisation, erreurs
- Google Cloud Console → API usage
- OpenAI Dashboard → Usage et coûts

## 🎓 Partager avec vos élèves

### URL d'accès :
- **URL publique** : `https://votre-nom-chatbot.streamlit.app`
- Partagez cette URL avec vos élèves
- Accessible 24/7 depuis n'importe quel appareil

### Instructions pour les élèves :
```
🔧 Chatbot Atelier - Mode d'emploi

1. Aller sur : https://votre-chatbot.streamlit.app
2. Poser vos questions dans le chat :
   - "Machine X ne démarre pas, que faire ?"
   - "Où est le contacteur KM3 sur machine Y ?"
   - "Procédure de maintenance machine Z"

3. Analyser un schéma :
   - Onglet "Analyse Schémas"
   - Prendre une photo du schéma
   - Uploader et demander l'analyse

4. Sélectionner une machine spécifique :
   - Sidebar → Machine actuelle
   - Filtrer les résultats par machine
```

## 💰 Coûts et limites

### Gratuit à vie :
- ✅ Streamlit Cloud : hébergement
- ✅ Google Drive API : accès documents
- ✅ Recherche et chat de base

### Optionnel payant :
- 💳 OpenAI : ~1 centime par schéma analysé
- Estimation : 2-5€/mois pour usage atelier

### Limites Streamlit Cloud gratuit :
- 1 app publique active
- Ressources partagées (plus lent aux heures de pointe)
- Mise en veille après 7 jours d'inactivité (réveil automatique)

## 🛡️ Sécurité et bonnes pratiques

### Sécurité :
- ✅ Secrets chiffrés sur Streamlit Cloud
- ✅ HTTPS automatique
- ✅ Service Account avec permissions minimales
- ✅ Pas de credentials dans le code public

### Bonnes pratiques :
- 🔄 Sauvegarder régulièrement votre dossier Drive
- 👥 Partager l'URL uniquement avec vos élèves
- 📊 Surveiller l'usage OpenAI si configuré
- 🔍 Tester après chaque ajout de documents

## 🎯 Résolution de problèmes

### "Erreur de connexion Google Drive" :
- Vérifiez les secrets Streamlit Cloud
- Vérifiez que le dossier est partagé avec le service account
- Vérifiez l'ID du dossier

### "Aucun document trouvé" :
- Vérifiez l'organisation des dossiers (un dossier par machine)
- Formats supportés : PDF, JPG, PNG
- Rechargez les documents

### "Erreur OpenAI" :
- Vérifiez la clé API dans les secrets
- Vérifiez le crédit sur votre compte OpenAI
- Fonctionnalité optionnelle, le chat marche sans

### App qui ne répond plus :
- App mise en veille : visitez l'URL pour la réveiller
- Erreur de code : vérifiez les logs dans Streamlit Cloud
- Redéployer : changez un petit détail dans GitHub

---

🎉 **Votre chatbot d'atelier est maintenant accessible en ligne pour tous vos élèves !**

URL d'exemple : `https://atelier-maintenance-chatbot.streamlit.app`