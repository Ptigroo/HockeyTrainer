"""
Tests pour le module de reconnaissance d'actions
"""
import numpy as np
import cv2
from action_recognition import ActionRecognizer, calculate_distance


def test_calculate_distance():
    """Test du calcul de distance"""
    p1 = (0, 0)
    p2 = (3, 4)
    distance = calculate_distance(p1, p2)
    assert distance == 5.0, f"Expected 5.0, got {distance}"
    print("✅ test_calculate_distance passed")


def test_action_recognizer_init():
    """Test de l'initialisation du reconnaisseur"""
    recognizer = ActionRecognizer()
    assert recognizer.current_action == "AUCUNE"
    assert recognizer.action_confidence == 0.0
    assert len(recognizer.ball_positions) == 0
    recognizer.close()
    print("✅ test_action_recognizer_init passed")


def test_ball_detection():
    """Test de la détection de balle sur une image synthétique"""
    recognizer = ActionRecognizer()
    
    # Créer une image avec une balle orange
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Dessiner une balle orange (BGR: 0, 140, 255)
    ball_center = (320, 240)
    ball_radius = 20
    cv2.circle(frame, ball_center, ball_radius, (0, 140, 255), -1)
    
    # Détecter la balle
    result = recognizer.detect_ball(frame)
    
    assert result is not None, "La balle n'a pas été détectée"
    x, y, radius = result
    
    # Vérifier que la position détectée est proche de la position réelle
    distance_error = calculate_distance((x, y), ball_center)
    assert distance_error < 10, f"Erreur de position trop grande: {distance_error}"
    
    recognizer.close()
    print("✅ test_ball_detection passed")


def test_classify_action_no_data():
    """Test de classification sans données"""
    recognizer = ActionRecognizer()
    
    action, confidence = recognizer.classify_action(None, None, 0, 180, 0)
    
    assert action == "AUCUNE"
    assert confidence == 0.0
    
    recognizer.close()
    print("✅ test_classify_action_no_data passed")


def test_classify_action_shooting():
    """Test de classification pour un tir"""
    recognizer = ActionRecognizer()
    
    # Simuler un tir: balle rapide qui s'éloigne
    player_pos = (320, 240)
    
    # Ajouter des positions de balle qui s'éloignent
    recognizer.ball_positions.append((320, 230))  # Proche
    recognizer.ball_positions.append((320, 200))  # S'éloigne
    
    ball_pos = (320, 150)  # Encore plus loin
    ball_speed = 60  # km/h, au-dessus du seuil de tir
    arm_angle = 160  # Bras tendu
    body_lean = 15
    
    action, confidence = recognizer.classify_action(
        ball_pos, player_pos, ball_speed, arm_angle, body_lean
    )
    
    assert action == "TIR", f"Expected TIR, got {action}"
    assert confidence > 0, f"Confidence devrait être > 0, got {confidence}"
    
    recognizer.close()
    print("✅ test_classify_action_shooting passed")


def test_classify_action_dribbling():
    """Test de classification pour un dribble"""
    recognizer = ActionRecognizer()
    
    player_pos = (320, 240)
    
    # Simuler un dribble: balle proche avec mouvement
    for i in range(5):
        x = 320 + (i % 2) * 20 - 10  # Oscillation autour du joueur
        y = 240 + 50
        recognizer.ball_positions.append((x, y))
    
    ball_pos = (330, 290)
    ball_speed = 15  # Vitesse modérée
    arm_angle = 90  # Bras plié
    body_lean = 30
    
    action, confidence = recognizer.classify_action(
        ball_pos, player_pos, ball_speed, arm_angle, body_lean
    )
    
    assert action == "DRIBBLE", f"Expected DRIBBLE, got {action}"
    assert confidence > 0, f"Confidence devrait être > 0, got {confidence}"
    
    recognizer.close()
    print("✅ test_classify_action_dribbling passed")


def test_reset():
    """Test de la réinitialisation"""
    recognizer = ActionRecognizer()
    
    # Ajouter des données
    recognizer.ball_positions.append((100, 100))
    recognizer.ball_speeds.append(30.0)
    recognizer.current_action = "TIR"
    recognizer.action_confidence = 0.8
    
    # Réinitialiser
    recognizer.reset()
    
    assert len(recognizer.ball_positions) == 0
    assert len(recognizer.ball_speeds) == 0
    assert recognizer.current_action == "AUCUNE"
    assert recognizer.action_confidence == 0.0
    
    recognizer.close()
    print("✅ test_reset passed")


def run_all_tests():
    """Exécute tous les tests"""
    print("\n🧪 Lancement des tests de reconnaissance d'actions")
    print("=" * 60)
    
    try:
        test_calculate_distance()
        test_action_recognizer_init()
        test_ball_detection()
        test_classify_action_no_data()
        test_classify_action_shooting()
        test_classify_action_dribbling()
        test_reset()
        
        print("=" * 60)
        print("✅ Tous les tests sont passés avec succès!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n❌ Test échoué: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
