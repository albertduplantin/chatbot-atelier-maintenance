"""
Système RAG (Retrieval Augmented Generation) pour la recherche dans les documents
"""
import os
import pickle
from typing import List, Dict, Optional, Tuple
import streamlit as st

# Fix pour ChromaDB sur Streamlit Cloud - Force l'utilisation de pysqlite3-binary
import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGSystem:
    """Système de recherche et génération augmentée par récupération"""
    
    def __init__(self, collection_name: str = "atelier_docs"):
        self.collection_name = collection_name
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self.initialize()
    
    def initialize(self):
        """Initialise le système RAG"""
        try:
            # Initialiser le modèle d'embeddings (français)
            self.embedding_model = SentenceTransformer('distiluse-base-multilingual-cased')
            
            # Initialiser ChromaDB
            self.chroma_client = chromadb.PersistentClient(
                path="./chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Créer ou récupérer la collection
            try:
                self.collection = self.chroma_client.get_collection(name=self.collection_name)
                st.success(f"✅ Collection '{self.collection_name}' chargée ({self.collection.count()} documents)")
            except:
                self.collection = self.chroma_client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Documents d'atelier maintenance"}
                )
                st.info(f"📝 Nouvelle collection '{self.collection_name}' créée")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'initialisation RAG: {e}")
    
    def add_document(self, doc_id: str, content: str, metadata: Dict):
        """Ajoute un document à la base de connaissances"""
        try:
            # Créer l'embedding du contenu
            embedding = self.embedding_model.encode(content).tolist()
            
            # Ajouter à ChromaDB
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erreur ajout document {doc_id}: {e}")
            return False
    
    def add_documents_batch(self, documents: List[Dict]):
        """Ajoute plusieurs documents en lot"""
        if not documents:
            return
        
        try:
            # Préparer les données
            contents = []
            metadatas = []
            ids = []
            
            for doc in documents:
                contents.append(doc['content'])
                metadatas.append(doc['metadata'])
                ids.append(doc['id'])
            
            # Créer les embeddings en lot
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # Ajouter à ChromaDB
            self.collection.add(
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            st.success(f"✅ {len(documents)} documents ajoutés à la base de connaissances")
            
        except Exception as e:
            st.error(f"❌ Erreur ajout batch: {e}")
    
    def search_documents(self, query: str, machine_filter: Optional[str] = None, 
                        doc_type_filter: Optional[str] = None, n_results: int = 5) -> List[Dict]:
        """Recherche des documents pertinents"""
        try:
            # Créer l'embedding de la requête
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Construire les filtres
            where_clause = {}
            if machine_filter:
                where_clause['machine_name'] = machine_filter
            if doc_type_filter:
                where_clause['document_type'] = doc_type_filter
            
            # Effectuer la recherche
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_clause if where_clause else None,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Formater les résultats
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'score': 1 - results['distances'][0][i],  # Convertir distance en score
                        'id': results['ids'][0][i] if 'ids' in results else f"result_{i}"
                    })
            
            return formatted_results
            
        except Exception as e:
            st.error(f"❌ Erreur recherche: {e}")
            return []
    
    def get_machines_list(self) -> List[str]:
        """Récupère la liste des machines disponibles"""
        try:
            # Récupérer tous les documents pour extraire les machines
            all_results = self.collection.get(include=['metadatas'])
            
            machines = set()
            if all_results['metadatas']:
                for metadata in all_results['metadatas']:
                    if 'machine_name' in metadata and metadata['machine_name']:
                        machines.add(metadata['machine_name'])
            
            return sorted(list(machines))
            
        except Exception as e:
            st.error(f"❌ Erreur récupération machines: {e}")
            return []
    
    def get_document_types(self) -> List[str]:
        """Récupère la liste des types de documents disponibles"""
        try:
            all_results = self.collection.get(include=['metadatas'])
            
            doc_types = set()
            if all_results['metadatas']:
                for metadata in all_results['metadatas']:
                    if 'document_type' in metadata and metadata['document_type']:
                        doc_types.add(metadata['document_type'])
            
            return sorted(list(doc_types))
            
        except Exception as e:
            st.error(f"❌ Erreur récupération types: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Retourne des statistiques sur la base de connaissances"""
        try:
            count = self.collection.count()
            machines = self.get_machines_list()
            doc_types = self.get_document_types()
            
            return {
                'total_documents': count,
                'machines_count': len(machines),
                'document_types_count': len(doc_types),
                'machines': machines,
                'document_types': doc_types
            }
            
        except Exception as e:
            st.error(f"❌ Erreur statistiques: {e}")
            return {}
    
    def clear_collection(self):
        """Vide la collection (utile pour réinitialiser)"""
        try:
            # Supprimer la collection existante
            self.chroma_client.delete_collection(name=self.collection_name)
            
            # Recréer une nouvelle collection
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"description": "Documents d'atelier maintenance"}
            )
            
            st.success("✅ Base de connaissances réinitialisée")
            
        except Exception as e:
            st.error(f"❌ Erreur réinitialisation: {e}")
    
    def generate_context_for_query(self, query: str, machine_filter: Optional[str] = None) -> str:
        """Génère le contexte pour une requête donnée"""
        # Rechercher les documents pertinents
        results = self.search_documents(
            query=query, 
            machine_filter=machine_filter, 
            n_results=3
        )
        
        if not results:
            return "Aucun document pertinent trouvé dans la base de connaissances."
        
        # Construire le contexte
        context_parts = []
        context_parts.append("Informations trouvées dans la documentation :\n")
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            machine = metadata.get('machine_name', 'Machine inconnue')
            doc_type = metadata.get('document_type', 'Document')
            file_path = metadata.get('file_path', 'Fichier inconnu')
            
            context_parts.append(f"--- Document {i} ---")
            context_parts.append(f"Machine: {machine}")
            context_parts.append(f"Type: {doc_type}")
            context_parts.append(f"Source: {file_path}")
            context_parts.append(f"Score de pertinence: {result['score']:.2f}")
            context_parts.append(f"Contenu:\n{result['content'][:1000]}...")
            context_parts.append("")
        
        return '\n'.join(context_parts)