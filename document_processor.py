"""
Processeur pour extraire et traiter le contenu des documents
"""
import io
import base64
from typing import List, Dict, Optional, Tuple
from PIL import Image
import PyPDF2
import pytesseract
import streamlit as st

class DocumentProcessor:
    """Traite les documents PDF et images pour extraire le texte et les images"""
    
    def __init__(self):
        # Configuration OCR si disponible
        self.ocr_available = self._check_tesseract()
    
    def _check_tesseract(self) -> bool:
        """Vérifie si Tesseract OCR est disponible"""
        try:
            pytesseract.get_tesseract_version()
            return True
        except:
            st.warning("⚠️ Tesseract OCR non disponible. L'extraction de texte des images sera limitée.")
            return False
    
    def process_pdf(self, pdf_content: bytes, file_path: str) -> Dict:
        """Traite un fichier PDF et extrait texte et images"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            
            result = {
                'file_path': file_path,
                'text_content': '',
                'images': [],
                'page_count': len(pdf_reader.pages),
                'metadata': {}
            }
            
            # Extraire le texte de chaque page
            full_text = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        full_text.append(f"=== Page {page_num + 1} ===\n{text}")
                    
                    # Extraire les images de la page si possible
                    images = self._extract_images_from_page(page, page_num)
                    result['images'].extend(images)
                    
                except Exception as e:
                    st.warning(f"⚠️ Erreur page {page_num + 1}: {e}")
                    continue
            
            result['text_content'] = '\n\n'.join(full_text)
            
            # Métadonnées du PDF
            if pdf_reader.metadata:
                result['metadata'] = {
                    'title': pdf_reader.metadata.get('/Title', ''),
                    'author': pdf_reader.metadata.get('/Author', ''),
                    'subject': pdf_reader.metadata.get('/Subject', ''),
                    'creator': pdf_reader.metadata.get('/Creator', '')
                }
            
            return result
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement PDF {file_path}: {e}")
            return {'file_path': file_path, 'text_content': '', 'images': [], 'error': str(e)}
    
    def _extract_images_from_page(self, page, page_num: int) -> List[Dict]:
        """Extrait les images d'une page PDF"""
        images = []
        
        try:
            if '/XObject' in page['/Resources']:
                xObject = page['/Resources']['/XObject'].get_object()
                
                for obj in xObject:
                    if xObject[obj]['/Subtype'] == '/Image':
                        try:
                            # Extraire l'image
                            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                            data = xObject[obj].get_data()
                            
                            # Convertir en image PIL
                            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                                mode = "RGB"
                            else:
                                mode = "P"
                            
                            image = Image.frombytes(mode, size, data)
                            
                            # Convertir en base64 pour stockage
                            img_buffer = io.BytesIO()
                            image.save(img_buffer, format='PNG')
                            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
                            
                            # Essayer d'extraire le texte de l'image avec OCR
                            ocr_text = ""
                            if self.ocr_available:
                                try:
                                    ocr_text = pytesseract.image_to_string(image, lang='fra')
                                except:
                                    pass
                            
                            images.append({
                                'page': page_num + 1,
                                'image_base64': img_base64,
                                'size': size,
                                'ocr_text': ocr_text.strip()
                            })
                            
                        except Exception as e:
                            continue
                            
        except Exception as e:
            pass
        
        return images
    
    def process_image_file(self, image_content: bytes, file_path: str) -> Dict:
        """Traite un fichier image"""
        try:
            image = Image.open(io.BytesIO(image_content))
            
            # Convertir en base64
            img_buffer = io.BytesIO()
            image.save(img_buffer, format='PNG')
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            # OCR si disponible
            ocr_text = ""
            if self.ocr_available:
                try:
                    ocr_text = pytesseract.image_to_string(image, lang='fra')
                except:
                    pass
            
            return {
                'file_path': file_path,
                'text_content': ocr_text.strip(),
                'images': [{
                    'page': 1,
                    'image_base64': img_base64,
                    'size': image.size,
                    'ocr_text': ocr_text.strip()
                }],
                'metadata': {
                    'format': image.format,
                    'size': image.size,
                    'mode': image.mode
                }
            }
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement image {file_path}: {e}")
            return {'file_path': file_path, 'text_content': '', 'images': [], 'error': str(e)}
    
    def extract_machine_info(self, file_path: str) -> Dict:
        """Extrait les informations sur la machine depuis le chemin du fichier"""
        parts = file_path.split('/')
        
        machine_info = {
            'machine_name': '',
            'document_type': '',
            'subsystem': ''
        }
        
        # Le nom de la machine est généralement le premier dossier
        if len(parts) > 1:
            machine_info['machine_name'] = parts[0]
        
        # Essayer de deviner le type de document
        filename = parts[-1].lower()
        if any(word in filename for word in ['schema', 'electrique', 'electrical']):
            machine_info['document_type'] = 'schema_electrique'
        elif any(word in filename for word in ['manuel', 'manual', 'guide']):
            machine_info['document_type'] = 'manuel'
        elif any(word in filename for word in ['maintenance', 'depannage', 'troubleshoot']):
            machine_info['document_type'] = 'maintenance'
        elif any(word in filename for word in ['pneumatique', 'hydraulique', 'pneumatic', 'hydraulic']):
            machine_info['document_type'] = 'schema_fluide'
        else:
            machine_info['document_type'] = 'autre'
        
        return machine_info
    
    def create_searchable_content(self, processed_doc: Dict) -> str:
        """Crée un contenu searchable à partir d'un document traité"""
        content_parts = []
        
        # Informations sur le fichier
        machine_info = self.extract_machine_info(processed_doc['file_path'])
        content_parts.append(f"Machine: {machine_info['machine_name']}")
        content_parts.append(f"Type: {machine_info['document_type']}")
        content_parts.append(f"Fichier: {processed_doc['file_path']}")
        
        # Texte extrait
        if processed_doc.get('text_content'):
            content_parts.append(f"Contenu textuel:\n{processed_doc['text_content']}")
        
        # Texte OCR des images
        for img in processed_doc.get('images', []):
            if img.get('ocr_text'):
                content_parts.append(f"Texte image page {img['page']}:\n{img['ocr_text']}")
        
        return '\n\n'.join(content_parts)