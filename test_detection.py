"""
Script de test rapide pour la détection de balle
Crée une simulation avec une balle qui se déplace
"""
import cv2
import numpy as np

def create_test_video(output_path='test_ball.mp4', duration_sec=5, fps=30):
    """
    Crée une vidéo de test avec une balle orange qui se déplace
    """
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration_sec * fps
    ball_radius = 15
    ball_color = (0, 140, 255)  # Orange en BGR
    
    print(f"🎬 Création d'une vidéo de test...")
    print(f"   Durée: {duration_sec}s, FPS: {fps}, Résolution: {width}x{height}")
    
    for frame_num in range(total_frames):
        # Fond blanc
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Dessiner une grille pour la calibration
        for i in range(0, width, 50):
            cv2.line(frame, (i, 0), (i, height), (200, 200, 200), 1)
        for i in range(0, height, 50):
            cv2.line(frame, (0, i), (width, i), (200, 200, 200), 1)
        
        # Position de la balle (trajectoire diagonale avec rebond)
        t = frame_num / total_frames
        
        # Mouvement horizontal (avec accélération)
        x = int(100 + (width - 200) * t)
        
        # Mouvement vertical (parabole)
        y = int(height // 2 + 150 * np.sin(t * 2 * np.pi))
        
        # Dessiner la balle
        cv2.circle(frame, (x, y), ball_radius, ball_color, -1)
        
        # Ajouter un effet de brillance
        highlight_pos = (x - ball_radius // 3, y - ball_radius // 3)
        cv2.circle(frame, highlight_pos, ball_radius // 4, (100, 200, 255), -1)
        
        # Ajouter des informations
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        cv2.putText(frame, "Test Video - Orange Ball", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        # Ajouter une échelle de référence (1 mètre = 100 pixels)
        cv2.line(frame, (width - 150, height - 50), (width - 50, height - 50), (0, 0, 0), 2)
        cv2.line(frame, (width - 150, height - 55), (width - 150, height - 45), (0, 0, 0), 2)
        cv2.line(frame, (width - 50, height - 55), (width - 50, height - 45), (0, 0, 0), 2)
        cv2.putText(frame, "1m (100px)", (width - 140, height - 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
        
        out.write(frame)
        
        # Afficher la progression
        if frame_num % fps == 0:
            print(f"   Progression: {int(t * 100)}%")
    
    out.release()
    print(f"✅ Vidéo de test créée: {output_path}")
    return output_path


def test_detection():
    """
    Test rapide de la détection avec la webcam
    """
    print("\n🧪 TEST DE DÉTECTION")
    print("="*50)
    print("Veuillez placer une balle orange/rouge devant la caméra")
    print("Appuyez sur 'q' pour quitter")
    print("="*50)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return
    
    # Plages de couleur
    lower_orange = np.array([5, 100, 100])
    upper_orange = np.array([25, 255, 255])
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir en HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Créer le masque
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        detected = False
        if len(contours) > 0:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 50:
                ((x, y), radius) = cv2.minEnclosingCircle(largest)
                if radius > 5:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                    cv2.putText(frame, "BALLE DETECTEE!", (int(x) - 70, int(y) - int(radius) - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    detected = True
        
        # Statut
        status = "DETECTE" if detected else "NON DETECTE"
        color = (0, 255, 0) if detected else (0, 0, 255)
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        # Afficher
        cv2.imshow("Test de detection", frame)
        cv2.imshow("Masque", mask)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Test terminé")


def main():
    """
    Menu principal
    """
    print("\n🏒 HOCKEY TRAINER - Tests")
    print("="*50)
    print("\n1. Créer une vidéo de test")
    print("2. Tester la détection en temps réel")
    print("3. Analyser la vidéo de test créée")
    print("4. Quitter")
    
    choice = input("\nVotre choix: ").strip()
    
    if choice == "1":
        duration = input("Durée de la vidéo (secondes, défaut=5): ").strip()
        duration = int(duration) if duration else 5
        video_path = create_test_video(duration_sec=duration)
        
        analyze = input("\nAnalyser cette vidéo maintenant? (o/n): ").strip().lower()
        if analyze == 'o':
            print("\nLancement de l'analyse...")
            import ball_tracking_video
            ball_tracking_video.analyze_video(video_path)
    
    elif choice == "2":
        test_detection()
    
    elif choice == "3":
        import os
        if os.path.exists('test_ball.mp4'):
            import ball_tracking_video
            ball_tracking_video.analyze_video('test_ball.mp4')
        else:
            print("❌ Aucune vidéo de test trouvée. Créez-en une d'abord (option 1)")
    
    elif choice == "4":
        print("👋 Au revoir!")
    
    else:
        print("❌ Choix invalide")


if __name__ == "__main__":
    main()
