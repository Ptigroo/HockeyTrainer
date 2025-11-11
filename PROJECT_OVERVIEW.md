# 🏒 Hockey Trainer - Vue d'Ensemble du Projet

## 📁 Structure du Projet

```
HockeyTrainer/
│
├── 🚀 LANCEURS
│   ├── start.bat              # Lanceur Windows (double-clic)
│   └── launcher.py            # Menu interactif Python
│
├── 🎯 MODULES PRINCIPAUX
│   ├── ball_tracking.py       # Détection balle en temps réel (webcam)
│   ├── ball_tracking_video.py # Analyse de vidéos existantes
│   ├── motion_detection.py    # Détection de mouvement
│   └── webcam_test.py         # Test de la caméra
│
├── 🧪 UTILITAIRES
│   └── test_detection.py      # Tests et création vidéos démo
│
├── 📚 DOCUMENTATION
│   ├── README.md              # Documentation complète
│   ├── QUICKSTART.md          # Guide de démarrage rapide
│   └── PROJECT_OVERVIEW.md    # Ce fichier
│
└── ⚙️ CONFIGURATION
    └── requirements.txt       # Dépendances Python
```

## 🎯 Fonctionnalités Implémentées

### ✅ Détection de Balle
- **Méthode:** Détection par couleur (HSV)
- **Couleurs supportées:** Orange, Rouge (configurable)
- **Sortie:** Position (x, y), rayon, trajectoire

### ✅ Calcul de Vitesse
- **Méthode:** Suivi des positions dans le temps
- **Unité:** km/h
- **Calibration:** Ajustable en temps réel (pixels/mètre)
- **Statistiques:** Vitesse instantanée, max, moyenne

### ✅ Suivi de Trajectoire
- **Visualisation:** Ligne jaune montrant le chemin
- **Mémoire:** Configurable (par défaut 50 positions)
- **Effet:** Épaisseur dégradée

### ✅ Analyse Vidéo
- **Formats:** MP4, AVI, et autres formats OpenCV
- **Contrôles:** Pause, frame par frame, calibration
- **Export:** Vidéo annotée avec détections
- **Rapport:** Statistiques détaillées en fin d'analyse

### ✅ Interface Utilisateur
- **Affichage:** Vitesse, position, statut détection
- **Contrôles clavier:** Intuitifs et documentés
- **Masque couleur:** Fenêtre séparée pour debug
- **Barre de progression:** Pour les vidéos

## 🔧 Technologies Utilisées

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.14.0 | Langage principal |
| OpenCV | 4.12.0 | Vision par ordinateur |
| NumPy | 2.2.6 | Calculs numériques |

## 📊 Flux de Traitement

### Mode Temps Réel (Webcam)
```
Caméra → Frame → Conversion HSV → Masque couleur → 
Détection contours → Cercle minimum → Position (x,y) → 
Calcul vitesse → Affichage
```

### Mode Analyse Vidéo
```
Fichier vidéo → Frame par frame → Traitement identique → 
Accumulation statistiques → Rapport final → 
Export vidéo annotée (optionnel)
```

## 🎨 Interface Utilisateur

### Fenêtres Affichées
1. **Fenêtre principale:** 
   - Flux vidéo avec annotations
   - Cercle vert autour de la balle
   - Vitesse instantanée
   - Statistiques
   
2. **Fenêtre masque:**
   - Visualisation du filtre couleur
   - Utile pour ajuster la détection
   - Blanc = couleur détectée, Noir = ignoré

### Informations Affichées
- ✅ Statut détection (DÉTECTÉ / RECHERCHE)
- 📍 Position balle (x, y)
- 🚀 Vitesse instantanée (km/h)
- 📈 Vitesse maximale (mode vidéo)
- 📊 Vitesse moyenne (mode vidéo)
- 📏 Calibration actuelle (pixels/m)
- ⏱️ Progression (mode vidéo)

## ⚙️ Paramètres Configurables

### Dans le code:
```python
# Plages de couleur HSV
lower_orange = np.array([5, 100, 100])
upper_orange = np.array([25, 255, 255])

# Filtre de taille
min_area = 50          # pixels²
min_radius = 5         # pixels
max_radius = 100       # pixels

# Trajectoire
max_positions = 50     # nombre de points

# Calibration
pixels_per_meter = 100 # à ajuster
```

### En temps réel (touches):
- **+/-:** Calibration pixels/mètre
- **R:** Réinitialiser le tracker
- **ESPACE:** Pause/Lecture

## 📈 Métriques de Performance

### Précision de Détection
- **Dépend de:**
  - Qualité de l'éclairage
  - Contraste balle/fond
  - Calibration couleur
  
### Précision de Vitesse
- **Dépend de:**
  - Calibration pixels/mètre
  - FPS de la caméra/vidéo
  - Stabilité de la caméra

### Performance
- **FPS:** ~30 fps sur webcam standard
- **Latence:** Temps réel (<50ms)
- **Ressources:** CPU uniquement (pas de GPU requis)

## 🚀 Évolutions Futures Possibles

### Court terme:
- [ ] Détection multi-balles
- [ ] Export statistiques (CSV, JSON)
- [ ] Graphiques de vitesse
- [ ] Interface graphique (GUI)
- [ ] Sauvegarde de calibration

### Moyen terme:
- [ ] Détection joueurs (YOLO)
- [ ] Analyse de posture
- [ ] Reconnaissance d'actions (tir, passe)
- [ ] Heatmaps de positions

### Long terme:
- [ ] Analyse tactique avancée
- [ ] Suivi multi-caméras
- [ ] Machine learning pour prédictions
- [ ] Application mobile
- [ ] Cloud storage et analyse

## 🎓 Concepts Techniques

### Détection par Couleur (HSV)
**Pourquoi HSV?** Plus robuste aux variations d'éclairage que RGB.
- **H (Hue):** Teinte (0-180°)
- **S (Saturation):** Intensité couleur (0-255)
- **V (Value):** Luminosité (0-255)

### Suivi de Trajectoire
**Méthode:** Deque (file FIFO) pour stocker positions.
- Efficace en mémoire
- Accès rapide aux positions récentes
- Taille limitée automatiquement

### Calcul de Vitesse
**Formule:**
```
vitesse (km/h) = (distance_pixels / pixels_per_meter) / temps × 3.6
```

## 🎯 Cas d'Usage

### 1. Entraînement Personnel
- Mesurer la puissance de tir
- Suivre l'amélioration au fil du temps
- Identifier les techniques efficaces

### 2. Analyse d'Équipe
- Analyser les passes
- Étudier les stratégies
- Préparer les matchs

### 3. Recrutement
- Évaluer les candidats
- Comparer les performances
- Données objectives

### 4. Recherche / Académique
- Biomécanique du sport
- Analyse de mouvement
- Études statistiques

## 📞 Support & Contribution

### Rapporter un Bug
1. Décrivez le problème
2. Étapes pour reproduire
3. Logs/captures d'écran
4. Configuration (OS, Python, OpenCV)

### Suggestions
- Nouvelles fonctionnalités
- Améliorations UI/UX
- Optimisations performance

## 📄 Licence

Projet personnel - Usage libre pour apprentissage et développement.

## 🙏 Remerciements

- **OpenCV:** Framework de vision par ordinateur
- **NumPy:** Calculs numériques efficaces
- **Python:** Langage accessible et puissant

---

**Version:** 1.0
**Date:** Novembre 2025
**Auteur:** Hockey Trainer Team

🏒 *"Analyser pour mieux performer!"*
