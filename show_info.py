"""
Script d'affichage des informations du projet Hockey Trainer
"""

def print_banner():
    """Affiche la bannière du projet"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🏒  HOCKEY TRAINER - Analyse Vidéo de Performance  🏒     ║
║                                                               ║
║                    Version 1.0 - Novembre 2025                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_project_info():
    """Affiche les informations du projet"""
    print("\n📦 PROJET INSTALLÉ AVEC SUCCÈS!\n")
    print("="*65)
    
    print("\n🎯 MODULES DISPONIBLES:")
    print("   ✅ ball_tracking.py          - Détection temps réel (webcam)")
    print("   ✅ ball_tracking_video.py    - Analyse de vidéos")
    print("   ✅ motion_detection.py       - Détection de mouvement")
    print("   ✅ webcam_test.py            - Test de caméra")
    print("   ✅ test_detection.py         - Tests et démos")
    
    print("\n🚀 LANCEURS:")
    print("   ⭐ start.bat                 - Double-clic pour lancer!")
    print("   ⭐ launcher.py               - Menu interactif Python")
    
    print("\n📚 DOCUMENTATION (8 fichiers):")
    print("   📄 DOC_INDEX.md              - Index de navigation")
    print("   📄 CHEATSHEET.md             - Aide-mémoire (1 min)")
    print("   📄 INSTALL_COMPLETE.md       - Statut installation (5 min)")
    print("   📄 QUICKSTART.md             - Démarrage rapide (10 min)")
    print("   📄 VISUAL_GUIDE.md           - Exemples visuels (15 min)")
    print("   📄 PROJECT_OVERVIEW.md       - Vue technique (20 min)")
    print("   📄 README.md                 - Documentation complète (30 min)")
    print("   📄 CODE_EXAMPLES.md          - Exemples de code")
    
    print("\n⚙️  CONFIGURATION:")
    print("   ✅ Python 3.14.0")
    print("   ✅ OpenCV 4.12.0")
    print("   ✅ NumPy 2.2.6")
    
    print("\n" + "="*65)

def print_quick_start():
    """Affiche le guide de démarrage rapide"""
    print("\n🚀 DÉMARRAGE RAPIDE:\n")
    
    print("1️⃣  Double-cliquez sur: start.bat")
    print("    OU")
    print("    Exécutez: python launcher.py")
    
    print("\n2️⃣  Pour tester rapidement:")
    print("    python test_detection.py")
    
    print("\n3️⃣  Pour utiliser votre webcam:")
    print("    python ball_tracking.py")
    
    print("\n4️⃣  Pour analyser une vidéo:")
    print("    python ball_tracking_video.py")

def print_keyboard_shortcuts():
    """Affiche les raccourcis clavier"""
    print("\n" + "="*65)
    print("\n⌨️  TOUCHES PRINCIPALES:\n")
    
    shortcuts = [
        ("Q", "Quitter l'application"),
        ("ESPACE", "Pause / Lecture (mode vidéo)"),
        ("+", "Augmenter la calibration"),
        ("-", "Diminuer la calibration"),
        ("R", "Réinitialiser le tracker"),
        ("→", "Frame suivante (en pause)"),
        ("C", "Afficher la calibration actuelle")
    ]
    
    for key, action in shortcuts:
        print(f"   {key:10s} → {action}")

def print_documentation_guide():
    """Affiche le guide de documentation"""
    print("\n" + "="*65)
    print("\n📖 QUELLE DOCUMENTATION LIRE?\n")
    
    print("   ⚡ Vous êtes pressé?")
    print("      → CHEATSHEET.md (1 minute)")
    
    print("\n   🌱 Vous débutez?")
    print("      → QUICKSTART.md (10 minutes)")
    
    print("\n   🎨 Vous voulez des exemples visuels?")
    print("      → VISUAL_GUIDE.md (15 minutes)")
    
    print("\n   📚 Vous voulez tout savoir?")
    print("      → README.md (30 minutes)")
    
    print("\n   💻 Vous êtes développeur?")
    print("      → CODE_EXAMPLES.md")
    
    print("\n   🗺️  Vous êtes perdu?")
    print("      → DOC_INDEX.md (guide de navigation)")

def print_features():
    """Affiche les fonctionnalités principales"""
    print("\n" + "="*65)
    print("\n✨ FONCTIONNALITÉS:\n")
    
    features = [
        "🎯 Détection de balle orange/rouge",
        "🚀 Calcul de vitesse en km/h",
        "📈 Vitesse instantanée, max, moyenne",
        "🎨 Visualisation de trajectoire",
        "📹 Temps réel (webcam) et vidéos",
        "⚙️  Calibration ajustable en direct",
        "📊 Rapport d'analyse détaillé",
        "💾 Export de vidéo annotée"
    ]
    
    for feature in features:
        print(f"   ✅ {feature}")

def print_next_steps():
    """Affiche les prochaines étapes"""
    print("\n" + "="*65)
    print("\n🎯 PROCHAINES ÉTAPES:\n")
    
    steps = [
        "1. Lisez CHEATSHEET.md ou QUICKSTART.md",
        "2. Lancez start.bat pour le menu interactif",
        "3. Testez avec python test_detection.py",
        "4. Essayez avec votre webcam",
        "5. Analysez vos propres vidéos",
        "6. Calibrez pour votre configuration",
        "7. Consultez CODE_EXAMPLES.md pour personnaliser"
    ]
    
    for step in steps:
        print(f"   {step}")

def print_footer():
    """Affiche le pied de page"""
    print("\n" + "="*65)
    print("\n🏒 HOCKEY TRAINER")
    print("   'Analyser pour mieux performer!'")
    print("\n   Version: 1.0")
    print("   Date: Novembre 2025")
    print("   Python: 3.14.0 | OpenCV: 4.12.0 | NumPy: 2.2.6")
    print("\n" + "="*65)
    print("\n✅ Tout est prêt! Bon entraînement! 🏒\n")

def main():
    """Fonction principale"""
    print_banner()
    print_project_info()
    print_quick_start()
    print_keyboard_shortcuts()
    print_documentation_guide()
    print_features()
    print_next_steps()
    print_footer()

if __name__ == "__main__":
    main()
