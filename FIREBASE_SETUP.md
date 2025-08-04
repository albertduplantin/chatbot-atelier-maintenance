# 🔥 Configuration Firebase - Guide Complet

## 📋 Prérequis
- Compte Google Cloud Platform
- Projet Firebase existant ou nouveau projet
- Compte pay-per-use Firebase (que vous avez déjà)

## 🚀 Étapes de Configuration

### 1. Accéder à Firebase Console
1. Allez sur [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Connectez-vous avec votre compte Google
3. Sélectionnez votre projet existant ou créez un nouveau projet

### 2. Activer les Services Firebase

#### 🔐 Authentication
1. Dans le menu de gauche, cliquez sur **"Authentication"**
2. Cliquez sur **"Get started"**
3. Allez dans l'onglet **"Sign-in method"**
4. Activez **"Google"** comme fournisseur :
   - Cliquez sur **"Google"**
   - Activez le toggle
   - Ajoutez votre email de support
   - Sauvegardez

#### 📊 Firestore Database
1. Dans le menu de gauche, cliquez sur **"Firestore Database"**
2. Cliquez sur **"Create database"**
3. Choisissez **"Start in test mode"** (pour le développement)
4. Sélectionnez une région proche (ex: `europe-west1`)
5. Cliquez sur **"Done"**

#### 💾 Storage
1. Dans le menu de gauche, cliquez sur **"Storage"**
2. Cliquez sur **"Get started"**
3. Choisissez **"Start in test mode"**
4. Sélectionnez la même région que Firestore
5. Cliquez sur **"Done"**

### 3. Configurer l'Application Web

#### 📱 Ajouter une App Web
1. Dans **"Project Settings"** (icône ⚙️)
2. Dans la section **"Your apps"**, cliquez sur l'icône Web (</>)
3. Donnez un nom à votre app : `chatbot-maintenance-web`
4. Activez **"Firebase Hosting"** si vous voulez déployer
5. Cliquez sur **"Register app"**

#### 🔑 Récupérer la Configuration
1. Après l'enregistrement, copiez le code de configuration
2. Il ressemble à ceci :
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### 4. Configurer les Variables d'Environnement

#### 📝 Créer le fichier .env.local
1. Dans votre projet, créez un fichier `.env.local`
2. Copiez le contenu suivant et remplacez par vos vraies valeurs :

```env
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyC...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123

# OpenAI Configuration (optionnel pour l'instant)
OPENAI_API_KEY=your_openai_api_key_here

# Google Drive Configuration (optionnel pour l'instant)
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id

# Configuration de l'application
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 5. Configurer les Règles de Sécurité

#### 🔒 Firestore Rules
1. Dans **"Firestore Database"** > **"Rules"**
2. Remplacez les règles par :

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permettre la lecture/écriture aux utilisateurs authentifiés
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

#### 🗄️ Storage Rules
1. Dans **"Storage"** > **"Rules"**
2. Remplacez les règles par :

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Permettre l'upload/download aux utilisateurs authentifiés
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 6. Tester la Configuration

#### 🧪 Test Local
1. Installez les dépendances :
```bash
npm install
```

2. Lancez l'application :
```bash
npm run dev
```

3. Ouvrez [http://localhost:3000](http://localhost:3000)

4. Testez la connexion Google :
   - Cliquez sur **"Se connecter avec Google"**
   - Autorisez l'application
   - Vérifiez que vous êtes connecté

#### 🔍 Vérifier dans Firebase Console
1. Dans **"Authentication"** > **"Users"** : vous devriez voir votre utilisateur
2. Dans **"Firestore Database"** : les collections seront créées automatiquement
3. Dans **"Storage"** : les fichiers uploadés apparaîtront ici

## 🛠️ Dépannage

### Erreur de Configuration
- Vérifiez que toutes les variables d'environnement sont correctes
- Redémarrez le serveur de développement après modification de `.env.local`

### Erreur d'Authentification
- Vérifiez que Google est activé dans Authentication
- Vérifiez que votre domaine est autorisé (localhost pour le développement)

### Erreur de Permissions
- Vérifiez que les règles Firestore et Storage sont correctes
- Assurez-vous d'être connecté avant d'utiliser les fonctionnalités

## 📊 Coûts Estimés

Avec votre utilisation prévue (5 utilisateurs, 300 éléments, 2 utilisations/semaine) :

- **Firestore** : ~0.50€/mois
- **Storage** : ~0.10€/mois  
- **Authentication** : Gratuit
- **Total estimé** : ~0.60€/mois

## 🎯 Prochaines Étapes

Une fois Firebase configuré, vous pourrez :
1. ✅ Tester l'authentification Google
2. 🔄 Synchroniser les documents
3. 🤖 Intégrer OpenAI pour le chat IA
4. 📁 Implémenter l'upload de schémas
5. 🚀 Déployer sur Vercel

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez les logs dans la console du navigateur
2. Consultez la documentation Firebase
3. Vérifiez que tous les services sont activés 