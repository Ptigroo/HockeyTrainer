# 🎨 Guide Visuel - Hockey Trainer

## 📸 À Quoi S'Attendre

### 🎯 Détection de Balle Réussie

Quand une balle est détectée, vous verrez:

```
┌─────────────────────────────────────┐
│  BALLE DÉTECTÉE                     │
│                                     │
│              ●── Vitesse: 45.3 km/h│
│             ╱ ╲  Pos: (320, 240)  │
│            │   │                   │
│             ╲_╱                    │
│           Cercle vert              │
│              │                     │
│              │ Trajectoire jaune   │
│              │                     │
│            ~~│~~                   │
│           ~~~│~~~                  │
│          ~~~~│~~~~                 │
└─────────────────────────────────────┘
```

**Éléments affichés:**
- 🟢 Cercle vert autour de la balle
- 🔴 Point rouge au centre (position exacte)
- 🟡 Ligne jaune (trajectoire)
- 📊 Texte: Vitesse en km/h
- 📍 Texte: Position (x, y)

---

### 🔍 Masque de Détection

La fenêtre "Masque de couleur" montre ce que l'algorithme "voit":

```
Masque de couleur:
┌─────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ░ = Noir (ignoré)
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  █ = Blanc (détecté)
│░░░░░░░░░░░█████░░░░░░░░░░░│
│░░░░░░░░░██████████░░░░░░░░│
│░░░░░░░░███████████░░░░░░░░│  ← Balle détectée
│░░░░░░░░░█████████░░░░░░░░░│
│░░░░░░░░░░░█████░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────┘
```

**Utilisation:** 
- Vérifier si la balle est bien détectée (zone blanche)
- Identifier les interférences (autres zones blanches)
- Ajuster les paramètres HSV si nécessaire

---

### 📊 Mode Analyse Vidéo

Interface complète avec statistiques:

```
┌────────────────────────────────────────────┐
│ Vitesse max: 67.8 km/h                    │
│ Vitesse moy: 42.5 km/h                    │
│                                            │
│               Vidéo                        │
│          avec trajectoire                  │
│           et annotations                   │
│                                            │
│ ▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░  45%            │
│        Barre de progression                │
└────────────────────────────────────────────┘
```

**Informations en temps réel:**
- Vitesse maximale atteinte
- Vitesse moyenne sur toute la vidéo
- Progression de l'analyse
- Indicateur PAUSE si en pause

---

## 🎮 Touches et Interactions

### Clavier Principal

```
┌─────────┬──────────────────────────────┐
│ Touche  │ Action                       │
├─────────┼──────────────────────────────┤
│   Q     │ Quitter l'application       │
│ ESPACE  │ Pause / Lecture (vidéo)     │
│   +     │ ↑ Calibration               │
│   -     │ ↓ Calibration               │
│   R     │ Réinitialiser tracker       │
│   →     │ Frame suivante (en pause)   │
│   C     │ Afficher calibration        │
└─────────┴──────────────────────────────┘
```

---

## 📐 Calibration Visuelle

### Méthode Simple

1. **Placez un objet de taille connue:**
   ```
   ├──────── 1 mètre ────────┤
   [======================]
   ```

2. **Comptez les pixels:**
   Utilisez un outil de capture ou observez la position

3. **Ajustez avec +/-:**
   ```
   Calibration: 80 px/m   (trop petit)
   → Appuyez sur +
   Calibration: 90 px/m
   → Appuyez sur +
   Calibration: 100 px/m  ✓ (correct!)
   ```

### Exemple Terrain de Hockey

```
Terrain de hockey sur gazon: 55m × 91m

Si la largeur (55m) = 5500 pixels
→ pixels_per_meter = 5500 / 55 = 100 px/m
```

---

## 📈 Interprétation des Résultats

### Vitesses Typiques

| Type de Tir | Vitesse | Niveau |
|-------------|---------|--------|
| Débutant | 20-40 km/h | ⭐ |
| Intermédiaire | 40-70 km/h | ⭐⭐ |
| Avancé | 70-100 km/h | ⭐⭐⭐ |
| Professionnel | 100-150 km/h | ⭐⭐⭐⭐ |
| Record | >150 km/h | ⭐⭐⭐⭐⭐ |

### Trajectoire

```
Trajectoire DIRECTE:
━━━━━━━━━━━━━━━→
Bon contrôle, puissance constante

Trajectoire IRRÉGULIÈRE:
╱╲╱╲╱╲╱╲╱╲→
Contrôle à améliorer

Trajectoire PARABOLIQUE:
     ╱‾‾‾╲
    ╱     ╲
━━━━       ━━━━→
Tir lobé (normal selon situation)
```

