'use client'

import { useState, useRef, useEffect } from 'react'
import { useChat } from '@/contexts/ChatContext'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { 
  Send, 
  Bot, 
  User, 
  Loader2, 
  AlertCircle,
  FileText,
  Wrench
} from 'lucide-react'
import { formatRelativeTime } from '@/lib/utils'
import { toast } from 'sonner'

export function ChatInterface() {
  const { messages, addMessage, isLoading, setIsLoading } = useChat()
  const { user } = useAuth()
  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!inputValue.trim()) return
    
    if (!user) {
      toast.error('Veuillez vous connecter pour utiliser le chat')
      return
    }

    // Ajouter le message utilisateur
    addMessage({
      role: 'user',
      content: inputValue
    })

    const userMessage = inputValue
    setInputValue('')
    setIsLoading(true)

    try {
      // Simuler une réponse IA (à remplacer par l'appel OpenAI)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const aiResponse = generateAIResponse(userMessage)
      
      addMessage({
        role: 'assistant',
        content: aiResponse
      })
    } catch (error) {
      toast.error('Erreur lors de la génération de la réponse')
      addMessage({
        role: 'assistant',
        content: '❌ Désolé, une erreur s\'est produite. Veuillez réessayer.'
      })
    } finally {
      setIsLoading(false)
    }
  }

  const generateAIResponse = (userMessage: string): string => {
    const message = userMessage.toLowerCase()
    
    if (message.includes('bonjour') || message.includes('salut')) {
      return '👋 Bonjour ! Comment puis-je vous aider avec la maintenance de vos machines aujourd\'hui ?'
    }
    
    if (message.includes('machine') || message.includes('équipement')) {
      return '🏭 Je peux vous aider avec la maintenance de vos machines. Pouvez-vous me préciser :\n\n• Le nom ou type de machine\n• Le problème rencontré\n• Les symptômes observés\n\nAvec ces informations, je pourrai vous fournir des conseils précis !'
    }
    
    if (message.includes('panne') || message.includes('problème') || message.includes('erreur')) {
      return '🔧 Pour diagnostiquer une panne, j\'ai besoin de plus d\'informations :\n\n• Quelle machine est concernée ?\n• Quels sont les symptômes exacts ?\n• Y a-t-il des messages d\'erreur ?\n• Quand le problème a-t-il commencé ?\n\nPlus vous me donnerez de détails, mieux je pourrai vous aider !'
    }
    
    if (message.includes('schéma') || message.includes('électrique')) {
      return '⚡ Pour analyser un schéma électrique, vous pouvez :\n\n1. **Uploader une image** via le bouton "Uploader un schéma" dans la sidebar\n2. **Décrire le problème** que vous rencontrez\n3. **Poser des questions** spécifiques sur les composants\n\nJe pourrai alors vous aider à identifier les éléments et proposer des solutions !'
    }
    
    return '🤔 Je comprends votre question. Pour vous aider au mieux, pourriez-vous me donner plus de détails sur :\n\n• La machine concernée\n• Le contexte de votre demande\n• Les documents disponibles\n\nJe suis là pour vous accompagner dans vos tâches de maintenance !'
  }

  return (
    <div className="flex flex-col h-full">
      {/* En-tête du chat */}
      <div className="border-b p-4">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
            <Bot className="h-4 w-4 text-primary-foreground" />
          </div>
          <div>
            <h2 className="font-semibold">Assistant Maintenance</h2>
            <p className="text-sm text-muted-foreground">
              {user ? 'Connecté et prêt à vous aider' : 'Connectez-vous pour commencer'}
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 chat-message ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role === 'assistant' && (
              <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-primary-foreground" />
              </div>
            )}
            
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted'
              }`}
            >
              <div className="whitespace-pre-wrap text-sm">
                {message.content}
              </div>
              <div className={`text-xs mt-2 ${
                message.role === 'user' 
                  ? 'text-primary-foreground/70' 
                  : 'text-muted-foreground'
              }`}>
                {formatRelativeTime(message.timestamp)}
              </div>
            </div>
            
            {message.role === 'user' && (
              <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center flex-shrink-0">
                <User className="h-4 w-4" />
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
              <Bot className="h-4 w-4 text-primary-foreground" />
            </div>
            <div className="bg-muted rounded-lg p-3">
              <div className="flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">L'assistant réfléchit...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Zone de saisie */}
      <div className="border-t p-4">
        {!user ? (
          <div className="flex items-center justify-center p-8 text-center">
            <div className="space-y-4">
              <AlertCircle className="h-12 w-12 text-muted-foreground mx-auto" />
              <div>
                <h3 className="font-semibold">Connexion requise</h3>
                <p className="text-sm text-muted-foreground">
                  Connectez-vous avec Google pour utiliser l'assistant
                </p>
              </div>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Posez votre question sur la maintenance..."
              disabled={isLoading}
              className="flex-1"
            />
            <Button 
              type="submit" 
              disabled={isLoading || !inputValue.trim()}
              size="icon"
            >
              <Send className="h-4 w-4" />
            </Button>
          </form>
        )}
      </div>
    </div>
  )
} 