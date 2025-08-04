// Configuration Firebase pour le Chatbot Atelier Maintenance
// 
// INSTRUCTIONS DE CONFIGURATION :
// 1. Allez sur https://console.firebase.google.com/
// 2. Créez un nouveau projet ou sélectionnez votre projet existant
// 3. Dans "Project Settings" > "General", trouvez la section "Your apps"
// 4. Cliquez sur l'icône Web (</>) pour ajouter une app web
// 5. Copiez les valeurs ci-dessous dans votre fichier .env.local

export const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "your-api-key",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "your-project.firebaseapp.com",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "your-project-id",
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET || "your-project.appspot.com",
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID || "123456789",
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID || "your-app-id",
}

// SERVICES À ACTIVER DANS FIREBASE :
// 1. Authentication > Sign-in method > Google (activé)
// 2. Firestore Database > Créer une base de données
// 3. Storage > Créer un bucket de stockage
// 4. Functions (optionnel pour les fonctions serveur)

// RÈGLES DE SÉCURITÉ RECOMMANDÉES :

// Firestore Rules :
/*
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permettre la lecture/écriture aux utilisateurs authentifiés
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
*/

// Storage Rules :
/*
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // Permettre l'upload/download aux utilisateurs authentifiés
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
}
*/ 