---

## 🎯 Scénarios d'Utilisation

### Scénario 1: Test Rapide
```
1. Lancer: python ball_tracking.py
2. Présenter balle orange devant webcam
3. Observer: détection + vitesse
4. Ajuster calibration si nécessaire
5. Quitter: touche Q
```

### Scénario 2: Analyse Match
```
1. Lancer: python ball_tracking_video.py
2. Sélectionner vidéo du match
3. Option: sauvegarder vidéo annotée
4. Observer l'analyse frame par frame
5. Consulter rapport final
```

### Scénario 3: Démonstration
```
1. Lancer: python test_detection.py
2. Créer vidéo de test (option 1)
3. Analyser automatiquement
4. Montrer aux autres
```

---

## 🎨 Personnalisation Visuelle

### Couleurs dans le Code

```python
# Balle détectée (cercle)
color_detected = (0, 255, 0)    # Vert

# Centre de la balle
color_center = (0, 0, 255)      # Rouge

# Trajectoire
color_trajectory = (0, 255, 255) # Jaune

# Texte
color_text = (255, 255, 255)    # Blanc
```

### Modifier les Couleurs

Pour changer l'apparence, modifiez les tuples BGR:
- `(B, G, R)` où B=Blue, G=Green, R=Red
- Valeurs de 0 à 255

**Exemples:**
```python
(255, 0, 0)    # Bleu
(0, 255, 0)    # Vert
(0, 0, 255)    # Rouge
(255, 255, 0)  # Cyan
(255, 0, 255)  # Magenta
(0, 255, 255)  # Jaune
(255, 255, 255) # Blanc
(0, 0, 0)      # Noir
```

---

## 🔧 Diagnostics Visuels

### Problème: Rien n'est détecté

**Vérifiez le masque:**
```
Masque tout noir? 
→ Ajustez les plages HSV

Masque avec trop de blanc?
→ Augmentez min_area

Balle visible mais non détectée?
→ Vérifiez l'éclairage
```

### Problème: Faux Positifs

```
Plusieurs zones blanches dans le masque?
→ Options:
  1. Réduire la plage HSV
  2. Augmenter min_radius
  3. Utiliser un fond uni
```

### Problème: Vitesse Erratique

```
Vitesse qui varie beaucoup?
→ Causes possibles:
  - Calibration incorrecte
  - Caméra qui bouge
  - Détection intermittente
  
Solution:
  - Stabiliser la caméra
  - Augmenter max_positions
  - Améliorer l'éclairage
```

---

## 📊 Exemple de Rapport Final

```
==================================================
📊 RAPPORT D'ANALYSE
==================================================
Vidéo: match_hockey_2025.mp4
Durée: 00:05:23
Frames analysées: 9690 / 9690 (100%)

STATISTIQUES BALLE:
  Vitesse maximale: 87.4 km/h
  Vitesse moyenne: 38.2 km/h
  Vitesse minimale: 5.1 km/h
  
DÉTECTION:
  Positions détectées: 8234
  Taux de détection: 85%
  Pertes de tracking: 42
  
CONFIGURATION:
  FPS: 30
  Résolution: 1920x1080
  Calibration: 120 pixels/mètre
  
==================================================
✅ Analyse terminée avec succès
💾 Vidéo sauvegardée: match_analyse.mp4
==================================================
```

---

## 🎓 Conseils pour de Meilleurs Résultats

### ✅ Bon Setup

```
🎥 Caméra
  │
  ├─ Stable (trépied recommandé)
  ├─ Angle: perpendiculaire au terrain
  ├─ Hauteur: 2-3 mètres
  └─ Résolution: 720p minimum
  
💡 Éclairage
  │
  ├─ Uniforme sur le terrain
  ├─ Éviter contre-jour
  └─ Pas d'ombres fortes
  
🏒 Balle
  │
  ├─ Couleur: Orange vif ou Rouge
  ├─ Propre (pas de boue)
  └─ Bonne visibilité
```

### ❌ À Éviter

```
✗ Caméra qui bouge
✗ Éclairage variable
✗ Fond de même couleur que la balle
✗ Trop d'objets orange/rouge dans le champ
✗ Balle sale ou décolorée
✗ Résolution trop basse
```

---

**🏒 Avec ce guide, vous êtes prêt à analyser vos performances !**

Pour plus de détails techniques, consultez:
- `README.md` - Documentation complète
- `QUICKSTART.md` - Démarrage rapide
- `PROJECT_OVERVIEW.md` - Vue d'ensemble technique
