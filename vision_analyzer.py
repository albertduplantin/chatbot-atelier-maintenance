"""
Analyseur de vision pour les schémas électriques
Utilise OpenAI GPT-4 Vision pour analyser les images de schémas
"""
import streamlit as st
import base64
from typing import Dict, Optional
import requests
import json

class VisionAnalyzer:
    """Analyseur de schémas électriques utilisant l'IA Vision"""
    
    def __init__(self):
        """Initialise l'analyseur de vision"""
        self.openai_client = None
        self.api_key = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialise le client OpenAI si disponible"""
        try:
            # Essayer de récupérer la clé depuis les secrets Streamlit
            if hasattr(st, 'secrets') and 'openai' in st.secrets:
                self.api_key = st.secrets['openai']['api_key']
            elif 'OPENAI_API_KEY' in st.session_state:
                self.api_key = st.session_state['OPENAI_API_KEY']
            
            if self.api_key:
                try:
                    import openai
                    self.openai_client = openai.OpenAI(api_key=self.api_key)
                except ImportError:
                    st.warning("Module OpenAI non disponible. L'analyse de schémas sera limitée.")
        except Exception as e:
            st.warning(f"Impossible d'initialiser OpenAI: {e}")
    
    def get_cost_estimate(self, num_schemas: int) -> str:
        """Estime le coût d'analyse des schémas
        
        Args:
            num_schemas: Nombre de schémas à analyser
            
        Returns:
            Estimation des coûts en texte
        """
        if not self.api_key:
            return "Configuration OpenAI requise pour l'estimation des coûts"
        
        # Coût approximatif : ~0.01€ par schéma avec GPT-4 Vision
        cost_per_schema = 0.01
        total_cost = num_schemas * cost_per_schema
        
        if total_cost < 0.05:
            return f"📊 Coût estimé : Négligeable (< 5 centimes pour {num_schemas} schéma{'s' if num_schemas > 1 else ''})"
        else:
            return f"📊 Coût estimé : ~{total_cost:.2f}€ pour {num_schemas} schéma{'s' if num_schemas > 1 else ''}"
    
    def analyze_electrical_schema(self, image_base64: str) -> Dict:
        """Analyse générale d'un schéma électrique
        
        Args:
            image_base64: Image encodée en base64
            
        Returns:
            Dictionnaire avec l'analyse du schéma
        """
        if not self.openai_client:
            return {
                "success": False,
                "error": "Client OpenAI non configuré. Veuillez configurer votre clé API OpenAI.",
                "analysis": "⚠️ Analyse non disponible sans OpenAI GPT-4 Vision"
            }
        
        try:
            prompt = """Tu es un expert en schémas électriques industriels. Analyse ce schéma et fournis :

1. **Type de schéma** : Puissance, commande, câblage, etc.
2. **Composants identifiés** : Contacteurs, relais, moteurs, capteurs, etc.
3. **Fonction principale** : Que contrôle ce schéma ?
4. **Points d'attention** : Éléments importants pour la maintenance
5. **Zones critiques** : Parties sensibles aux pannes

Sois précis et technique, comme pour un technicien de maintenance."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "success": True,
                "analysis": analysis,
                "type": "general_analysis"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors de l'analyse : {str(e)}",
                "analysis": "❌ Impossible d'analyser le schéma"
            }
    
    def suggest_troubleshooting(self, image_base64: str, symptom: str) -> Dict:
        """Suggère des solutions de dépannage basées sur un symptôme
        
        Args:
            image_base64: Image encodée en base64
            symptom: Description du problème/symptôme
            
        Returns:
            Dictionnaire avec les suggestions de dépannage
        """
        if not self.openai_client:
            return {
                "success": False,
                "error": "Client OpenAI non configuré. Veuillez configurer votre clé API OpenAI.",
                "analysis": "⚠️ Dépannage non disponible sans OpenAI GPT-4 Vision"
            }
        
        try:
            prompt = f"""Tu es un expert en maintenance industrielle. Analyse ce schéma électrique et le symptôme rapporté.

**SYMPTÔME RAPPORTÉ** : {symptom}

Fournis un diagnostic structuré :

1. **Diagnostic probable** : Causes les plus probables
2. **Vérifications à faire** : Points de mesure et contrôles
3. **Composants à vérifier** : Dans l'ordre de probabilité
4. **Procédure de test** : Étapes concrètes de dépannage
5. **Solutions recommandées** : Actions correctives

Sois pratique et précis, comme pour guider un technicien sur site."""

            response = self.openai_client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1200,
                temperature=0.1
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "success": True,
                "analysis": analysis,
                "type": "troubleshooting",
                "symptom": symptom
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erreur lors du diagnostic : {str(e)}",
                "analysis": "❌ Impossible de diagnostiquer le problème"
            }
    
    def is_available(self) -> bool:
        """Vérifie si l'analyseur de vision est disponible
        
        Returns:
            True si OpenAI est configuré, False sinon
        """
        return self.openai_client is not None
    
    def get_status(self) -> str:
        """Retourne le statut de configuration
        
        Returns:
            Message de statut
        """
        if self.openai_client:
            return "✅ OpenAI GPT-4 Vision configuré"
        elif self.api_key:
            return "⚠️ Clé OpenAI présente mais client non initialisé"
        else:
            return "❌ OpenAI non configuré - Analyse de schémas indisponible"