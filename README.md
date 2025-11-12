# 🏒 Hockey Trainer - Analyse Vidéo

Application d'analyse vidéo pour évaluer les performances des joueurs de hockey.

## 📋 Fonctionnalités

### ✅ Implémenté
- **Détection de mouvement** (`motion_detection.py`) - Détecte les zones de mouvement dans la vidéo
- **Test webcam** (`webcam_test.py`) - Vérifie que la caméra fonctionne
- **Détection de balle en temps réel** (`ball_tracking.py`) - Détecte et suit une balle de hockey orange/rouge
- **Calcul de vitesse** - Mesure la vitesse de la balle en km/h
- **Analyse vidéo** (`ball_tracking_video.py`) - Analyse des vidéos existantes avec statistiques
- **Détection de posture** (`posture_detection.py`) - Analyse la posture du joueur en temps réel avec MediaPipe

### 🎯 Fonctionnalités futures
- Détection des joueurs
- Trajectoire de la crosse
- Analyse tactique (positions, passes, etc.)

## 🚀 Installation

### Prérequis
- Python 3.7+
- OpenCV
- NumPy
- MediaPipe

### Installation des dépendances
```powershell
pip install -r requirements.txt
```

## 📖 Utilisation

### 1. Test de la webcam
```powershell
python webcam_test.py
```
- Appuyez sur `q` pour quitter

### 2. Détection de mouvement
```powershell
python motion_detection.py
```
- Détecte les mouvements dans le champ de la caméra
- Appuyez sur `q` pour quitter

### 3. Détection de balle en temps réel (webcam)
```powershell
python ball_tracking.py
```

**Touches disponibles:**
- `q` : Quitter
- `r` : Réinitialiser le tracker
- `c` : Afficher la calibration actuelle
- `+/-` : Ajuster la calibration (pixels par mètre)

**Informations affichées:**
- Position de la balle en temps réel
- Vitesse instantanée en km/h
- Trajectoire de la balle
- Masque de détection de couleur

### 4. Analyse de vidéo existante
```powershell
python ball_tracking_video.py
```

**Mode interactif:**
1. Choisir "Analyse d'une vidéo existante"
2. Entrer le chemin de la vidéo
3. Optionnellement sauvegarder la vidéo analysée

**Touches pendant la lecture:**
- `ESPACE` : Pause/Lecture
- `q` : Quitter
- `+/-` : Ajuster la calibration
- `→` (Flèche droite) : Frame suivante (en pause)

**Rapport généré:**
- Vitesse maximale atteinte
- Vitesse moyenne
- Nombre de détections
- Barre de progression

### 5. Détection de posture (IA)
```powershell
python posture_detection.py
```

**Description:**
- Utilise MediaPipe Pose pour détecter 33 landmarks du corps
- Calcule les angles (hanche, genou, inclinaison du tronc)
- Classifie la posture en temps réel

**Postures détectées:**
- `DROIT` : Posture debout normale
- `PENCHÉ EN AVANT` : Torso incliné > 25°
- `ACCROUPI / BAS` : Genou fléchi < 140°

**Touches disponibles:**
- `q` : Quitter

**Informations affichées:**
- Classification de posture avec code couleur
- Angles du genou, hanche et inclinaison
- Visualisation des 33 landmarks corporels
- Connexions squelettiques

## ⚙️ Configuration

### Calibration de la détection de couleur

Par défaut, l'application détecte les balles **orange** (typique du hockey sur gazon/salle).

Pour détecter une **balle rouge**, modifiez dans `ball_tracking.py` ou `ball_tracking_video.py`:

```python
# Décommentez ces lignes pour détecter le rouge:
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])

# Combinez les masques:
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask_red1 | mask_red2 | mask_orange
```

### Calibration de la vitesse

La vitesse est calculée en convertissant les pixels en mètres. Vous devez calibrer le ratio `pixels_per_meter` selon votre configuration.

**Méthode de calibration:**
1. Placez un objet de taille connue dans le champ de vision (ex: bâton de 1m)
2. Comptez le nombre de pixels qu'il occupe à l'écran
3. Ajustez `pixels_per_meter` avec les touches `+/-`
4. Formule: `pixels_per_meter = nombre_de_pixels / longueur_en_mètres`

**Exemple:**
- Un bâton de 1m = 150 pixels → `pixels_per_meter = 150`
- La patinoire fait 60m = 6000 pixels → `pixels_per_meter = 100`

## 🔧 Paramètres ajustables

### Dans `BallTracker` / `BallTrackerVideo`:

```python
# Nombre de positions gardées en mémoire pour la trajectoire
max_positions = 50

# Calibration distance
pixels_per_meter = 100

# Plages de couleur HSV (Orange)
lower_orange = np.array([5, 100, 100])
upper_orange = np.array([25, 255, 255])

# Filtre de taille de contour (pixels²)
min_area = 50
min_radius = 5
max_radius = 100
```

## 📊 Exemples de résultats

**Détection en temps réel:**
- Vitesse instantanée: 45.3 km/h
- Position: (320, 240)
- Trajectoire affichée en jaune

**Analyse vidéo:**
```
==================================================
📊 RAPPORT D'ANALYSE
==================================================
Vitesse maximale: 67.8 km/h
Vitesse moyenne: 42.5 km/h
Positions détectées: 245
Calibration utilisée: 100 pixels/mètre
==================================================
```

## 🐛 Résolution de problèmes

### La balle n'est pas détectée
1. Vérifiez la couleur de la balle (orange/rouge)
2. Ajustez les plages HSV dans le code
3. Vérifiez l'éclairage (évitez les ombres fortes)
4. Augmentez la taille minimum du contour si trop de faux positifs

### La vitesse semble incorrecte
1. Calibrez `pixels_per_meter` correctement
2. Vérifiez le FPS de votre caméra/vidéo
3. Assurez-vous que la caméra est stable (pas de mouvement)

### Performances faibles
1. Réduisez la résolution de la vidéo
2. Réduisez `max_positions`
3. Utilisez une vidéo avec FPS plus faible

## 📝 Structure du projet

```
HockeyTrainer/
│
├── motion_detection.py      # Détection de mouvement basique
├── webcam_test.py           # Test de la webcam
├── ball_tracking.py         # Détection de balle en temps réel
├── ball_tracking_video.py   # Analyse de vidéos
├── posture_detection.py     # Détection de posture avec IA (MediaPipe)
├── test_detection.py        # Tests et création de vidéos démo
└── README.md               # Ce fichier
```

## 🔮 Développements futurs

- [ ] Détection multi-balles
- [ ] Interface graphique (GUI)
- [ ] Export des données en CSV/JSON
- [ ] Graphiques de vitesse
- [ ] Détection des joueurs avec IA
- [x] Analyse de posture (implémenté avec MediaPipe)
- [ ] Analyse de trajectoire avancée
- [ ] Heatmaps de positions
- [ ] Reconnaissance d'actions (tir, passe, dribble)
- [ ] Postures spécifiques hockey (préparation tir, etc.)
- [ ] Fusionner détection posture avec motion_detection.py

## 📄 Licence

Projet personnel - Usage libre

## 👤 Auteur

Hockey Trainer Team

---

**Note:** Ce projet est en développement actif. Les fonctionnalités et l'API peuvent évoluer.
