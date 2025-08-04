import { getStorage } from 'firebase/storage'
import app from './firebase'

// Initialize Firebase Storage (server-side only)
export const storage = getStorage(app) 