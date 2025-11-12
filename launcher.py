# Hockey Trainer - Lanceur Principal
# Script pour lancer facilement les différents modules

import sys
import subprocess
import importlib.util

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    dependencies = {
        'cv2': 'opencv-python',
        'numpy': 'numpy'
    }
    
    missing = []
    
    for module, package in dependencies.items():
        if importlib.util.find_spec(module) is None:
            missing.append(package)
            print(f"   ❌ {package} n'est pas installé")
        else:
            print(f"   ✅ {package}")
    
    if missing:
        print("\n⚠️  Dépendances manquantes détectées!")
        print(f"   Packages manquants: {', '.join(missing)}")
        install = input("\n   Installer automatiquement? (o/n): ").strip().lower()
        
        if install == 'o':
            print("\n📦 Installation en cours...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
                print("✅ Installation réussie!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Erreur lors de l'installation")
                print("   Installez manuellement avec: pip install opencv-python numpy")
                return False
        else:
            print("\n⚠️  Installez les dépendances avec:")
            print(f"   pip install {' '.join(missing)}")
            return False
    
    print("✅ Toutes les dépendances sont installées!\n")
    return True


def show_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("🏒 HOCKEY TRAINER - Analyse Vidéo de Performance")
    print("="*60)
    print("\n📋 MODULES DISPONIBLES:\n")
    print("1. 📹 Test de la webcam")
    print("   → Vérifiez que votre caméra fonctionne")
    print()
    print("2. 👁️  Détection de mouvement")
    print("   → Détecte les zones de mouvement dans la vidéo")
    print()
    print("3. 🎯 Détection de balle (Temps réel)")
    print("   → Détecte et suit une balle jaune via webcam")
    print("   → Calcule la vitesse en km/h")
    print()
    print("4. 🏒 Reconnaissance d'actions (NOUVEAU!)")
    print("   → Détecte TIR, PASSE, DRIBBLE avec tracking de balle")
    print("   → Combine détection de posture et suivi de balle")
    print()
    print("5. 📊 Analyse de vidéo")
    print("   → Analyse une vidéo existante")
    print("   → Génère un rapport avec statistiques")
    print()
    print("6. 🧪 Tests et démonstration")
    print("   → Créer une vidéo de test")
    print("   → Tester la détection")
    print()
    print("7. 📖 Aide et documentation")
    print()
    print("0. ❌ Quitter")
    print()
    print("="*60)


def run_module(module_name):
    """Lance un module spécifique"""
    try:
        if module_name == "webcam_test":
            import webcam_test
            webcam_test
            subprocess.run([sys.executable, "webcam_test.py"])
        
        elif module_name == "motion_detection":
            import motion_detection
            motion_detection
            subprocess.run([sys.executable, "motion_detection.py"])
        
        elif module_name == "ball_tracking":
            import ball_tracking
            ball_tracking.main()
        
        elif module_name == "action_recognition":
            import action_recognition
            action_recognition.main()
        
        elif module_name == "ball_tracking_video":
            import ball_tracking_video
            ball_tracking_video.main()
        
        elif module_name == "test_detection":
            import test_detection
            test_detection.main()
        
    except ImportError as e:
        print(f"❌ Erreur: Impossible d'importer le module {module_name}")
        print(f"   Détails: {e}")
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")


def show_help():
    """Affiche l'aide"""
    print("\n" + "="*60)
    print("📖 AIDE - HOCKEY TRAINER")
    print("="*60)
    print()
    print("🎯 DÉTECTION DE BALLE:")
    print("   La détection fonctionne avec des balles JAUNE VIVE.")
    print("   Optimisée pour éliminer les reflets sur murs et parquet.")
    print("   Assurez-vous d'avoir un bon éclairage.")
    print()
    print("🏒 RECONNAISSANCE D'ACTIONS:")
    print("   Combine détection de posture (MediaPipe) et tracking de balle.")
    print("   Détecte automatiquement: TIR, PASSE, DRIBBLE")
    print("   Ajustez la détection de balle avec s/x et d/c en temps réel.")
    print()
    print("⚙️  CALIBRATION:")
    print("   La vitesse dépend de la calibration 'pixels_per_meter'.")
    print("   Utilisez +/- pendant l'exécution pour ajuster.")
    print()
    print("🎮 TOUCHES COMMUNES:")
    print("   Q      → Quitter")
    print("   ESPACE → Pause (mode vidéo)")
    print("   +/-    → Ajuster calibration")
    print()
    print("📁 FICHIERS:")
    print("   requirements.txt  → Dépendances Python")
    print("   README.md         → Documentation complète")
    print()
    print("🔧 INSTALLATION:")
    print("   pip install -r requirements.txt")
    print()
    print("="*60)
    input("\nAppuyez sur ENTRÉE pour continuer...")


def main():
    """Fonction principale"""
    # Vérifier les dépendances au démarrage
    if not check_dependencies():
        input("\nAppuyez sur ENTRÉE pour quitter...")
        return
    
    while True:
        show_menu()
        choice = input("Votre choix: ").strip()
        
        if choice == "1":
            print("\n🚀 Lancement du test webcam...")
            run_module("webcam_test")
        
        elif choice == "2":
            print("\n🚀 Lancement de la détection de mouvement...")
            run_module("motion_detection")
        
        elif choice == "3":
            print("\n🚀 Lancement de la détection de balle en temps réel...")
            run_module("ball_tracking")
        
        elif choice == "4":
            print("\n🚀 Lancement de la reconnaissance d'actions...")
            run_module("action_recognition")
        
        elif choice == "5":
            print("\n🚀 Lancement de l'analyse vidéo...")
            run_module("ball_tracking_video")
        
        elif choice == "6":
            print("\n🚀 Lancement des tests...")
            run_module("test_detection")
        
        elif choice == "7":
            show_help()
        
        elif choice == "0":
            print("\n👋 Merci d'avoir utilisé Hockey Trainer!")
            print("   Bon entraînement! 🏒\n")
            break
        
        else:
            print("\n❌ Choix invalide. Veuillez choisir un numéro entre 0 et 7.")
            input("Appuyez sur ENTRÉE pour continuer...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption détectée. Au revoir!")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        input("Appuyez sur ENTRÉE pour quitter...")
