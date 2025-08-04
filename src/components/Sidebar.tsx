'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useChat } from '@/contexts/ChatContext'
import { useDocuments } from '@/hooks/useDocuments'
import { Button } from '@/components/ui/button'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card'
import { 
  MessageSquare, 
  FileText, 
  Settings, 
  LogIn, 
  RefreshCw, 
  Trash2,
  Database,
  Upload,
  Loader2,
  X
} from 'lucide-react'
import { toast } from 'sonner'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const { user, signInWithGoogle } = useAuth()
  const { clearMessages, currentMachine, setCurrentMachine } = useChat()
  const { documents, loading, loadDocuments, getStats } = useDocuments()

  const handleSignIn = async () => {
    try {
      await signInWithGoogle()
      toast.success('Connexion réussie !')
    } catch (error) {
      toast.error('Erreur de connexion')
    }
  }

  const handleClearChat = () => {
    clearMessages()
    toast.success('Conversation effacée')
  }

  const handleReloadDocuments = async () => {
    if (!user) {
      toast.error('Veuillez vous connecter d\'abord')
      return
    }
    
    try {
      await loadDocuments()
      toast.success('Documents rechargés avec succès')
    } catch (error) {
      toast.error('Erreur lors du rechargement des documents')
    }
  }

  const stats = getStats()

  return (
    <>
      {/* Overlay pour mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed md:static inset-y-0 left-0 z-50 w-80 border-r bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        <div className="flex h-full flex-col gap-4 p-4">
          
          {/* En-tête avec bouton fermer pour mobile */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-sm">🔧</span>
              </div>
              <div>
                <h2 className="font-semibold">Configuration</h2>
                <p className="text-xs text-muted-foreground">Paramètres et contrôles</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={onClose}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Authentification */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <LogIn className="h-4 w-4" />
                Authentification
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {user ? (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <div className="h-2 w-2 rounded-full bg-green-500" />
                    <span className="font-medium">Connecté</span>
                  </div>
                  <p className="text-xs text-muted-foreground truncate">
                    {user.email}
                  </p>
                </div>
              ) : (
                <Button onClick={handleSignIn} className="w-full" size="sm">
                  <LogIn className="h-4 w-4 mr-2" />
                  Se connecter avec Google
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Documents */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <FileText className="h-4 w-4" />
                Documents
              </CardTitle>
              <CardDescription className="text-xs">
                Gestion de la base de connaissances
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="text-center p-2 bg-muted rounded">
                  <div className="font-semibold">
                    {loading ? (
                      <Loader2 className="h-3 w-3 animate-spin mx-auto" />
                    ) : (
                      stats.totalDocuments
                    )}
                  </div>
                  <div className="text-muted-foreground">Documents</div>
                </div>
                <div className="text-center p-2 bg-muted rounded">
                  <div className="font-semibold">
                    {loading ? (
                      <Loader2 className="h-3 w-3 animate-spin mx-auto" />
                    ) : (
                      stats.totalMachines
                    )}
                  </div>
                  <div className="text-muted-foreground">Machines</div>
                </div>
              </div>
              
              <div className="space-y-2">
                <Button 
                  onClick={handleReloadDocuments} 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                  disabled={!user}
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Recharger documents
                </Button>
                
                <Button 
                  onClick={handleClearChat} 
                  variant="outline" 
                  size="sm" 
                  className="w-full"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Vider la base
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Machine actuelle */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <Database className="h-4 w-4" />
                Machine actuelle
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-sm text-muted-foreground">
                {currentMachine ? (
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-blue-500" />
                    {currentMachine}
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-gray-400" />
                    Toutes les machines
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Analyse de schémas */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <Upload className="h-4 w-4" />
                Analyse de schémas
              </CardTitle>
              <CardDescription className="text-xs">
                Upload et analyse d'images
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full"
                disabled={!user}
              >
                <Upload className="h-4 w-4 mr-2" />
                Uploader un schéma
              </Button>
            </CardContent>
          </Card>

          {/* Paramètres */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <Settings className="h-4 w-4" />
                Paramètres
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full"
              >
                <Settings className="h-4 w-4 mr-2" />
                Configuration
              </Button>
            </CardContent>
          </Card>

          {/* Espace libre */}
          <div className="flex-1" />

          {/* Footer */}
          <div className="text-xs text-muted-foreground text-center pt-4 border-t">
            <p>Chatbot Atelier Maintenance</p>
            <p>Version 2.0 - Next.js + Firebase</p>
          </div>
        </div>
      </div>
    </>
  )
} 