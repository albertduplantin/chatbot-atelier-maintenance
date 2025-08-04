'use client'

import { createContext, useContext, useState, useCallback } from 'react'

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

export interface ChatContextType {
  messages: Message[]
  isLoading: boolean
  currentMachine: string | null
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void
  clearMessages: () => void
  setCurrentMachine: (machine: string | null) => void
  setIsLoading: (loading: boolean) => void
}

const ChatContext = createContext<ChatContextType | undefined>(undefined)

export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: '👋 Bonjour ! Je suis votre assistant de maintenance industrielle.\n\nJe peux vous aider à :\n- 🔍 Rechercher dans vos documentations\n- 📋 Analyser des schémas électriques\n- 🛠️ Proposer des solutions de dépannage\n\nQuelle machine vous pose problème aujourd\'hui ?',
      timestamp: new Date()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [currentMachine, setCurrentMachine] = useState<string | null>(null)

  const addMessage = useCallback((message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
  }, [])

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: '👋 Bonjour ! Je suis votre assistant de maintenance industrielle.\n\nJe peux vous aider à :\n- 🔍 Rechercher dans vos documentations\n- 📋 Analyser des schémas électriques\n- 🛠️ Proposer des solutions de dépannage\n\nQuelle machine vous pose problème aujourd\'hui ?',
        timestamp: new Date()
      }
    ])
  }, [])

  const value = {
    messages,
    isLoading,
    currentMachine,
    addMessage,
    clearMessages,
    setCurrentMachine,
    setIsLoading
  }

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  )
}

export function useChat() {
  const context = useContext(ChatContext)
  if (context === undefined) {
    throw new Error('useChat doit être utilisé dans un ChatProvider')
  }
  return context
} 