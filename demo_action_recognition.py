"""
Script de démonstration pour la reconnaissance d'actions
Crée une vidéo simulant différentes actions de hockey
"""
import cv2
import numpy as np
from action_recognition import ActionRecognizer, calculate_distance


def create_demo_frame_with_player_and_ball(width, height, frame_num, action_type):
    """
    Crée une frame de démo avec un joueur (rectangle) et une balle
    
    Args:
        width, height: Dimensions de la frame
        frame_num: Numéro de la frame
        action_type: Type d'action à simuler ('shooting', 'passing', 'dribbling')
    
    Returns:
        Frame BGR
    """
    # Fond blanc
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dessiner une grille
    for i in range(0, width, 50):
        cv2.line(frame, (i, 0), (i, height), (220, 220, 220), 1)
    for i in range(0, height, 50):
        cv2.line(frame, (0, i), (width, i), (220, 220, 220), 1)
    
    # Position du "joueur" (représenté par un rectangle)
    player_x = width // 4
    player_y = height // 2
    player_width = 40
    player_height = 80
    
    # Dessiner le joueur
    cv2.rectangle(frame, 
                  (player_x - player_width // 2, player_y - player_height // 2),
                  (player_x + player_width // 2, player_y + player_height // 2),
                  (0, 0, 0), -1)
    
    cv2.putText(frame, "JOUEUR", (player_x - 30, player_y - player_height // 2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Position de la balle selon l'action
    ball_radius = 15
    t = frame_num / 30.0  # Normaliser le temps
    
    if action_type == 'shooting':
        # TIR: Balle part rapidement vers la droite
        ball_x = int(player_x + 50 + t * 300)
        ball_y = int(player_y - 20 - t * 50)
        label = "SIMULATION: TIR"
        label_color = (0, 0, 255)
        
    elif action_type == 'passing':
        # PASSE: Balle part à vitesse moyenne
        ball_x = int(player_x + 50 + t * 150)
        ball_y = int(player_y)
        label = "SIMULATION: PASSE"
        label_color = (255, 165, 0)
        
    else:  # dribbling
        # DRIBBLE: Balle oscille près du joueur
        ball_x = int(player_x + 60 + 30 * np.sin(t * 5))
        ball_y = int(player_y + 50 + 20 * np.cos(t * 5))
        label = "SIMULATION: DRIBBLE"
        label_color = (0, 255, 0)
    
    # S'assurer que la balle reste dans le cadre
    ball_x = max(ball_radius, min(width - ball_radius, ball_x))
    ball_y = max(ball_radius, min(height - ball_radius, ball_y))
    
    # Dessiner la balle orange
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 140, 255), -1)
    
    # Ajouter un highlight
    highlight_pos = (ball_x - ball_radius // 3, ball_y - ball_radius // 3)
    cv2.circle(frame, highlight_pos, ball_radius // 4, (100, 200, 255), -1)
    
    # Afficher le type de simulation
    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, label_color, 2)
    
    # Afficher le numéro de frame
    cv2.putText(frame, f"Frame: {frame_num}", (10, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
    
    return frame


def demo_action_recognition():
    """
    Démonstration de la reconnaissance d'actions avec des frames simulées
    """
    print("🏒 Démonstration - Reconnaissance d'Actions")
    print("=" * 60)
    print("Cette démo montre comment le système détecte:")
    print("  - TIR: Balle rapide qui s'éloigne")
    print("  - PASSE: Balle à vitesse moyenne")
    print("  - DRIBBLE: Balle proche en mouvement")
    print("=" * 60)
    print("\nNote: Cette démo utilise des frames synthétiques.")
    print("Pour une utilisation réelle, lancez: python action_recognition.py")
    print("=" * 60)
    
    width, height = 640, 480
    fps = 30
    
    # Séquences d'actions
    sequences = [
        ('dribbling', 60, "Séquence 1/3: DRIBBLE"),
        ('passing', 45, "Séquence 2/3: PASSE"),
        ('shooting', 45, "Séquence 3/3: TIR"),
    ]
    
    print("\nAppuyez sur 'q' pour quitter, 'ESPACE' pour passer à la séquence suivante")
    print("Les séquences démarrent automatiquement...")
    
    for action_type, num_frames, sequence_name in sequences:
        print(f"\n▶ {sequence_name}")
        
        for frame_num in range(num_frames):
            # Créer la frame de démonstration
            frame = create_demo_frame_with_player_and_ball(
                width, height, frame_num, action_type
            )
            
            # Ajouter des informations supplémentaires
            info_y = 70
            cv2.putText(frame, "Demo Mode - Frames Synthetiques", 
                       (10, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)
            
            cv2.putText(frame, f"Sequence: {sequence_name}", 
                       (10, info_y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            
            # Afficher
            cv2.imshow('Demo - Reconnaissance d\'Actions', frame)
            
            # Contrôle
            key = cv2.waitKey(1000 // fps) & 0xFF
            if key == ord('q'):
                print("\n⏹ Démo arrêtée")
                cv2.destroyAllWindows()
                return
            elif key == ord(' '):
                print("  ⏭ Passage à la séquence suivante")
                break
        
        # Petite pause entre les séquences
        cv2.waitKey(500)
    
    cv2.destroyAllWindows()
    print("\n✅ Démo terminée!")
    print("\nPour utiliser le système avec une vraie webcam:")
    print("  python action_recognition.py")


if __name__ == "__main__":
    demo_action_recognition()
