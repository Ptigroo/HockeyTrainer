# 🚀 Guide de Démarrage Rapide - Hockey Trainer

## Installation (Première utilisation)

### Étape 1: Installer les dépendances
Ouvrez PowerShell dans ce dossier et exécutez:
```powershell
pip install -r requirements.txt
```

OU utilisez directement le lanceur qui installera automatiquement les dépendances:
```powershell
python launcher.py
```

OU double-cliquez sur `start.bat`

## 🎯 Utilisation Rapide

### Option 1: Lanceur interactif (Recommandé)
Double-cliquez sur `start.bat` ou exécutez:
```powershell
python launcher.py
```

### Option 2: Lancer directement un module

#### Test de la webcam
```powershell
python webcam_test.py
```

#### Détection de balle en temps réel
```powershell
python ball_tracking.py
```

#### Analyse d'une vidéo
```powershell
python ball_tracking_video.py
```

#### Tests et démonstration
```powershell
python test_detection.py
```

## 🎮 Touches Principales

| Touche | Action |
|--------|--------|
| `Q` | Quitter |
| `ESPACE` | Pause/Lecture (vidéo) |
| `+` | Augmenter calibration |
| `-` | Diminuer calibration |
| `R` | Réinitialiser tracker |
| `→` | Frame suivante (en pause) |

## ⚙️ Configuration Rapide

### Pour une balle ORANGE (défaut)
Aucune configuration nécessaire ✅

### Pour une balle ROUGE
Modifiez dans `ball_tracking.py` lignes 28-32:
```python
# Décommentez ces lignes:
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
# ...
```

### Calibration de la vitesse
1. Lancez le module de détection
2. Utilisez `+` ou `-` pour ajuster `pixels_per_meter`
3. Formule: **pixels_per_meter = pixels / mètres**

**Exemple:** 
- Un objet de 1m fait 150 pixels → `pixels_per_meter = 150`

## 📊 Que fait chaque module?

| Module | Description | Utilité |
|--------|-------------|---------|
| `webcam_test.py` | Affiche le flux de la webcam | Tester si la caméra fonctionne |
| `motion_detection.py` | Détecte les mouvements | Analyser l'activité globale |
| `ball_tracking.py` | Détecte et suit la balle (webcam) | Entraînement en temps réel |
| `ball_tracking_video.py` | Analyse une vidéo | Analyser un match/entraînement |
| `test_detection.py` | Crée des vidéos de test | Tester sans matériel |
| `launcher.py` | Menu interactif | Accès facile à tous les modules |

## 🎬 Premier Test

1. **Créez une vidéo de test:**
   ```powershell
   python test_detection.py
   ```
   Choisissez option 1

2. **Analysez la vidéo:**
   Choisissez ensuite option 3 pour analyser

3. **Testez avec votre webcam:**
   ```powershell
   python ball_tracking.py
   ```
   Présentez une balle orange devant la caméra

## 🐛 Problèmes Courants

### "Module cv2 not found"
→ Installez OpenCV: `pip install opencv-python`

### La balle n'est pas détectée
→ Vérifiez:
- La couleur de la balle (orange/rouge)
- L'éclairage
- Ajustez les plages HSV dans le code

### Vitesse incorrecte
→ Calibrez `pixels_per_meter` avec les touches +/-

### Caméra non accessible
→ Fermez les autres applications utilisant la caméra

## 📖 Documentation Complète

Consultez `README.md` pour la documentation complète.

## 💡 Conseils

- ✅ Utilisez un bon éclairage
- ✅ Fond uni pour meilleure détection
- ✅ Calibrez avant chaque session
- ✅ Filmez en 30 FPS minimum
- ✅ Stabilisez la caméra

## 🎯 Prochaines Étapes

Une fois familiarisé avec la détection de balle:
1. Filmez vos entraînements
2. Analysez les vidéos
3. Suivez vos progrès (vitesse max, moyenne)
4. Identifiez les points à améliorer

---

**Besoin d'aide?** Consultez le README.md ou les commentaires dans le code.

🏒 Bon entraînement!
