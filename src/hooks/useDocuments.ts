import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { toast } from 'sonner'

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

export function useDocuments() {
  const { user } = useAuth()
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Charger tous les documents (simulation)
  const loadDocuments = useCallback(async () => {
    if (!user) return

    setLoading(true)
    setError(null)

    try {
      // Simulation de documents
      const mockDocuments: Document[] = [
        {
          id: '1',
          name: 'Schema Electrique Machine 1',
          machine: 'Machine 1',
          type: 'schema',
          url: '#',
          size: 1024000,
          uploadedAt: new Date(),
          uploadedBy: user.uid,
        },
        {
          id: '2',
          name: 'Notice Maintenance Machine 2',
          machine: 'Machine 2',
          type: 'pdf',
          url: '#',
          size: 2048000,
          uploadedAt: new Date(),
          uploadedBy: user.uid,
        }
      ]
      
      setDocuments(mockDocuments)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur lors du chargement des documents'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }, [user])

  // Charger les documents par machine
  const loadDocumentsByMachine = useCallback(async (machine: string) => {
    if (!user) return

    setLoading(true)
    setError(null)

    try {
      const mockDocuments: Document[] = [
        {
          id: '1',
          name: `Document ${machine}`,
          machine: machine,
          type: 'pdf',
          url: '#',
          size: 1024000,
          uploadedAt: new Date(),
          uploadedBy: user.uid,
        }
      ]
      
      setDocuments(mockDocuments)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur lors du chargement des documents'
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }, [user])

  // Ajouter un document
  const addDocument = useCallback(async (document: Omit<Document, 'id' | 'uploadedAt'>) => {
    if (!user) {
      toast.error('Vous devez être connecté pour ajouter un document')
      return
    }

    try {
      const newDoc: Document = {
        ...document,
        id: Date.now().toString(),
        uploadedAt: new Date(),
        uploadedBy: user.uid,
      }
      
      setDocuments(prev => [...prev, newDoc])
      toast.success('Document ajouté avec succès')
      return newDoc.id
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur lors de l\'ajout du document'
      toast.error(errorMessage)
      throw err
    }
  }, [user])

  // Supprimer un document
  const deleteDocument = useCallback(async (documentId: string) => {
    if (!user) {
      toast.error('Vous devez être connecté pour supprimer un document')
      return
    }

    try {
      setDocuments(prev => prev.filter(doc => doc.id !== documentId))
      toast.success('Document supprimé avec succès')
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur lors de la suppression du document'
      toast.error(errorMessage)
      throw err
    }
  }, [user])

  // Statistiques des documents
  const getStats = useCallback(() => {
    const totalDocuments = documents.length
    const machines = Array.from(new Set(documents.map(doc => doc.machine)))
    const totalMachines = machines.length
    
    const documentsByType = documents.reduce((acc, doc) => {
      acc[doc.type] = (acc[doc.type] || 0) + 1
      return acc
    }, {} as Record<string, number>)

    return {
      totalDocuments,
      totalMachines,
      machines,
      documentsByType,
    }
  }, [documents])

  // Charger les documents au montage du composant
  useEffect(() => {
    if (user) {
      loadDocuments()
    }
  }, [user, loadDocuments])

  return {
    documents,
    loading,
    error,
    loadDocuments,
    loadDocumentsByMachine,
    addDocument,
    deleteDocument,
    getStats,
  }
} 