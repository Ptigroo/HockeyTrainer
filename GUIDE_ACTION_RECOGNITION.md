# 🏒 Guide de Reconnaissance d'Actions

## 🎯 Description

Ce module combine la **détection de balle** améliorée avec la **reconnaissance de posture** pour détecter automatiquement vos actions de hockey :
- **TIR** : Balle lancée à grande vitesse (>50 km/h)
- **PASSE** : Balle lancée à vitesse moyenne (20-50 km/h) avec bras tendu
- **DRIBBLE** : Balle maintenue proche du joueur en mouvement

## 🚀 Démarrage Rapide

### Option 1 : Via le launcher
```bash
python launcher.py
```
Puis choisissez l'option **4** pour la reconnaissance d'actions.

### Option 2 : Directement
```bash
python action_recognition.py
```

### Option 3 : Fichier batch (Windows)
Double-cliquez sur `start_action_recognition.bat`

## ⚙️ Configuration

### Détection de Balle Jaune

La détection est optimisée pour une **balle jaune vive** avec ces paramètres par défaut :
- **Teinte (Hue)** : 20-35
- **Saturation** : 80+ (couleur intense)
- **Luminosité** : 100+ (balle visible)
- **Circularité** : >0.7 (forme ronde)

### Ajustements en Temps Réel

Si la balle n'est pas bien détectée, utilisez ces touches :

| Touche | Action | Quand l'utiliser |
|--------|--------|------------------|
| `h` | Afficher/masquer paramètres | Pour voir les valeurs actuelles |
| `s` | Diminuer saturation (-10) | Si balle non détectée (trop stricte) |
| `x` | Augmenter saturation (+10) | Si reflets détectés (pas assez stricte) |
| `d` | Diminuer luminosité (-10) | Si balle dans l'ombre |
| `c` | Augmenter luminosité (+10) | Si reflets clairs détectés |
| `r` | Réinitialiser | Redémarrer l'analyse |
| `q` | Quitter | Fermer l'application |

## 🎮 Utilisation

### 1. Positionnement
- Placez-vous face à la caméra
- Gardez votre corps entier visible dans le cadre
- Assurez-vous que la balle est bien éclairée

### 2. Vérification de la Détection
- Appuyez sur `h` pour afficher les paramètres
- Vérifiez que le compteur "Contours" est faible (1-3)
- Si beaucoup de contours : augmentez la saturation avec `x`
- Si aucun contour : baissez la saturation avec `s`

### 3. Actions Détectées

#### 🔴 TIR
**Critères :**
- Vitesse de balle > 50 km/h
- Balle s'éloigne du joueur
- Haute confiance si vitesse > 80 km/h

**Conseils :**
- Frappez fort et net
- Mouvement rapide et fluide
- La balle doit partir rapidement

#### 🟠 PASSE
**Critères :**
- Vitesse entre 20-50 km/h
- Bras tendu (angle coude > 140°)
- Mouvement contrôlé

**Conseils :**
- Extension complète du bras
- Mouvement plus doux qu'un tir
- Suivi avec le bras

#### 🟢 DRIBBLE
**Critères :**
- Balle à moins de 150 pixels du joueur
- Vitesse > 5 km/h (en mouvement)
- Balle reste proche sur 5+ frames

**Conseils :**
- Gardez la balle près de vous
- Mouvement continu
- Déplacements latéraux

## 🔧 Problèmes Courants

### La balle n'est pas détectée
**Solution :**
1. Appuyez sur `h` pour voir les paramètres
2. Si "Contours: 0" → Baissez la saturation avec `s`
3. Vérifiez l'éclairage de la balle
4. Assurez-vous que la balle est jaune vif

### Des reflets sont détectés comme balles
**Solution :**
1. Augmentez la saturation avec `x` (montez à 100-120)
2. Les reflets ont une saturation faible
3. La balle jaune vive a une saturation >150

### La balle est détectée seulement de près
**Solution :**
- C'est normal ! Le système privilégie les objets proches
- Assurez-vous d'avoir un bon éclairage uniforme
- Les objets lointains ont moins de saturation

### Mon action n'est pas reconnue
**Causes possibles :**
- **TIR** : Vitesse insuffisante (< 50 km/h)
- **PASSE** : Bras pas assez tendu ou vitesse hors plage
- **DRIBBLE** : Balle trop loin ou pas assez de mouvement

**Solutions :**
- Vérifiez que la vitesse s'affiche à l'écran
- Assurez-vous que votre corps entier est visible
- Exagérez légèrement les mouvements

### La vitesse semble incorrecte
**Calibration pixels/mètre :**
- Par défaut : 100 pixels = 1 mètre
- Ajustez selon votre configuration
- Plus vous êtes proche, plus ce ratio est élevé

## 📊 Informations Affichées

### Écran Principal
```
Action: TIR
Confiance: 85%
Vitesse balle: 65.3 km/h
```

### Avec paramètres (touche `h`)
```
Balle Hue: 20-35
Balle Sat: 80+ (s/x)
Balle Val: 100+ (d/c)
Contours: 1
```

### Visualisation
- **Squelette** : Détection de votre posture (MediaPipe)
- **Cercle vert** : Balle détectée
- **Ligne jaune** : Trajectoire de la balle
- **Point bleu** : Centre du joueur

## 💡 Astuces

### Pour de Meilleurs Résultats
1. **Éclairage** : Uniforme, sans ombres fortes
2. **Arrière-plan** : Évitez les murs jaunes/oranges
3. **Balle** : Jaune vif, propre, bien visible
4. **Position** : Corps entier dans le cadre
5. **Distance** : 2-4 mètres de la caméra

### Calibration Initiale
1. Lancez le programme
2. Appuyez sur `h` pour voir les paramètres
3. Regardez "Contours" :
   - Si 0 : Baissez saturation (touches `s`)
   - Si >5 : Montez saturation (touches `x`)
   - Idéal : 1-2 contours
4. Testez quelques actions pour vérifier

### Actions Difficiles à Détecter
- **Tirs très rapides** : Peuvent sortir du champ trop vite
- **Passes courtes** : Peuvent être confondues avec dribbles
- **Mouvements latéraux** : Gardez face à la caméra

## 🔬 Paramètres Techniques

### Système de Scoring Multi-critères
La détection utilise un score composite basé sur :
- Position verticale (40%) : Privilégie le bas de l'image (sol)
- Circularité (25%) : Favorise les formes rondes
- Saturation (25%) : Préfère les couleurs vives
- Taille (10%) : Favorise les objets proches

### Filtres Anti-reflets
- Morphologie : Kernel 5x5, 1 itération
- Aire minimale : 50 pixels
- Circularité minimale : 0.7
- Rayon : 5-150 pixels

## 📞 Support

### Problème Persistant ?
1. Vérifiez `requirements.txt` installé
2. Testez d'abord `ball_tracking.py` seul
3. Consultez `QUICKSTART.md` pour l'installation

### Ressources
- `ball_tracking.py` : Test de détection balle seule
- `launcher.py` : Menu interactif complet
- `README.md` : Documentation générale

---

**Bon entraînement ! 🏒**
