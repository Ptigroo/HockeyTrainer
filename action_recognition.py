"""
Reconnaissance d'actions de hockey (tir, passe, dribble)
Combine la détection de balle et la détection de posture pour classifier les actions
"""
import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque
import time
from ball_tracking import BallTracker


def calculate_distance(point1, point2):
    """
    Calcule la distance euclidienne entre deux points
    
    Args:
        point1, point2: Tuples (x, y)
    
    Returns:
        Distance en pixels
    """
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def calculate_angle(a, b, c):
    """
    Calcule l'angle au point b formé par les points a, b, c
    
    Args:
        a, b, c: Points avec attributs x, y (landmarks MediaPipe)
    
    Returns:
        Angle en degrés (0-180)
    """
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    
    dot_product = np.dot(ba, bc)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    
    if norm_ba == 0 or norm_bc == 0:
        return 0
    
    cosine_angle = dot_product / (norm_ba * norm_bc)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)


class ActionRecognizer:
    def __init__(self):
        """
        Initialise le système de reconnaissance d'actions
        """
        # MediaPipe Pose pour la détection de posture
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )
        
        # Utiliser le BallTracker amélioré avec détection de balle jaune
        self.ball_tracker = BallTracker(max_positions=30)
        
        # Historique pour l'analyse temporelle (positions gérées par BallTracker)
        self.ball_speeds = deque(maxlen=10)
        
        # État de l'action actuelle
        self.current_action = "AUCUNE"
        self.action_confidence = 0.0
        self.action_start_time = None
        
        # Seuils de détection (ajustables)
        self.dribble_max_distance = 150  # pixels
        self.pass_min_speed = 20  # km/h
        self.shoot_min_speed = 50  # km/h
        
    def detect_ball(self, frame):
        """
        Détecte la balle dans la frame en utilisant le BallTracker amélioré
        
        Returns:
            (x, y, radius) ou None si non trouvée
        """
        # Utiliser le BallTracker avec détection optimisée pour balle jaune
        position, mask = self.ball_tracker.update(frame)
        return position
    
    def get_player_center(self, landmarks, image_w, image_h):
        """
        Calcule le centre du joueur (milieu du torse)
        
        Args:
            landmarks: Liste des landmarks MediaPipe
            image_w, image_h: Dimensions de l'image
        
        Returns:
            (x, y) en pixels ou None
        """
        if landmarks is None:
            return None
        
        # Utiliser le milieu entre les hanches
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        
        center_x = int((left_hip.x + right_hip.x) / 2 * image_w)
        center_y = int((left_hip.y + right_hip.y) / 2 * image_h)
        
        return (center_x, center_y)
    
    def calculate_ball_speed(self):
        """
        Calcule la vitesse de la balle en km/h en utilisant le BallTracker
        
        Returns:
            Vitesse en km/h
        """
        # Utiliser la vitesse calculée par le BallTracker
        return self.ball_tracker.speed_kmh
    
    def get_arm_extension(self, landmarks):
        """
        Mesure l'extension du bras (pour détecter une passe ou un tir)
        
        Returns:
            Angle du coude droit en degrés
        """
        if landmarks is None:
            return 180.0
        
        # Bras droit: épaule (12), coude (14), poignet (16)
        right_shoulder = landmarks[12]
        right_elbow = landmarks[14]
        right_wrist = landmarks[16]
        
        elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        return elbow_angle
    
    def classify_action(self, ball_pos, player_pos, ball_speed, arm_angle, body_lean):
        """
        Classifie l'action basée sur les données collectées
        
        Args:
            ball_pos: Position de la balle (x, y) ou None
            player_pos: Position du joueur (x, y) ou None
            ball_speed: Vitesse de la balle en km/h
            arm_angle: Angle du coude en degrés
            body_lean: Inclinaison du corps en degrés
        
        Returns:
            (action, confidence): Nom de l'action et niveau de confiance (0-1)
        """
        if ball_pos is None or player_pos is None:
            return "AUCUNE", 0.0
        
        # Calculer la distance balle-joueur
        distance = calculate_distance(ball_pos, player_pos)
        
        # TIR: Balle s'éloigne rapidement du joueur avec bras tendu
        if ball_speed > self.shoot_min_speed:
            # Vérifier si la balle s'éloigne (comparer avec position précédente)
            if len(self.ball_tracker.positions) >= 2:
                prev_distance = calculate_distance(
                    (self.ball_tracker.positions[-2][0], self.ball_tracker.positions[-2][1]),
                    player_pos
                )
                if distance > prev_distance:
                    # Balle s'éloigne avec grande vitesse = TIR
                    confidence = min(1.0, ball_speed / 80.0)
                    return "TIR", confidence
        
        # PASSE: Vitesse moyenne avec bras en extension
        if self.pass_min_speed < ball_speed < self.shoot_min_speed:
            if arm_angle > 140:  # Bras tendu
                confidence = min(1.0, ball_speed / 40.0)
                return "PASSE", confidence
        
        # DRIBBLE: Balle proche du joueur avec mouvement
        if distance < self.dribble_max_distance:
            if ball_speed > 5:  # Minimum de mouvement
                # Vérifier que la balle reste proche
                if len(self.ball_tracker.positions) >= 5:
                    recent_distances = []
                    for i in range(-5, 0):
                        dist = calculate_distance(
                            (self.ball_tracker.positions[i][0], self.ball_tracker.positions[i][1]),
                            player_pos
                        )
                        recent_distances.append(dist)
                    
                    avg_distance = np.mean(recent_distances)
                    if avg_distance < self.dribble_max_distance:
                        confidence = max(0.5, 1.0 - (avg_distance / self.dribble_max_distance))
                        return "DRIBBLE", confidence
        
        return "AUCUNE", 0.0
    
    def update(self, frame):
        """
        Met à jour la reconnaissance d'action avec une nouvelle frame
        
        Args:
            frame: Frame BGR d'OpenCV
        
        Returns:
            Tuple (action, confidence, annotated_frame)
        """
        current_time = time.time()
        image_h, image_w, _ = frame.shape
        
        # Copie pour annotation
        annotated_frame = frame.copy()
        
        # 1. Détecter la posture du joueur
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        pose_results = self.pose.process(image_rgb)
        image_rgb.flags.writeable = True
        
        player_pos = None
        arm_angle = 180.0
        body_lean = 0.0
        
        if pose_results.pose_landmarks:
            # Dessiner le squelette
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                pose_results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            landmarks = pose_results.pose_landmarks.landmark
            player_pos = self.get_player_center(landmarks, image_w, image_h)
            arm_angle = self.get_arm_extension(landmarks)
            
            # Calculer l'inclinaison du corps
            right_shoulder = landmarks[12]
            right_hip = landmarks[24]
            dx = right_shoulder.x - right_hip.x
            dy = right_shoulder.y - right_hip.y
            if dy != 0:
                body_lean = abs(math.degrees(math.atan(dx / dy)))
        
        # 2. Détecter la balle avec le BallTracker amélioré
        ball_result = self.detect_ball(frame)
        ball_pos = None
        
        if ball_result is not None:
            x, y, radius = ball_result
            ball_pos = (x, y)
            
            # Dessiner la balle avec la trajectoire
            self.ball_tracker.draw_trajectory(annotated_frame)
            cv2.circle(annotated_frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(annotated_frame, (x, y), 5, (0, 0, 255), -1)
        
        # 3. Calculer la vitesse de la balle
        ball_speed = self.calculate_ball_speed()
        if ball_speed > 0:
            self.ball_speeds.append(ball_speed)
        
        # 4. Dessiner la position du joueur
        if player_pos is not None:
            cv2.circle(annotated_frame, player_pos, 10, (255, 0, 0), -1)
            cv2.putText(annotated_frame, "Joueur", (player_pos[0] - 30, player_pos[1] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # 5. Classifier l'action
        action, confidence = self.classify_action(
            ball_pos, player_pos, ball_speed, arm_angle, body_lean
        )
        
        # Appliquer un seuil de confiance minimum
        if confidence < 0.4:
            action = "AUCUNE"
            confidence = 0.0
        else:
            # Mettre à jour l'action courante
            if action != self.current_action:
                self.current_action = action
                self.action_start_time = current_time
        
        self.action_confidence = confidence
        
        return action, confidence, annotated_frame
    
    def draw_info(self, frame, action, confidence):
        """
        Dessine les informations d'action sur la frame
        
        Args:
            frame: Frame à annoter
            action: Nom de l'action
            confidence: Niveau de confiance
        """
        # Couleur selon l'action
        if action == "TIR":
            color = (0, 0, 255)  # Rouge
        elif action == "PASSE":
            color = (255, 165, 0)  # Orange
        elif action == "DRIBBLE":
            color = (0, 255, 0)  # Vert
        else:
            color = (128, 128, 128)  # Gris
        
        # Afficher l'action détectée
        action_text = f"Action: {action}"
        cv2.putText(frame, action_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3, cv2.LINE_AA)
        
        # Afficher la confiance si action détectée
        if action != "AUCUNE":
            conf_text = f"Confiance: {confidence:.0%}"
            cv2.putText(frame, conf_text, (10, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
        
        # Afficher la vitesse de la balle si disponible
        if len(self.ball_speeds) > 0:
            speed = self.ball_speeds[-1]
            speed_text = f"Vitesse balle: {speed:.1f} km/h"
            cv2.putText(frame, speed_text, (10, 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Afficher les instructions
        help_text = "Q: Quitter | R: Reset"
        cv2.putText(frame, help_text, (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    
    def reset(self):
        """
        Réinitialise l'état du reconnaisseur
        """
        self.ball_tracker = BallTracker(max_positions=30)
        self.ball_speeds.clear()
        self.current_action = "AUCUNE"
        self.action_confidence = 0.0
        self.action_start_time = None
    
    def close(self):
        """
        Libère les ressources
        """
        self.pose.close()


def main():
    """
    Programme principal pour tester la reconnaissance d'actions
    """
    print("🏒 Reconnaissance d'Actions - Hockey Trainer")
    print("=" * 60)
    print("Détection: TIR, PASSE, DRIBBLE")
    print("Touches:")
    print("  - 'q': Quitter")
    print("  - 'r': Réinitialiser")
    print("  - 's/x': Ajuster Saturation balle (si mauvaise détection)")
    print("  - 'd/c': Ajuster Luminosité balle")
    print("  - 'h': Afficher les paramètres de détection")
    print("=" * 60)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return
    
    recognizer = ActionRecognizer()
    show_ball_params = False
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Erreur de lecture de la frame")
                break
            
            # Mettre à jour la reconnaissance
            action, confidence, annotated_frame = recognizer.update(frame)
            
            # Dessiner les informations
            recognizer.draw_info(annotated_frame, action, confidence)
            
            # Afficher les paramètres de détection de balle si demandé
            if show_ball_params:
                y_offset = 160
                params = [
                    f"Balle Hue: {recognizer.ball_tracker.hue_min}-{recognizer.ball_tracker.hue_max}",
                    f"Balle Sat: {recognizer.ball_tracker.sat_min}+ (s/x)",
                    f"Balle Val: {recognizer.ball_tracker.val_min}+ (d/c)",
                    f"Contours: {recognizer.ball_tracker.num_contours}",
                ]
                for i, text in enumerate(params):
                    cv2.putText(annotated_frame, text, (10, y_offset + i*25),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
            # Afficher
            cv2.imshow('Reconnaissance d\'Actions - Hockey Trainer', annotated_frame)
            
            # Gestion des touches
            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                recognizer.reset()
                print("🔄 Reconnaisseur réinitialisé")
            elif key == ord('h'):
                show_ball_params = not show_ball_params
                print(f"📋 Paramètres balle: {'Affichés' if show_ball_params else 'Masqués'}")
            # Ajustements de la saturation pour la détection de balle
            elif key == ord('s'):
                recognizer.ball_tracker.sat_min = max(0, recognizer.ball_tracker.sat_min - 10)
                print(f"💧 Saturation balle: {recognizer.ball_tracker.sat_min}")
            elif key == ord('x'):
                recognizer.ball_tracker.sat_min = min(255, recognizer.ball_tracker.sat_min + 10)
                print(f"💧 Saturation balle: {recognizer.ball_tracker.sat_min}")
            # Ajustements de la luminosité pour la détection de balle
            elif key == ord('d'):
                recognizer.ball_tracker.val_min = max(0, recognizer.ball_tracker.val_min - 10)
                print(f"💡 Luminosité balle: {recognizer.ball_tracker.val_min}")
            elif key == ord('c'):
                recognizer.ball_tracker.val_min = min(255, recognizer.ball_tracker.val_min + 10)
                print(f"💡 Luminosité balle: {recognizer.ball_tracker.val_min}")
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
        recognizer.close()
        print("✅ Session terminée")


if __name__ == "__main__":
    main()
