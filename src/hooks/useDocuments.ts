import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { documentService, Document } from '@/lib/firebase-services'
import { toast } from 'sonner'

export function useDocuments() {
  const { user } = useAuth()
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Charger tous les documents
  const loadDocuments = useCallback(async () => {
    if (!user) return

    setLoading(true)
    setError(null)

    try {
      const docs = await documentService.getDocuments()
      setDocuments(docs)
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
      const docs = await documentService.getDocumentsByMachine(machine)
      setDocuments(docs)
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
      const docId = await documentService.addDocument({
        ...document,
        uploadedBy: user.uid,
      })
      
      // Recharger les documents
      await loadDocuments()
      
      toast.success('Document ajouté avec succès')
      return docId
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erreur lors de l\'ajout du document'
      toast.error(errorMessage)
      throw err
    }
  }, [user, loadDocuments])

  // Supprimer un document
  const deleteDocument = useCallback(async (documentId: string) => {
    if (!user) {
      toast.error('Vous devez être connecté pour supprimer un document')
      return
    }

    try {
      await documentService.deleteDocument(documentId)
      
      // Mettre à jour la liste locale
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
    const machines = [...new Set(documents.map(doc => doc.machine))]
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