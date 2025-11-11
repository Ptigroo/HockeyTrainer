import cv2

# Ouvrir la webcam (0 = caméra principale du laptop)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Impossible d'accéder à la caméra")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de capture")
        break

    # Afficher la vidéo
    cv2.imshow("Flux vidéo - Appuie sur 'q' pour quitter", frame)

    # Sortir avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
