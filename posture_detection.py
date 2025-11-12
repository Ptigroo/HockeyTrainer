"""
Détection et classification de posture de joueur de hockey en temps réel
Utilise MediaPipe Pose pour détecter 33 landmarks du corps
"""
import cv2
import mediapipe as mp
import numpy as np
import math


def calculate_angle(a, b, c):
    """
    Calcule l'angle au point b formé par les points a, b, c
    
    Args:
        a, b, c: Points avec attributs x, y (landmarks MediaPipe)
    
    Returns:
        Angle en degrés (0-180)
    """
    # Convertir les coordonnées en vecteurs
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])
    
    # Calculer le produit scalaire et les normes
    dot_product = np.dot(ba, bc)
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    
    # Éviter la division par zéro
    if norm_ba == 0 or norm_bc == 0:
        return 0
    
    # Calculer l'angle
    cosine_angle = dot_product / (norm_ba * norm_bc)
    # S'assurer que la valeur est dans [-1, 1] pour éviter les erreurs d'arrondi
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)


def torso_lean_angle(shoulder, hip):
    """
    Mesure l'inclinaison du tronc par rapport à la verticale
    
    Args:
        shoulder: Landmark de l'épaule
        hip: Landmark de la hanche
    
    Returns:
        Angle d'inclinaison en degrés (0 = vertical)
    """
    # Calculer l'angle entre la ligne épaule-hanche et la verticale
    dx = shoulder.x - hip.x
    dy = shoulder.y - hip.y
    
    # Éviter la division par zéro
    if dy == 0:
        return 90.0
    
    # Calculer l'angle par rapport à la verticale
    angle = abs(math.degrees(math.atan(dx / dy)))
    
    return angle


def classify_posture(landmarks, image_w, image_h):
    """
    Classifie la posture selon des règles heuristiques
    
    Args:
        landmarks: Liste des 33 landmarks MediaPipe
        image_w, image_h: Dimensions de l'image
    
    Returns:
        String: "DROIT", "PENCHÉ EN AVANT", ou "ACCROUPI / BAS"
    """
    # Récupérer les landmarks clés
    # 11: épaule gauche, 12: épaule droite
    # 23: hanche gauche, 24: hanche droite
    # 25: genou gauche, 26: genou droite
    # 27: cheville gauche, 28: cheville droite
    
    left_shoulder = landmarks[11]
    right_shoulder = landmarks[12]
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    left_knee = landmarks[25]
    right_knee = landmarks[26]
    left_ankle = landmarks[27]
    right_ankle = landmarks[28]
    
    # Utiliser les landmarks du côté droit pour les calculs
    # (on pourrait moyenner gauche/droite pour plus de robustesse)
    
    # 1. Calculer l'angle de la hanche (épaule-hanche-genou)
    hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
    
    # 2. Calculer l'angle du genou (hanche-genou-cheville)
    knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
    
    # 3. Calculer l'inclinaison du tronc
    torso_angle = torso_lean_angle(right_shoulder, right_hip)
    
    # Classification basée sur les seuils heuristiques
    # (Ces valeurs sont ajustables selon les besoins)
    
    # Si le genou est très plié (angle < 140°), c'est une position accroupie
    if knee_angle < 140:
        return "ACCROUPI / BAS"
    
    # Si le tronc est très incliné (> 25°), penché en avant
    if torso_angle > 25:
        return "PENCHÉ EN AVANT"
    
    # Sinon, position droite
    return "DROIT"


def main():
    """
    Fonction principale - capture vidéo et analyse de posture en temps réel
    """
    # Initialiser MediaPipe Pose
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    # Configurer le modèle Pose
    pose = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1  # 0=lite, 1=full, 2=heavy
    )
    
    # Ouvrir la webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la webcam")
        return
    
    print("🏒 Détection de Posture - Hockey Trainer")
    print("=" * 50)
    print("MediaPipe Pose activé - 33 landmarks détectés")
    print("Appuyez sur 'q' pour quitter")
    print("=" * 50)
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Erreur de lecture de la frame")
            break
        
        # Convertir BGR (OpenCV) en RGB (MediaPipe)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Détecter la pose
        results = pose.process(image)
        
        # Reconvertir en BGR pour l'affichage
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Traiter les résultats si des landmarks sont détectés
        if results.pose_landmarks:
            # Dessiner les landmarks et les connexions
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )
            
            # Classifier la posture
            landmarks = results.pose_landmarks.landmark
            image_h, image_w, _ = image.shape
            posture = classify_posture(landmarks, image_w, image_h)
            
            # Afficher la classification
            # Choisir la couleur selon la posture
            if posture == "DROIT":
                color = (0, 255, 0)  # Vert
            elif posture == "PENCHÉ EN AVANT":
                color = (0, 165, 255)  # Orange
            else:  # ACCROUPI / BAS
                color = (0, 0, 255)  # Rouge
            
            # Afficher le texte de la posture
            cv2.putText(
                image,
                f"Posture: {posture}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                color,
                2,
                cv2.LINE_AA
            )
            
            # Afficher des informations supplémentaires
            # Calculer quelques angles pour affichage
            right_shoulder = landmarks[12]
            right_hip = landmarks[24]
            right_knee = landmarks[26]
            right_ankle = landmarks[28]
            
            hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
            knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
            torso_angle = torso_lean_angle(right_shoulder, right_hip)
            
            # Afficher les angles
            cv2.putText(
                image,
                f"Genou: {int(knee_angle)}°",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            
            cv2.putText(
                image,
                f"Hanche: {int(hip_angle)}°",
                (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
            
            cv2.putText(
                image,
                f"Inclinaison: {int(torso_angle)}°",
                (10, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )
        else:
            # Aucune pose détectée
            cv2.putText(
                image,
                "Aucune personne détectée",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )
        
        # Afficher la frame
        cv2.imshow('Détection de Posture - Hockey Trainer', image)
        
        # Quitter avec 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()
    pose.close()
    
    print("✅ Session terminée")


if __name__ == "__main__":
    main()
