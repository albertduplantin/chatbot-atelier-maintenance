#!/bin/bash

# 🚀 Script de Déploiement Automatique
# Chatbot Atelier Maintenance - Next.js + Firebase

set -e  # Arrêter en cas d'erreur

echo "🚀 Démarrage du déploiement..."

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "package.json" ]; then
    log_error "package.json non trouvé. Assurez-vous d'être dans le répertoire du projet."
    exit 1
fi

# Vérifier que Git est initialisé
if [ ! -d ".git" ]; then
    log_error "Git n'est pas initialisé. Exécutez 'git init' d'abord."
    exit 1
fi

# Vérifier les dépendances
log_info "Vérification des dépendances..."
if [ ! -d "node_modules" ]; then
    log_warning "node_modules non trouvé. Installation des dépendances..."
    npm install
else
    log_success "Dépendances déjà installées"
fi

# Vérifier la configuration Firebase
log_info "Vérification de la configuration Firebase..."
if [ ! -f "src/lib/firebase.ts" ]; then
    log_error "Configuration Firebase manquante"
    exit 1
fi

# Build de test
log_info "Test du build..."
if npm run build; then
    log_success "Build réussi"
else
    log_error "Échec du build"
    exit 1
fi

# Vérifier le statut Git
log_info "Vérification du statut Git..."
if [ -n "$(git status --porcelain)" ]; then
    log_warning "Changements non commités détectés"
    echo "Changements détectés :"
    git status --short
    
    read -p "Voulez-vous commiter ces changements ? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "🚀 Auto-commit avant déploiement"
        log_success "Changements commités"
    else
        log_warning "Déploiement annulé"
        exit 1
    fi
else
    log_success "Aucun changement non commité"
fi

# Vérifier la branche
CURRENT_BRANCH=$(git branch --show-current)
log_info "Branche actuelle: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    log_warning "Vous n'êtes pas sur la branche principale"
    read -p "Voulez-vous continuer sur la branche $CURRENT_BRANCH ? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_warning "Déploiement annulé"
        exit 1
    fi
fi

# Push vers GitHub
log_info "Push vers GitHub..."
if git push origin $CURRENT_BRANCH; then
    log_success "Code poussé vers GitHub"
else
    log_error "Échec du push vers GitHub"
    exit 1
fi

# Vérifier si Vercel CLI est installé
if command -v vercel &> /dev/null; then
    log_info "Déploiement via Vercel CLI..."
    if vercel --prod; then
        log_success "Déploiement Vercel réussi"
    else
        log_warning "Échec du déploiement Vercel CLI"
        log_info "Le déploiement se fera automatiquement via GitHub"
    fi
else
    log_info "Vercel CLI non installé. Le déploiement se fera automatiquement via GitHub"
fi

# Afficher les informations finales
log_success "🎉 Déploiement terminé !"
echo ""
echo "📋 Prochaines étapes :"
echo "1. Vérifiez le déploiement sur Vercel Dashboard"
echo "2. Testez l'application en ligne"
echo "3. Vérifiez les variables d'environnement"
echo "4. Configurez Firebase pour la production"
echo ""
echo "🔗 Liens utiles :"
echo "- Vercel Dashboard: https://vercel.com/dashboard"
echo "- Firebase Console: https://console.firebase.google.com/"
echo "- GitHub Repository: $(git remote get-url origin)"
echo ""

# Vérifier les variables d'environnement
log_info "Vérification des variables d'environnement..."
if [ -f ".env.local" ]; then
    log_warning "Fichier .env.local détecté localement"
    echo "Assurez-vous que les variables sont configurées dans Vercel Dashboard"
else
    log_warning "Aucun fichier .env.local détecté"
    echo "Configurez les variables d'environnement dans Vercel Dashboard"
fi

log_success "Script de déploiement terminé ! 🚀" 