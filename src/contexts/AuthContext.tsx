'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  uid: string
  email: string
  displayName: string
  photoURL: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  signInWithGoogle: () => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simuler un utilisateur connecté pour le développement
    setUser({
      uid: 'dev-user-123',
      email: 'dev@example.com',
      displayName: 'Développeur',
      photoURL: 'https://via.placeholder.com/40'
    })
    setLoading(false)
  }, [])

  const signInWithGoogle = async () => {
    // Simulation de connexion
    setUser({
      uid: 'dev-user-123',
      email: 'dev@example.com',
      displayName: 'Développeur',
      photoURL: 'https://via.placeholder.com/40'
    })
  }

  const signOut = async () => {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, signInWithGoogle, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 