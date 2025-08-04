# 🔧 Chatbot Atelier Maintenance - Architecture Moderne

## 🚀 Nouvelle Architecture Next.js 14 + Firebase

Application moderne de maintenance industrielle avec interface React, authentification Firebase, et IA OpenAI.

### ✨ Fonctionnalités

- **🔐 Authentification** Firebase (Google)
- **📁 Gestion documents** Google Drive + Firebase Storage
- **🤖 Chat IA** OpenAI GPT-3.5
- **👁️ Analyse schémas** OpenAI GPT-4 Vision
- **🔍 Recherche avancée** Firestore
- **📱 Interface moderne** React + Tailwind CSS
- **🚀 Déploiement** Vercel

### 🏗️ Architecture Technique

```
🌐 Frontend (Next.js 14 + Vercel)
├── 📱 React 18 + TypeScript
├── 🎨 Tailwind CSS + Shadcn/ui
├── 🔄 Server Actions
└── 🚀 Déploiement Vercel

🔥 Backend (Firebase)
├── 🔐 Authentication
├── 📊 Firestore (NoSQL)
├── 🗄️ Storage
├── ⚡ Cloud Functions
└── 🔍 Full-text Search

🧠 IA & Recherche
├── 🤖 OpenAI GPT-3.5-turbo
├── 👁️ OpenAI GPT-4 Vision
├── 🔍 Firestore Search
└── 📊 Embeddings Hugging Face
```

### 💰 Coût Estimé

- **Firebase** : 0€ (votre compte existant)
- **OpenAI API** : ~7€/an
- **Vercel** : 0€
- **Total** : ~7€/an maximum

### 📦 Installation

```bash
# Cloner le projet
git clone https://github.com/albertduplantin/chatbot-atelier-maintenance.git

# Installer les dépendances
npm install

# Configuration
cp env.example .env.local
# Remplir les variables d'environnement

# Lancer en développement
npm run dev
```

### 🔧 Configuration Requise

#### 1. Firebase (Votre compte existant)
- Projet Firebase configuré
- Authentication activé (Google)
- Firestore activé
- Storage activé

#### 2. OpenAI
- Compte OpenAI
- Clé API GPT-3.5 et GPT-4 Vision

#### 3. Google Drive
- Dossier partagé avec Service Account
- Documents PDF organisés par machine

### 📋 Variables d'Environnement

```env
# Firebase
NEXT_PUBLIC_FIREBASE_API_KEY=your_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_domain
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_bucket
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# OpenAI
OPENAI_API_KEY=your_openai_key

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
```

## 🚀 Déploiement Automatique

### 🎯 Stratégie de Déploiement
- **Déploiement automatique** via Vercel
- **Push sur GitHub** → Déploiement en production
- **Pull Request** → Preview automatique
- **Gratuit** → 100GB bande passante/mois

### 📋 Prérequis
1. **Compte GitHub** (pour le repository)
2. **Compte Vercel** (gratuit)
3. **Projet Firebase** configuré
4. **Variables d'environnement** prêtes

### 🚀 Déploiement Rapide

#### 1. Configurer Vercel
1. Allez sur [https://vercel.com](https://vercel.com)
2. Cliquez sur **"Continue with GitHub"**
3. Sélectionnez votre repository
4. Cliquez sur **"Deploy"**

#### 2. Configurer les Variables d'Environnement
Dans Vercel Dashboard > Settings > Environment Variables :
```env
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyC...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123

# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your_folder_id

# Application URL
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

### 🔄 Déploiement Automatique
Une fois configuré, chaque `git push` déclenche automatiquement un déploiement !

### 📊 Monitoring
- **Vercel Dashboard** : Analytics et performance
- **Firebase Console** : Logs et monitoring
- **GitHub** : Historique des déploiements

### 📖 Guide Complet
Consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour un guide détaillé.

### 📁 Structure des Documents

```
📁 Dossier Google Drive
├── 📁 Machine1
│   ├── 📄 schema_electrique.pdf
│   └── 📄 notice_maintenance.pdf
├── 📁 Machine2
│   └── 📄 documentation.pdf
└── 📄 document_general.pdf
```

### 🎯 Utilisation

1. **Connexion** : Authentification Google
2. **Upload** : Documents automatiquement synchronisés
3. **Chat** : Questions en langage naturel
4. **Analyse** : Upload de schémas électriques
5. **Recherche** : Recherche avancée dans les documents

### 🔍 Fonctionnalités Avancées

- **Recherche sémantique** dans les documents
- **Analyse de schémas** avec IA Vision
- **Suggestions de dépannage** basées sur les documents
- **Historique des conversations**
- **Interface responsive** mobile/desktop

### 🛠️ Développement

```bash
# Installation
npm install

# Développement
npm run dev

# Build
npm run build

# Linting
npm run lint

# Type checking
npm run type-check
```

### 📊 Performance

- **Temps de réponse** : < 1 minute
- **Utilisateurs** : 5 utilisateurs
- **Documents** : 300 éléments
- **Fréquence** : 2 utilisations/semaine

### 🔒 Sécurité

- **Authentification** Firebase sécurisée
- **Documents** stockés de manière sécurisée
- **API keys** protégées côté serveur
- **HTTPS** obligatoire en production

### 🤝 Support

Pour toute question ou problème :
1. Vérifier la documentation
2. Consulter les logs Firebase
3. Tester avec un petit nombre de documents

---

**🎓 Parfait pour vos élèves en maintenance industrielle !**

*Migration depuis Streamlit vers une architecture moderne, robuste et évolutive.*