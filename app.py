"""
Chatbot d'Atelier - Interface principale Streamlit
Application de maintenance industrielle avec analyse de schémas électriques
"""
import streamlit as st
import os
from datetime import datetime
from typing import Dict, List, Optional
import json

# Import des modules locaux
from google_drive_handler import GoogleDriveHandler
from document_processor import DocumentProcessor
from rag_system import RAGSystem
from vision_analyzer import VisionAnalyzer

# Configuration de la page
st.set_page_config(
    page_title="🔧 Chatbot Atelier Maintenance",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AtelierChatbot:
    """Classe principale du chatbot d'atelier"""
    
    def __init__(self):
        self.drive_handler = None
        self.doc_processor = DocumentProcessor()
        self.rag_system = RAGSystem()
        self.vision_analyzer = VisionAnalyzer()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialise les variables de session Streamlit"""
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant", 
                    "content": "👋 Bonjour ! Je suis votre assistant de maintenance industrielle. \n\nJe peux vous aider à :\n- 🔍 Rechercher dans vos documentations\n- 📋 Analyser des schémas électriques\n- 🛠️ Proposer des solutions de dépannage\n\nQuelle machine vous pose problème aujourd'hui ?"
                }
            ]
        
        if 'current_machine' not in st.session_state:
            st.session_state.current_machine = None
        
        if 'documents_loaded' not in st.session_state:
            st.session_state.documents_loaded = False
        
        if 'selected_schema' not in st.session_state:
            st.session_state.selected_schema = None
    
    def render_sidebar(self):
        """Affiche la barre latérale avec les contrôles"""
        st.sidebar.title("🔧 Configuration")
        
        # Section Google Drive
        with st.sidebar.expander("📁 Google Drive", expanded=False):
            # Récupérer l'ID depuis les secrets ou permettre la saisie
            folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID') or st.secrets.get('GOOGLE_DRIVE_FOLDER_ID', '')
            
            if folder_id:
                st.info(f"📁 Dossier configuré: {folder_id[:20]}...")
                if not self.drive_handler:
                    try:
                        self.drive_handler = GoogleDriveHandler(folder_id)
                        st.success("✅ Connecté à Google Drive")
                    except Exception as e:
                        st.error(f"❌ Erreur connexion: {e}")
            else:
                folder_id_input = st.text_input(
                    "ID du dossier Drive",
                    help="Coller l'ID du dossier depuis l'URL Google Drive"
                )
                
                if st.button("🔗 Connecter Drive"):
                    if folder_id_input:
                        try:
                            self.drive_handler = GoogleDriveHandler(folder_id_input)
                            st.success("✅ Connecté à Google Drive")
                        except Exception as e:
                            st.error(f"❌ Erreur connexion: {e}")
                    else:
                        st.warning("⚠️ Veuillez saisir l'ID du dossier")
        
        # Section gestion des documents
        with st.sidebar.expander("📚 Base de connaissances", expanded=True):
            stats = self.rag_system.get_stats()
            
            st.metric("Documents", stats.get('total_documents', 0))
            st.metric("Machines", stats.get('machines_count', 0))
            
            if st.button("🔄 Recharger documents"):
                self.load_documents_from_drive()
            
            if st.button("🗑️ Vider la base", type="secondary"):
                self.rag_system.clear_collection()
                st.rerun()
        
        # Section machine actuelle
        st.sidebar.subheader("🏭 Machine actuelle")
        machines = self.rag_system.get_machines_list()
        
        if machines:
            current_machine = st.sidebar.selectbox(
                "Sélectionner une machine",
                ["Toutes"] + machines,
                index=0
            )
            st.session_state.current_machine = current_machine if current_machine != "Toutes" else None
        else:
            st.sidebar.info("Aucune machine dans la base")
        
        # Section analyse de coût
        with st.sidebar.expander("💰 Estimation coûts", expanded=False):
            num_schemas = st.number_input("Nombre de schémas à analyser", 1, 50, 5)
            cost_est = self.vision_analyzer.get_cost_estimate(num_schemas)
            st.write(cost_est)
    
    def load_documents_from_drive(self):
        """Charge les documents depuis Google Drive"""
        if not self.drive_handler:
            st.warning("⚠️ Veuillez d'abord connecter Google Drive")
            return
        
        with st.spinner("📥 Chargement des documents..."):
            # Lister tous les fichiers
            files = self.drive_handler.list_files_in_folder()
            
            if not files:
                st.warning("Aucun fichier trouvé dans le dossier Drive")
                return
            
            # Traiter chaque fichier
            documents_to_add = []
            progress_bar = st.progress(0)
            
            for i, file in enumerate(files):
                progress_bar.progress((i + 1) / len(files))
                
                # Télécharger le fichier
                file_content = self.drive_handler.download_file(file['id'])
                if not file_content:
                    continue
                
                # Traiter selon le type
                if file['mimeType'] == 'application/pdf':
                    processed_doc = self.doc_processor.process_pdf(file_content, file['path'])
                elif file['mimeType'].startswith('image/'):
                    processed_doc = self.doc_processor.process_image_file(file_content, file['path'])
                else:
                    continue  # Ignorer les autres types
                
                # Extraire les infos machine
                machine_info = self.doc_processor.extract_machine_info(file['path'])
                
                # Créer le contenu searchable
                searchable_content = self.doc_processor.create_searchable_content(processed_doc)
                
                if searchable_content.strip():
                    documents_to_add.append({
                        'id': file['id'],
                        'content': searchable_content,
                        'metadata': {
                            'file_path': file['path'],
                            'machine_name': machine_info['machine_name'],
                            'document_type': machine_info['document_type'],
                            'mime_type': file['mimeType'],
                            'modified_time': file.get('modifiedTime', ''),
                            'has_images': len(processed_doc.get('images', [])) > 0,
                            'images_count': len(processed_doc.get('images', []))
                        }
                    })
            
            # Ajouter à la base RAG
            if documents_to_add:
                self.rag_system.add_documents_batch(documents_to_add)
                st.session_state.documents_loaded = True
            
            progress_bar.empty()
    
    def handle_user_message(self, user_message: str):
        """Traite un message utilisateur"""
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Rechercher dans la base de connaissances
        search_results = self.rag_system.search_documents(
            query=user_message,
            machine_filter=st.session_state.current_machine,
            n_results=3
        )
        
        # Construire la réponse
        if search_results:
            response = self.generate_response(user_message, search_results)
        else:
            response = "🤔 Je n'ai pas trouvé d'informations pertinentes dans la documentation. Pouvez-vous préciser votre question ou vérifier que les documents sont bien chargés ?"
        
        # Ajouter la réponse de l'assistant
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    def generate_response(self, query: str, search_results: List[Dict]) -> str:
        """Génère une réponse basée sur les résultats de recherche"""
        response_parts = []
        
        # Analyser le type de question
        query_lower = query.lower()
        is_troubleshooting = any(word in query_lower for word in ['panne', 'problème', 'erreur', 'défaut', 'ne marche pas'])
        is_component_search = any(word in query_lower for word in ['où est', 'trouve', 'localise', 'composant'])
        
        if is_troubleshooting:
            response_parts.append("🔧 **Analyse de panne**\n")
        elif is_component_search:
            response_parts.append("🔍 **Localisation de composant**\n")
        else:
            response_parts.append("📋 **Informations trouvées**\n")
        
        # Ajouter les informations trouvées
        for i, result in enumerate(search_results, 1):
            metadata = result['metadata']
            machine = metadata.get('machine_name', 'Machine inconnue')
            doc_type = metadata.get('document_type', 'Document')
            
            response_parts.append(f"**Document {i}** - {machine} ({doc_type})")
            response_parts.append(f"Score: {result['score']:.2f}")
            
            # Résumer le contenu
            content = result['content'][:500] + "..." if len(result['content']) > 500 else result['content']
            response_parts.append(content)
            
            # Proposer d'analyser les schémas si disponibles
            if metadata.get('has_images'):
                response_parts.append(f"📸 Ce document contient {metadata.get('images_count', 0)} schéma(s)")
                response_parts.append("💡 Vous pouvez demander une analyse détaillée des schémas")
            
            response_parts.append("---")
        
        # Ajouter des suggestions selon le contexte
        if is_troubleshooting:
            response_parts.append("\n**Suggestions pour le dépannage :**")
            response_parts.append("1. Vérifiez l'alimentation électrique")
            response_parts.append("2. Contrôlez les fusibles et disjoncteurs")
            response_parts.append("3. Testez les contacteurs et relais")
            response_parts.append("4. Mesurez les tensions aux points de contrôle")
        
        return "\n".join(response_parts)
    
    def render_chat_interface(self):
        """Affiche l'interface de chat"""
        st.title("🔧 Chatbot Atelier Maintenance")
        
        # Afficher les messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Input utilisateur
        if prompt := st.chat_input("Posez votre question sur la maintenance..."):
            self.handle_user_message(prompt)
            st.rerun()
    
    def render_schema_analyzer(self):
        """Interface d'analyse de schémas"""
        st.subheader("📸 Analyse de schémas")
        
        # Upload d'image
        uploaded_image = st.file_uploader(
            "Téléchargez un schéma électrique",
            type=['png', 'jpg', 'jpeg'],
            help="Téléchargez une photo ou scan de schéma électrique"
        )
        
        if uploaded_image:
            # Afficher l'image
            st.image(uploaded_image, caption="Schéma à analyser", use_column_width=True)
            
            # Convertir en base64
            import base64
            image_base64 = base64.b64encode(uploaded_image.read()).decode()
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔍 Analyse générale"):
                    with st.spinner("Analyse en cours..."):
                        result = self.vision_analyzer.analyze_electrical_schema(image_base64)
                        if result['success']:
                            st.success("✅ Analyse terminée")
                            st.write(result['analysis'])
                        else:
                            st.error(f"❌ Erreur: {result['error']}")
            
            with col2:
                symptom = st.text_input("Décrivez le symptôme/panne")
                if st.button("🛠️ Aide au dépannage") and symptom:
                    with st.spinner("Génération de la procédure..."):
                        result = self.vision_analyzer.suggest_troubleshooting(image_base64, symptom)
                        if result['success']:
                            st.success("✅ Procédure générée")
                            st.write(result['analysis'])
                        else:
                            st.error(f"❌ Erreur: {result['error']}")
    
    def run(self):
        """Lance l'application principale"""
        # Barre latérale
        self.render_sidebar()
        
        # Interface principale avec onglets
        tab1, tab2 = st.tabs(["💬 Chat", "📸 Analyse Schémas"])
        
        with tab1:
            self.render_chat_interface()
        
        with tab2:
            self.render_schema_analyzer()
        
        # Footer avec informations
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.info("🏭 Maintenance Industrielle")
        with col2:
            stats = self.rag_system.get_stats()
            st.metric("Documents chargés", stats.get('total_documents', 0))
        with col3:
            if st.session_state.current_machine:
                st.success(f"🔧 Machine: {st.session_state.current_machine}")
            else:
                st.info("🔧 Toutes machines")
        with col4:
            st.caption("🌐 Hébergé sur Streamlit Cloud")

def main():
    """Point d'entrée principal"""
    try:
        chatbot = AtelierChatbot()
        chatbot.run()
    except Exception as e:
        st.error(f"❌ Erreur application: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()