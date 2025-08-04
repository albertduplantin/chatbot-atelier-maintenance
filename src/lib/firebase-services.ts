import { 
  collection, 
  addDoc, 
  getDocs, 
  query, 
  where, 
  orderBy, 
  limit,
  doc,
  updateDoc,
  deleteDoc,
  serverTimestamp,
  DocumentData,
  QueryDocumentSnapshot
} from 'firebase/firestore'
import { 
  ref, 
  uploadBytes, 
  getDownloadURL, 
  deleteObject,
  listAll
} from 'firebase/storage'
import { db } from './firebase'
import { storage } from './firebase-storage'

// Types pour les données
export interface Document {
  id?: string
  name: string
  machine: string
  type: 'pdf' | 'image' | 'schema'
  url: string
  size: number
  uploadedAt: Date
  uploadedBy: string
  tags?: string[]
  description?: string
}

export interface Conversation {
  id?: string
  userId: string
  messages: Message[]
  machine?: string
  createdAt: Date
  updatedAt: Date
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  metadata?: {
    machine?: string
    document?: string
    confidence?: number
  }
}

// Service pour les documents
export class DocumentService {
  private collection = 'documents'

  // Ajouter un nouveau document
  async addDocument(document: Omit<Document, 'id' | 'uploadedAt'>): Promise<string> {
    try {
      const docRef = await addDoc(collection(db, this.collection), {
        ...document,
        uploadedAt: serverTimestamp(),
      })
      return docRef.id
    } catch (error) {
      console.error('Erreur lors de l\'ajout du document:', error)
      throw error
    }
  }

  // Récupérer tous les documents
  async getDocuments(): Promise<Document[]> {
    try {
      const querySnapshot = await getDocs(collection(db, this.collection))
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Document[]
    } catch (error) {
      console.error('Erreur lors de la récupération des documents:', error)
      throw error
    }
  }

  // Récupérer les documents par machine
  async getDocumentsByMachine(machine: string): Promise<Document[]> {
    try {
      const q = query(
        collection(db, this.collection),
        where('machine', '==', machine),
        orderBy('uploadedAt', 'desc')
      )
      const querySnapshot = await getDocs(q)
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Document[]
    } catch (error) {
      console.error('Erreur lors de la récupération des documents par machine:', error)
      throw error
    }
  }

  // Supprimer un document
  async deleteDocument(documentId: string): Promise<void> {
    try {
      await deleteDoc(doc(db, this.collection, documentId))
    } catch (error) {
      console.error('Erreur lors de la suppression du document:', error)
      throw error
    }
  }
}

// Service pour les conversations
export class ConversationService {
  private collection = 'conversations'

  // Créer une nouvelle conversation
  async createConversation(userId: string, machine?: string): Promise<string> {
    try {
      const docRef = await addDoc(collection(db, this.collection), {
        userId,
        machine,
        messages: [],
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp(),
      })
      return docRef.id
    } catch (error) {
      console.error('Erreur lors de la création de la conversation:', error)
      throw error
    }
  }

  // Ajouter un message à une conversation
  async addMessage(conversationId: string, message: Omit<Message, 'id'>): Promise<void> {
    try {
      const conversationRef = doc(db, this.collection, conversationId)
      const conversation = await getDocs(query(
        collection(db, this.collection),
        where('__name__', '==', conversationId)
      ))
      
      if (!conversation.empty) {
        const currentMessages = conversation.docs[0].data().messages || []
        const newMessage = {
          ...message,
          id: Date.now().toString(),
        }
        
        await updateDoc(conversationRef, {
          messages: [...currentMessages, newMessage],
          updatedAt: serverTimestamp(),
        })
      }
    } catch (error) {
      console.error('Erreur lors de l\'ajout du message:', error)
      throw error
    }
  }

  // Récupérer les conversations d'un utilisateur
  async getUserConversations(userId: string): Promise<Conversation[]> {
    try {
      const q = query(
        collection(db, this.collection),
        where('userId', '==', userId),
        orderBy('updatedAt', 'desc'),
        limit(10)
      )
      const querySnapshot = await getDocs(q)
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Conversation[]
    } catch (error) {
      console.error('Erreur lors de la récupération des conversations:', error)
      throw error
    }
  }

  // Supprimer une conversation
  async deleteConversation(conversationId: string): Promise<void> {
    try {
      await deleteDoc(doc(db, this.collection, conversationId))
    } catch (error) {
      console.error('Erreur lors de la suppression de la conversation:', error)
      throw error
    }
  }
}

// Service pour le stockage de fichiers
export class StorageService {
  // Uploader un fichier
  async uploadFile(file: File, path: string): Promise<string> {
    try {
      const storageRef = ref(storage, path)
      const snapshot = await uploadBytes(storageRef, file)
      const downloadURL = await getDownloadURL(snapshot.ref)
      return downloadURL
    } catch (error) {
      console.error('Erreur lors de l\'upload du fichier:', error)
      throw error
    }
  }

  // Supprimer un fichier
  async deleteFile(path: string): Promise<void> {
    try {
      const storageRef = ref(storage, path)
      await deleteObject(storageRef)
    } catch (error) {
      console.error('Erreur lors de la suppression du fichier:', error)
      throw error
    }
  }

  // Lister les fichiers dans un dossier
  async listFiles(folderPath: string): Promise<string[]> {
    try {
      const folderRef = ref(storage, folderPath)
      const result = await listAll(folderRef)
      return result.items.map(item => item.fullPath)
    } catch (error) {
      console.error('Erreur lors de la liste des fichiers:', error)
      throw error
    }
  }
}

// Instances des services
export const documentService = new DocumentService()
export const conversationService = new ConversationService()
export const storageService = new StorageService() 