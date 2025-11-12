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
        
        # Paramètres ajustables pour la détection
        self.hue_min = 20  # Ajusté selon vos tests
        self.hue_max = 35  # Légèrement élargi
        self.sat_min = 80  # Réduit pour détecter la balle à distance
        self.val_min = 100  # Réduit pour accepter des conditions variées
        self.min_circularity = 0.7  # Augmenté pour être plus strict sur la forme
        self.min_area = 50  # Réduit pour détecter la balle plus loin (apparaît plus petite)
        self.min_radius = 5  # Réduit pour détecter la balle lointaine
        self.max_radius = 150
        self.num_contours = 0  # Pour debug
        
    def detect_ball(self, frame):
        """
        Détecte la balle dans la frame en utilisant la détection de couleur
        Retourne (x, y, radius) ou None si non trouvée
        """
        # Convertir en HSV pour meilleure détection de couleur
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Plages de couleur pour une balle jaune vive - ajustables en temps réel
        lower_yellow = np.array([self.hue_min, self.sat_min, self.val_min])
        upper_yellow = np.array([self.hue_max, 255, 255])
        
        # Créer un masque pour la couleur jaune
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Nettoyer le masque avec morphologie plus agressive
        # Cela aide à éliminer les petits reflets
        kernel = np.ones((5, 5), np.uint8)  # Réduit pour garder les petites balles lointaines
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)  # Réduit aussi
        
        # Trouver les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        frame_height = frame.shape[0]
        
        if len(contours) > 0:
            # Filtrer les contours par circularité et taille avec scoring
            valid_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filtrer les contours trop petits (évite les petits reflets)
                if area < self.min_area:
                    continue
                
                # Calculer la circularité (4*pi*area/perimeter^2)
                # Une balle parfaite a une circularité de 1.0
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                    
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Filtrer les formes non circulaires (reflets allongés)
                if circularity > self.min_circularity:
                    # Calculer le cercle et sa position
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    
                    if radius < self.min_radius or radius > self.max_radius:
                        continue
                    
                    # Calculer la saturation moyenne dans la région
                    mask_region = np.zeros(hsv.shape[:2], dtype=np.uint8)
                    cv2.circle(mask_region, (int(x), int(y)), int(radius), 255, -1)
                    mean_sat = cv2.mean(hsv[:, :, 1], mask=mask_region)[0]
                    
                    # Système de scoring multi-critères
                    score = 0.0
                    
                    # Score basé sur la position verticale (plus bas = meilleur)
                    # Les balles au sol sont dans la partie basse, les reflets murs en haut
                    y_ratio = y / frame_height
                    score += y_ratio * 100  # 0-100 points (plus bas = plus de points)
                    
                    # Score basé sur la circularité (plus rond = meilleur)
                    score += circularity * 50  # 0-50 points
                    
                    # Score basé sur la saturation (plus saturé = meilleur)
                    score += (mean_sat / 255) * 50  # 0-50 points
                    
                    # Score basé sur la taille (plus gros = plus proche = meilleur)
                    score += (radius / self.max_radius) * 30  # 0-30 points
                    
                    valid_contours.append((contour, radius, circularity, score, mean_sat, y))
            
            if len(valid_contours) > 0:
                # Trier par score (plus haut = meilleur candidat)
                valid_contours.sort(key=lambda x: x[3], reverse=True)
                
                # Prendre le meilleur candidat
                best_contour, best_radius, _, _, _, _ = valid_contours[0]
                
                # Trouver le cercle minimum englobant
                ((x, y), radius) = cv2.minEnclosingCircle(best_contour)
                
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
        
        # Compter le nombre de contours pour debug
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.num_contours = len(contours)
        
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
    print("  - 'h': Afficher/Masquer l'aide")
    print("  - 'a/z': Ajuster Hue Min (Teinte)")
    print("  - 's/x': Ajuster Saturation Min")
    print("  - 'd/c': Ajuster Value Min (Luminosité)")
    print("  - 'f/v': Ajuster Circularité Min")
    print("  - '+/-': Augmenter/diminuer pixels_per_meter")
    
    tracker = BallTracker(max_positions=50)
    show_help = False
    
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
        
        # Afficher le nombre de contours détectés (debug)
        contour_text = f"Contours: {tracker.num_contours}"
        cv2.putText(frame, contour_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Afficher les paramètres de calibration
        calib_text = f"Calib: {tracker.pixels_per_meter} px/m"
        cv2.putText(frame, calib_text, (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Afficher les paramètres de détection (si aide activée)
        if show_help:
            y_offset = 90  # Ajusté pour le nouveau texte
            params_text = [
                f"Hue: {tracker.hue_min}-{tracker.hue_max} (a/z)",
                f"Sat: {tracker.sat_min}+ (s/x) <- IMPORTANT!",
                f"Val: {tracker.val_min}+ (d/c)",
                f"Circ: {tracker.min_circularity:.2f}+ (f/v)",
                f"Area: {tracker.min_area}+ px",
            ]
            for i, text in enumerate(params_text):
                cv2.putText(frame, text, (10, y_offset + i*25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 0), 1)
        
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
        elif key == ord('h'):
            show_help = not show_help
            print(f"� Aide: {'Affichée' if show_help else 'Masquée'}")
        # Ajustements de la teinte (Hue)
        elif key == ord('a'):
            tracker.hue_min = max(0, tracker.hue_min - 2)
            print(f"🎨 Hue Min: {tracker.hue_min}")
        elif key == ord('z'):
            tracker.hue_min = min(tracker.hue_max - 5, tracker.hue_min + 2)
            print(f"🎨 Hue Min: {tracker.hue_min}")
        # Ajustements de la saturation
        elif key == ord('s'):
            tracker.sat_min = max(0, tracker.sat_min - 10)
            print(f"💧 Saturation Min: {tracker.sat_min}")
        elif key == ord('x'):
            tracker.sat_min = min(255, tracker.sat_min + 10)
            print(f"💧 Saturation Min: {tracker.sat_min}")
        # Ajustements de la valeur (luminosité)
        elif key == ord('d'):
            tracker.val_min = max(0, tracker.val_min - 10)
            print(f"💡 Value Min: {tracker.val_min}")
        elif key == ord('c'):
            tracker.val_min = min(255, tracker.val_min + 10)
            print(f"💡 Value Min: {tracker.val_min}")
        # Ajustements de la circularité
        elif key == ord('f'):
            tracker.min_circularity = max(0.1, tracker.min_circularity - 0.05)
            print(f"⭕ Circularité Min: {tracker.min_circularity:.2f}")
        elif key == ord('v'):
            tracker.min_circularity = min(1.0, tracker.min_circularity + 0.05)
            print(f"⭕ Circularité Min: {tracker.min_circularity:.2f}")
        # Calibration pixels/mètre
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
