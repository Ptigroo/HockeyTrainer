# 🏒 Hockey Trainer - Aide-Mémoire

## ⚡ Démarrage Ultra-Rapide

### Double-cliquez sur: `start.bat`

---

## 🎮 Touches Essentielles

| Touche | Action |
|--------|--------|
| **Q** | Quitter |
| **ESPACE** | Pause/Lecture |
| **+** | Augmenter calibration |
| **-** | Diminuer calibration |

---

## 🚀 Commandes Rapides

```powershell
# Test webcam
python webcam_test.py

# Détection balle (direct)
python ball_tracking.py

# Analyse vidéo
python ball_tracking_video.py

# Tests
python test_detection.py
```

---

## ⚙️ Calibration Express

**Formule:** `pixels_per_meter = pixels / mètres`

**Exemple:** 1m = 150 pixels → `pixels_per_meter = 150`

Ajustez avec **+/-** pendant l'exécution

---

## 🎯 Couleurs Détectées

**Par défaut:** Orange

**Pour Rouge:** Décommentez lignes 33-36 dans `ball_tracking.py`

---

## 📊 Vitesses Typiques

| Niveau | Vitesse |
|--------|---------|
| Débutant | 20-40 km/h |
| Intermédiaire | 40-70 km/h |
| Avancé | 70-100 km/h |
| Pro | >100 km/h |

---

## 🐛 Problème? Solutions Rapides

**Balle non détectée?**
- Vérifiez la couleur
- Améliorez l'éclairage

**Vitesse incorrecte?**
- Calibrez avec +/-

**Caméra inaccessible?**
- Fermez les autres applis

---

## 📖 Documentation

- **Démarrage:** `QUICKSTART.md`
- **Visuel:** `VISUAL_GUIDE.md`
- **Complet:** `README.md`
- **Code:** `CODE_EXAMPLES.md`

---

**💡 Besoin d'aide? Ouvrez `INSTALL_COMPLETE.md`**
