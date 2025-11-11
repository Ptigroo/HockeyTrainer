import cv2
import numpy as np
from collections import deque
import time
import os

class BallTrackerVideo:
    def __init__(self, max_positions=50):
        """
        Tracker de balle optimisé pour analyse vidéo
        """
        self.positions = deque(maxlen=max_positions)
        self.frame_numbers = deque(maxlen=max_positions)
        self.ball_found = False
        self.speed_kmh = 0.0
        self.max_speed = 0.0
        self.avg_speed = 0.0
        self.speed_history = []
        
        # Calibration (à ajuster selon la vidéo)
        self.pixels_per_meter = 100
        self.fps = 30
        
    def detect_ball(self, frame):
        """
        Détecte la balle dans la frame
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Plages de couleur pour balle orange/rouge
        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([25, 255, 255])
        
        # Masque pour la couleur
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Nettoyer le masque
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > 50:
                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                
                if radius > 5 and radius < 100:
                    return (int(x), int(y), int(radius)), mask
        
        return None, mask
    
    def calculate_speed(self, frame_number):
        """
        Calcule la vitesse basée sur les positions et numéros de frames
        """
        if len(self.positions) < 2:
            return 0.0
        
        num_points = min(5, len(self.positions))
        if num_points < 2:
            return 0.0
        
        # Distance parcourue
        total_distance_pixels = 0
        for i in range(-num_points + 1, 0):
            x1, y1 = self.positions[i-1]
            x2, y2 = self.positions[i]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance_pixels += distance
        
        # Temps écoulé basé sur les frames
        frames_elapsed = self.frame_numbers[-1] - self.frame_numbers[-num_points]
        time_elapsed = frames_elapsed / self.fps
        
        if time_elapsed > 0:
            distance_meters = total_distance_pixels / self.pixels_per_meter
            speed_ms = distance_meters / time_elapsed
            speed_kmh = speed_ms * 3.6
            return speed_kmh
        
        return 0.0
    
    def update(self, frame, frame_number):
        """
        Met à jour le tracker
        """
        result, mask = self.detect_ball(frame)
        
        if result is not None:
            x, y, radius = result
            self.positions.append((x, y))
            self.frame_numbers.append(frame_number)
            self.ball_found = True
            
            # Calculer la vitesse
            self.speed_kmh = self.calculate_speed(frame_number)
            
            if self.speed_kmh > 0:
                self.speed_history.append(self.speed_kmh)
                self.max_speed = max(self.max_speed, self.speed_kmh)
                self.avg_speed = np.mean(self.speed_history)
            
            return (x, y, radius), mask
        else:
            self.ball_found = False
            return None, mask
    
    def draw_trajectory(self, frame):
        """
        Dessine la trajectoire
        """
        for i in range(1, len(self.positions)):
            thickness = int(np.sqrt(len(self.positions) / float(i + 1)) * 2)
            cv2.line(frame, self.positions[i-1], self.positions[i], (0, 255, 255), thickness)
    
    def draw_info(self, frame, position):
        """
        Affiche les informations détaillées
        """
        if position is not None:
            x, y, radius = position
            
            # Cercle autour de la balle
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            
            # Vitesse instantanée
            speed_text = f"Vitesse: {self.speed_kmh:.1f} km/h"
            cv2.putText(frame, speed_text, (x - 50, y - radius - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Statistiques globales
        stats_y = 30
        cv2.putText(frame, f"Vitesse max: {self.max_speed:.1f} km/h", (10, stats_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Vitesse moy: {self.avg_speed:.1f} km/h", (10, stats_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def analyze_video(video_path, output_path=None):
    """
    Analyse une vidéo et génère un rapport
    """
    if not os.path.exists(video_path):
        print(f"❌ Fichier vidéo non trouvé: {video_path}")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Impossible d'ouvrir la vidéo: {video_path}")
        return
    
    # Propriétés de la vidéo
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"📹 Vidéo: {video_path}")
    print(f"   FPS: {fps}, Frames: {total_frames}, Résolution: {width}x{height}")
    
    tracker = BallTrackerVideo(max_positions=100)
    tracker.fps = fps
    
    # Préparer l'enregistrement vidéo si demandé
    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"💾 Enregistrement vers: {output_path}")
    
    frame_number = 0
    paused = False
    
    print("\n📝 Touches:")
    print("  - ESPACE: Pause/Lecture")
    print("  - 'q': Quitter")
    print("  - '+/-': Ajuster calibration")
    print("  - Flèche droite: Frame suivante (en pause)")
    print("\n▶️  Analyse en cours...\n")
    
    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("✅ Fin de la vidéo")
                break
            
            frame_number += 1
        else:
            # En pause, on utilise la dernière frame
            ret = True
        
        # Analyse
        position, mask = tracker.update(frame.copy(), frame_number)
        
        # Dessiner
        display_frame = frame.copy()
        tracker.draw_trajectory(display_frame)
        tracker.draw_info(display_frame, position)
        
        # Barre de progression
        progress = int((frame_number / total_frames) * 100)
        cv2.rectangle(display_frame, (10, height - 30), (width - 10, height - 10), (50, 50, 50), -1)
        cv2.rectangle(display_frame, (10, height - 30), (10 + int((width - 20) * progress / 100), height - 10), (0, 255, 0), -1)
        cv2.putText(display_frame, f"{progress}%", (width // 2 - 30, height - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Indicateur pause
        if paused:
            cv2.putText(display_frame, "PAUSE", (width - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Afficher
        cv2.imshow("Analyse vidéo - Hockey Trainer", display_frame)
        
        # Enregistrer si demandé
        if out is not None and not paused:
            out.write(display_frame)
        
        # Gestion des touches
        key = cv2.waitKey(1 if not paused else 0) & 0xFF
        
        if key == ord('q'):
            print("⏹️  Arrêt demandé")
            break
        elif key == ord(' '):  # ESPACE pour pause
            paused = not paused
            print("⏸️  Pause" if paused else "▶️  Lecture")
        elif key == 83:  # Flèche droite
            if paused:
                paused = False
                ret, frame = cap.read()
                if ret:
                    frame_number += 1
                paused = True
        elif key == ord('+') or key == ord('='):
            tracker.pixels_per_meter += 10
            print(f"📏 Calibration: {tracker.pixels_per_meter} px/m")
        elif key == ord('-'):
            tracker.pixels_per_meter = max(10, tracker.pixels_per_meter - 10)
            print(f"📏 Calibration: {tracker.pixels_per_meter} px/m")
    
    # Rapport final
    print("\n" + "="*50)
    print("📊 RAPPORT D'ANALYSE")
    print("="*50)
    print(f"Vitesse maximale: {tracker.max_speed:.1f} km/h")
    print(f"Vitesse moyenne: {tracker.avg_speed:.1f} km/h")
    print(f"Positions détectées: {len(tracker.speed_history)}")
    print(f"Calibration utilisée: {tracker.pixels_per_meter} pixels/mètre")
    print("="*50)
    
    cap.release()
    if out is not None:
        out.release()
        print(f"✅ Vidéo sauvegardée: {output_path}")
    
    cv2.destroyAllWindows()


def main():
    """
    Programme principal
    """
    print("🏒 HOCKEY TRAINER - Analyse de balle")
    print("="*50)
    print("\nChoisissez le mode:")
    print("1. Analyse d'une vidéo existante")
    print("2. Webcam en direct")
    
    choice = input("\nVotre choix (1 ou 2): ").strip()
    
    if choice == "1":
        video_path = input("Chemin de la vidéo: ").strip().strip('"')
        save_output = input("Sauvegarder la vidéo analysée? (o/n): ").strip().lower()
        
        output_path = None
        if save_output == 'o':
            output_path = input("Chemin de sortie (ex: output.mp4): ").strip()
        
        analyze_video(video_path, output_path)
    
    elif choice == "2":
        print("\n⚠️  Pour la webcam, utilisez 'ball_tracking.py'")
        import ball_tracking
        ball_tracking.main()
    
    else:
        print("❌ Choix invalide")


if __name__ == "__main__":
    main()
