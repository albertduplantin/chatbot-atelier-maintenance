"""
Gestionnaire pour accéder aux documents Google Drive
"""
import os
import io
import json
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
import streamlit as st

class GoogleDriveHandler:
    """Gestionnaire pour accéder aux documents dans Google Drive"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    def __init__(self, folder_id: str):
        self.folder_id = folder_id
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authentification avec Google Drive API"""
        creds = None
        
        # Vérifier si on a des credentials stockés dans Streamlit secrets
        if hasattr(st, 'secrets') and 'google_drive' in st.secrets:
            creds_dict = dict(st.secrets['google_drive'])
            
            # Vérifier si c'est un service account ou OAuth2
            if creds_dict.get('type') == 'service_account':
                # Service Account credentials
                creds = service_account.Credentials.from_service_account_info(
                    creds_dict, scopes=self.SCOPES)
            else:
                # OAuth2 credentials (legacy)
                creds = Credentials.from_authorized_user_info(creds_dict, self.SCOPES)
        
        # Si pas de credentials valides, on affiche un message d'erreur
        if not creds:
            st.error("❌ Credentials Google Drive non configurés. Voir le README.")
            return
        
        # Pour les credentials OAuth2, vérifier s'ils sont valides
        if hasattr(creds, 'valid') and not creds.valid:
            if hasattr(creds, 'expired') and creds.expired and hasattr(creds, 'refresh_token') and creds.refresh_token:
                creds.refresh(Request())
            else:
                st.error("❌ Credentials Google Drive expirés ou invalides.")
                return
        
        self.service = build('drive', 'v3', credentials=creds)
        
        # Afficher un message de succès si la connexion fonctionne
        try:
            # Test simple de connexion
            self.service.files().list(pageSize=1).execute()
            st.success("✅ Connecté à Google Drive")
        except Exception as e:
            st.error(f"❌ Erreur de connexion Google Drive: {e}")
            return
    
    def list_files_in_folder(self, folder_id: Optional[str] = None) -> List[Dict]:
        """Liste tous les fichiers dans un dossier"""
        if not self.service:
            return []
        
        target_folder = folder_id or self.folder_id
        
        try:
            # Rechercher tous les fichiers dans le dossier
            query = f"'{target_folder}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            all_files = []
            
            for file in files:
                file_info = {
                    'id': file['id'],
                    'name': file['name'],
                    'mimeType': file['mimeType'],
                    'modifiedTime': file.get('modifiedTime'),
                    'path': self.get_file_path(file['id'])
                }
                
                # Si c'est un dossier, lister récursivement
                if file['mimeType'] == 'application/vnd.google-apps.folder':
                    subfolder_files = self.list_files_in_folder(file['id'])
                    all_files.extend(subfolder_files)
                else:
                    all_files.append(file_info)
            
            return all_files
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la liste des fichiers: {e}")
            return []
    
    def get_file_path(self, file_id: str) -> str:
        """Obtient le chemin complet d'un fichier"""
        try:
            file_metadata = self.service.files().get(
                fileId=file_id, 
                fields='name, parents'
            ).execute()
            
            path_parts = [file_metadata['name']]
            
            # Remonter la hiérarchie des dossiers
            if 'parents' in file_metadata:
                parent_id = file_metadata['parents'][0]
                while parent_id != self.folder_id:
                    parent = self.service.files().get(
                        fileId=parent_id, 
                        fields='name, parents'
                    ).execute()
                    path_parts.insert(0, parent['name'])
                    if 'parents' in parent:
                        parent_id = parent['parents'][0]
                    else:
                        break
            
            return '/'.join(path_parts)
            
        except Exception as e:
            return f"unknown_path/{file_metadata.get('name', 'unknown')}"
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Télécharge un fichier depuis Google Drive"""
        if not self.service:
            return None
        
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            return file_io.getvalue()
            
        except Exception as e:
            st.error(f"❌ Erreur lors du téléchargement: {e}")
            return None
    
    def search_files_by_machine(self, machine_name: str) -> List[Dict]:
        """Recherche des fichiers pour une machine spécifique"""
        all_files = self.list_files_in_folder()
        
        # Filtrer les fichiers qui contiennent le nom de la machine
        machine_files = []
        for file in all_files:
            if machine_name.lower() in file['path'].lower() or machine_name.lower() in file['name'].lower():
                machine_files.append(file)
        
        return machine_files