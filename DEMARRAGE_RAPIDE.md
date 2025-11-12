# 🚀 Démarrage Rapide - Hockey Trainer

## ✅ Installation Terminée

Python 3.12 avec mediapipe est maintenant configuré dans l'environnement virtuel `venv312`.

## 🎮 Lancement des Modules

### Option 1 : Fichiers Batch (Plus Simple - Windows)

Double-cliquez sur :
- **`start_ball_tracking.bat`** - Tracking de balle seul
- **`start_action_recognition.bat`** - Reconnaissance d'actions complète

### Option 2 : Ligne de Commande

```powershell
# Tracking de balle
.\venv312\Scripts\python.exe ball_tracking.py

# Reconnaissance d'actions
.\venv312\Scripts\python.exe action_recognition.py

# Launcher (menu interactif)
.\venv312\Scripts\python.exe launcher.py
```

## ⌨️ Contrôles

### Ball Tracking
- `q` : Quitter
- `r` : Réinitialiser
- `h` : Afficher/masquer paramètres
- `s/x` : Ajuster saturation
- `d/c` : Ajuster luminosité
- `a/z` : Ajuster teinte
- `f/v` : Ajuster circularité

### Action Recognition
- `q` : Quitter
- `r` : Réinitialiser
- `h` : Afficher/masquer paramètres balle
- `s/x` : Ajuster saturation balle
- `d/c` : Ajuster luminosité balle

## 🎯 Configuration Balle Jaune

**Paramètres par défaut :**
- Teinte : 20-35
- Saturation : 80+
- Luminosité : 100+
- Circularité : 0.7+

**Si la balle n'est pas détectée :**
1. Appuyez sur `h` pour voir les paramètres
2. Baissez la saturation avec `s` (5-6 fois)
3. Vérifiez que "Contours" est faible (1-3)

**Si des reflets sont détectés :**
1. Augmentez la saturation avec `x`
2. Visez 100-120+ de saturation

## 📚 Documentation

- `GUIDE_ACTION_RECOGNITION.md` - Guide complet
- `INTEGRATION_SUMMARY.md` - Détails techniques
- `README_ACTION_RECOGNITION.md` - Vue d'ensemble

## 🔧 Environnement Python

**Environnement actif :** `venv312` (Python 3.12)

**Packages installés :**
- mediapipe
- opencv-python
- numpy
- (et leurs dépendances)

**Pour réinstaller si nécessaire :**
```powershell
.\venv312\Scripts\python.exe -m pip install mediapipe opencv-python numpy
```

## 💡 Conseils

1. **Éclairage** : Uniforme, évitez les ombres fortes
2. **Balle** : Jaune vif, propre, bien visible
3. **Arrière-plan** : Évitez les surfaces jaunes
4. **Distance** : 2-4 mètres de la caméra idéal

## 🆘 Problèmes Courants

**"ModuleNotFoundError: No module named 'mediapipe'"**
→ Utilisez les fichiers `.bat` ou le chemin complet Python :
```powershell
.\venv312\Scripts\python.exe action_recognition.py
```

**La caméra ne s'ouvre pas**
→ Vérifiez qu'aucune autre application utilise la webcam

**Détection lente**
→ Normal avec mediapipe, optimisations possibles selon PC

---

**Bon entraînement ! 🏒**
