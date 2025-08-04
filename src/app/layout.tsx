import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'sonner'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '🔧 Chatbot Atelier Maintenance',
  description: 'Assistant IA pour la maintenance industrielle avec analyse de schémas électriques',
  keywords: ['maintenance', 'industrielle', 'IA', 'schémas', 'électriques', 'chatbot'],
  authors: [{ name: 'Atelier Maintenance' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          {children}
        </div>
        <Toaster 
          position="top-right"
          richColors
          closeButton
          duration={4000}
        />
      </body>
    </html>
  )
} 