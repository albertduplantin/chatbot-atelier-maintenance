"""
Fichier d'exemple de configuration
Copiez ce fichier en config.py et adaptez les valeurs
"""

# Configuration Google Drive
GOOGLE_DRIVE_CONFIG = {
    "folder_id": "VOTRE_FOLDER_ID_ICI",  # ID du dossier racine contenant vos docs
    "credentials_file": "credentials.json"  # Fichier credentials téléchargé de Google Cloud
}

# Configuration OpenAI (optionnel)
OPENAI_CONFIG = {
    "api_key": "sk-VOTRE_CLE_API_ICI",  # Clé API OpenAI pour l'analyse de schémas
    "model": "gpt-4-vision-preview",    # Modèle pour l'analyse d'images
    "max_tokens": 1500,                 # Limite de tokens par réponse
    "temperature": 0.1                  # Créativité (0 = précis, 1 = créatif)
}

# Configuration de l'application
APP_CONFIG = {
    "title": "🔧 Chatbot Atelier Maintenance",
    "max_documents_per_search": 5,      # Nombre max de documents retournés par recherche
    "chunk_size": 1000,                 # Taille des chunks de texte pour la recherche
    "chunk_overlap": 200                # Chevauchement entre chunks
}

# Configuration RAG (Retrieval Augmented Generation)
RAG_CONFIG = {
    "collection_name": "atelier_docs",
    "embedding_model": "distiluse-base-multilingual-cased",  # Modèle pour embeddings français
    "similarity_threshold": 0.7,        # Seuil de similarité pour la recherche
    "max_results": 10                   # Nombre max de résultats de recherche
}

# Types de documents supportés
SUPPORTED_MIME_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/jpg", 
    "image/png",
    "image/gif",
    "image/bmp"
]

# Types de documents détectés automatiquement
DOCUMENT_TYPES = {
    "schema_electrique": ["schema", "electrique", "electrical", "circuit"],
    "schema_pneumatique": ["pneumatique", "pneumatic", "air"],
    "schema_hydraulique": ["hydraulique", "hydraulic", "huile"],
    "manuel": ["manuel", "manual", "guide", "handbook"],
    "maintenance": ["maintenance", "depannage", "troubleshoot", "reparation"],
    "procedure": ["procedure", "process", "etape", "step"],
    "autre": []
}

# Messages du chatbot
CHATBOT_MESSAGES = {
    "welcome": """👋 Bonjour ! Je suis votre assistant de maintenance industrielle.

Je peux vous aider à :
- 🔍 Rechercher dans vos documentations
- 📋 Analyser des schémas électriques
- 🛠️ Proposer des solutions de dépannage
- 📚 Localiser des composants sur les schémas

Quelle machine vous pose problème aujourd'hui ?""",
    
    "no_documents": "🤔 Je n'ai pas trouvé d'informations pertinentes. Vérifiez que les documents sont bien chargés.",
    
    "drive_not_connected": "⚠️ Veuillez d'abord connecter Google Drive dans la barre latérale.",
    
    "analysis_in_progress": "🔄 Analyse en cours...",
    
    "analysis_complete": "✅ Analyse terminée !"
}

# Configuration des coûts (estimation)
COST_CONFIG = {
    "gpt4_vision_per_image": 0.01,     # ~1 centime par image haute résolution
    "gpt4_vision_per_image_low": 0.003, # ~0.3 centime résolution normale
    "currency": "EUR"
}

# Configuration sécurité
SECURITY_CONFIG = {
    "max_file_size_mb": 10,             # Taille max des fichiers uploadés
    "allowed_extensions": [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "sanitize_filenames": True,         # Nettoyer les noms de fichiers
    "log_user_queries": False           # Logger les questions des utilisateurs
}