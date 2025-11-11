import cv2
import numpy as np
from collections import deque
import time

class BallTracker:
    def __init__(self, max_positions=30):
        """
        Initialise le tracker de balle
        max_positions: nombre de positions à garder en mémoire pour la trajectoire
        """
        self.positions = deque(maxlen=max_positions)
        self.timestamps = deque(maxlen=max_positions)
        self.ball_found = False
        self.speed_kmh = 0.0
        
        # Calibration: distance pixels -> mètres (à ajuster selon votre configuration)
        self.pixels_per_meter = 100  # À calibrer selon votre vidéo
        
    def detect_ball(self, frame):
        """
        Détecte la balle dans la frame en utilisant la détection de couleur
        Retourne (x, y, radius) ou None si non trouvée
        """
        # Convertir en HSV pour meilleure détection de couleur
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Plages de couleur pour une balle orange/rouge de hockey
        # Option 1: Orange
        lower_orange = np.array([5, 100, 100])
        upper_orange = np.array([25, 255, 255])
        
        # Option 2: Rouge (décommentez si balle rouge)
        # lower_red1 = np.array([0, 100, 100])
        # upper_red1 = np.array([10, 255, 255])
        # lower_red2 = np.array([160, 100, 100])
        # upper_red2 = np.array([180, 255, 255])
        
        # Créer un masque pour la couleur
        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
        
        # Si vous utilisez le rouge, combinez les masques:
        # mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        # mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        # mask = mask_red1 | mask_red2 | mask_orange
        
        mask = mask_orange
        
        # Nettoyer le masque avec morphologie
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Prendre le plus grand contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Filtrer les contours trop petits
            if cv2.contourArea(largest_contour) > 50:
                # Trouver le cercle minimum englobant
                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                
                # Filtrer les cercles trop petits ou trop grands
                if radius > 5 and radius < 100:
                    return (int(x), int(y), int(radius)), mask
        
        return None, mask
    
    def calculate_speed(self):
        """
        Calcule la vitesse de la balle en km/h basée sur les positions récentes
        """
        if len(self.positions) < 2:
            return 0.0
        
        # Prendre les 5 dernières positions pour un calcul plus stable
        num_points = min(5, len(self.positions))
        if num_points < 2:
            return 0.0
        
        # Calculer la distance totale parcourue
        total_distance_pixels = 0
        for i in range(-num_points + 1, 0):
            x1, y1 = self.positions[i-1]
            x2, y2 = self.positions[i]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            total_distance_pixels += distance
        
        # Calculer le temps écoulé
        time_elapsed = self.timestamps[-1] - self.timestamps[-num_points]
        
        if time_elapsed > 0:
            # Convertir en vitesse réelle
            distance_meters = total_distance_pixels / self.pixels_per_meter
            speed_ms = distance_meters / time_elapsed  # mètres par seconde
            speed_kmh = speed_ms * 3.6  # conversion en km/h
            return speed_kmh
        
        return 0.0
    
    def update(self, frame):
        """
        Met à jour le tracker avec une nouvelle frame
        """
        result, mask = self.detect_ball(frame)
        current_time = time.time()
        
        if result is not None:
            x, y, radius = result
            self.positions.append((x, y))
            self.timestamps.append(current_time)
            self.ball_found = True
            
            # Calculer la vitesse
            self.speed_kmh = self.calculate_speed()
            
            return (x, y, radius), mask
        else:
            self.ball_found = False
            return None, mask
    
    def draw_trajectory(self, frame):
        """
        Dessine la trajectoire de la balle
        """
        # Dessiner la trajectoire
        for i in range(1, len(self.positions)):
            thickness = int(np.sqrt(len(self.positions) / float(i + 1)) * 2)
            cv2.line(frame, self.positions[i-1], self.positions[i], (0, 255, 255), thickness)
    
    def draw_info(self, frame, position):
        """
        Affiche les informations sur la balle
        """
        if position is not None:
            x, y, radius = position
            
            # Dessiner le cercle autour de la balle
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            
            # Afficher la vitesse
            speed_text = f"Vitesse: {self.speed_kmh:.1f} km/h"
            cv2.putText(frame, speed_text, (x - 50, y - radius - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Afficher la position
            pos_text = f"Pos: ({x}, {y})"
            cv2.putText(frame, pos_text, (x - 50, y - radius - 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def main():
    """
    Programme principal pour tester la détection et le suivi de balle
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Impossible d'accéder à la caméra")
        return
    
    # Obtenir les propriétés de la vidéo
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30  # Valeur par défaut
    
    print(f"📹 Caméra ouverte (FPS: {fps})")
    print("📝 Touches:")
    print("  - 'q': Quitter")
    print("  - 'r': Réinitialiser le tracker")
    print("  - 'c': Calibrer (ajuster pixels par mètre)")
    print("  - '+/-': Augmenter/diminuer pixels_per_meter")
    
    tracker = BallTracker(max_positions=50)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de capture")
            break
        
        # Mettre à jour le tracker
        position, mask = tracker.update(frame)
        
        # Dessiner la trajectoire
        tracker.draw_trajectory(frame)
        
        # Dessiner les informations
        if position is not None:
            tracker.draw_info(frame, position)
            status_text = "BALLE DÉTECTÉE"
            status_color = (0, 255, 0)
        else:
            status_text = "RECHERCHE..."
            status_color = (0, 0, 255)
        
        # Afficher le statut
        cv2.putText(frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        
        # Afficher les paramètres de calibration
        calib_text = f"Calibration: {tracker.pixels_per_meter} px/m"
        cv2.putText(frame, calib_text, (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Afficher les frames
        cv2.imshow("Détection de balle - Hockey Trainer", frame)
        cv2.imshow("Masque de couleur", mask)
        
        # Gestion des touches
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            tracker = BallTracker(max_positions=50)
            print("🔄 Tracker réinitialisé")
        elif key == ord('c'):
            print(f"📏 Calibration actuelle: {tracker.pixels_per_meter} pixels/mètre")
            print("   Utilisez +/- pour ajuster")
        elif key == ord('+') or key == ord('='):
            tracker.pixels_per_meter += 10
            print(f"📏 Pixels/mètre: {tracker.pixels_per_meter}")
        elif key == ord('-') or key == ord('_'):
            tracker.pixels_per_meter = max(10, tracker.pixels_per_meter - 10)
            print(f"📏 Pixels/mètre: {tracker.pixels_per_meter}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Application fermée")


if __name__ == "__main__":
    main()
