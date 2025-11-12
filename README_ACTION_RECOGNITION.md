# 🏒 Reconnaissance d'Actions avec Tracking de Balle Amélioré

## 🎯 Vue d'Ensemble

Ce système combine :
- **Détection de balle jaune vive** optimisée (ball_tracking.py)
- **Reconnaissance de posture** MediaPipe
- **Classification d'actions** automatique (TIR, PASSE, DRIBBLE)

## 🚀 Démarrage Rapide

```bash
# Option 1 : Via le launcher
python launcher.py
# → Choisir option 4

# Option 2 : Direct
python action_recognition.py

# Option 3 : Windows
start_action_recognition.bat
```

## ⚙️ Contrôles

| Touche | Action |
|--------|--------|
| `q` | Quitter |
| `r` | Réinitialiser |
| `h` | Afficher/masquer paramètres balle |
| `s` | Saturation -10 (si balle non détectée) |
| `x` | Saturation +10 (si reflets détectés) |
| `d` | Luminosité -10 |
| `c` | Luminosité +10 |

## 📖 Documentation

- **Guide complet** : `GUIDE_ACTION_RECOGNITION.md`
- **Résumé intégration** : `INTEGRATION_SUMMARY.md`
- **Détection balle seule** : Lancez `python ball_tracking.py`

## 🎯 Actions Détectées

- 🔴 **TIR** : Vitesse > 50 km/h, balle s'éloigne
- 🟠 **PASSE** : Vitesse 20-50 km/h, bras tendu  
- 🟢 **DRIBBLE** : Balle proche, en mouvement

## ⚡ Problèmes Courants

**Balle non détectée ?**
→ Appuyez sur `s` pour baisser la saturation

**Reflets détectés ?**
→ Appuyez sur `x` pour augmenter la saturation

**Besoin d'aide ?**
→ Consultez `GUIDE_ACTION_RECOGNITION.md`

Bon entraînement ! 🏒
