# 🔧 Exemples de Code - Extensions et Personnalisations

Ce fichier contient des exemples de code pour étendre et personnaliser Hockey Trainer.

## 📝 Table des Matières

1. [Changer la Couleur de Détection](#1-changer-la-couleur-de-détection)
2. [Ajouter une Nouvelle Couleur](#2-ajouter-une-nouvelle-couleur)
3. [Sauvegarder les Statistiques](#3-sauvegarder-les-statistiques)
4. [Créer des Graphiques](#4-créer-des-graphiques)
5. [Multi-Balles](#5-détection-multi-balles)
6. [Notifications](#6-notifications-sonores)
7. [Interface Graphique](#7-interface-graphique-simple)

---

## 1. Changer la Couleur de Détection

### Détecter une Balle Bleue

```python
# Dans ball_tracking.py, méthode detect_ball():

# Remplacer:
lower_orange = np.array([5, 100, 100])
upper_orange = np.array([25, 255, 255])
mask = cv2.inRange(hsv, lower_orange, upper_orange)

# Par:
lower_blue = np.array([100, 100, 100])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
```

### Détecter une Balle Verte

```python
lower_green = np.array([40, 100, 100])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
```

### Plages de Couleurs HSV Courantes

```python
# Dictionnaire de couleurs
COLORS = {
    'rouge': ([0, 100, 100], [10, 255, 255]),
    'orange': ([5, 100, 100], [25, 255, 255]),
    'jaune': ([20, 100, 100], [40, 255, 255]),
    'vert': ([40, 100, 100], [80, 255, 255]),
    'cyan': ([80, 100, 100], [100, 255, 255]),
    'bleu': ([100, 100, 100], [130, 255, 255]),
    'violet': ([130, 100, 100], [160, 255, 255]),
    'rose': ([160, 100, 100], [180, 255, 255])
}

# Utilisation:
color_name = 'bleu'
lower, upper = COLORS[color_name]
lower = np.array(lower)
upper = np.array(upper)
mask = cv2.inRange(hsv, lower, upper)
```

---

## 2. Ajouter une Nouvelle Couleur

### Détection Multi-Couleurs

```python
def detect_ball_multicolor(self, frame):
    """
    Détecte une balle de plusieurs couleurs possibles
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Définir plusieurs plages
    ranges = [
        ([5, 100, 100], [25, 255, 255]),   # Orange
        ([0, 100, 100], [10, 255, 255]),   # Rouge
        ([160, 100, 100], [180, 255, 255]) # Rouge (wrap)
    ]
    
    # Combiner tous les masques
    combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    
    for lower, upper in ranges:
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        combined_mask = cv2.bitwise_or(combined_mask, mask)
    
    # Reste du traitement...
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.erode(combined_mask, kernel, iterations=2)
    combined_mask = cv2.dilate(combined_mask, kernel, iterations=2)
    
    # Trouver contours
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 50:
            ((x, y), radius) = cv2.minEnclosingCircle(largest)
            if radius > 5 and radius < 100:
                return (int(x), int(y), int(radius)), combined_mask
    
    return None, combined_mask
```

---

## 3. Sauvegarder les Statistiques

### Export CSV

```python
import csv
from datetime import datetime

class BallTrackerWithExport(BallTracker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_data = []  # Stocker toutes les données
    
    def update(self, frame, frame_number=None):
        """Version modifiée avec enregistrement des données"""
        position, mask = super().update(frame)
        
        if position is not None:
            x, y, radius = position
            timestamp = time.time()
            
            # Enregistrer les données
            self.all_data.append({
                'timestamp': timestamp,
                'frame': frame_number,
                'x': x,
                'y': y,
                'radius': radius,
                'speed_kmh': self.speed_kmh
            })
        
        return position, mask
    
    def export_to_csv(self, filename='ball_tracking_data.csv'):
        """Exporte les données en CSV"""
        if not self.all_data:
            print("Aucune donnée à exporter")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.all_data[0].keys())
            writer.writeheader()
            writer.writerows(self.all_data)
        
        print(f"✅ Données exportées vers {filename}")

# Utilisation:
tracker = BallTrackerWithExport()
# ... après l'analyse ...
tracker.export_to_csv('analyse_match_2025.csv')
```

### Export JSON

```python
import json

def export_to_json(tracker, filename='ball_tracking_data.json'):
    """Exporte les données en JSON"""
    data = {
        'metadata': {
            'export_date': datetime.now().isoformat(),
            'total_detections': len(tracker.all_data),
            'max_speed': tracker.max_speed,
            'avg_speed': tracker.avg_speed
        },
        'detections': tracker.all_data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Données exportées vers {filename}")
```

---

## 4. Créer des Graphiques

### Graphique de Vitesse

```python
# Installer matplotlib: pip install matplotlib

import matplotlib.pyplot as plt

def plot_speed_over_time(tracker):
    """Crée un graphique de la vitesse au fil du temps"""
    if not tracker.all_data:
        print("Aucune donnée disponible")
        return
    
    frames = [d['frame'] for d in tracker.all_data if d['frame']]
    speeds = [d['speed_kmh'] for d in tracker.all_data if d['frame']]
    
    plt.figure(figsize=(12, 6))
    plt.plot(frames, speeds, linewidth=2, color='#2196F3')
    plt.fill_between(frames, speeds, alpha=0.3, color='#2196F3')
    
    plt.title('Vitesse de la Balle au Fil du Temps', fontsize=16, fontweight='bold')
    plt.xlabel('Frame', fontsize=12)
    plt.ylabel('Vitesse (km/h)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Ligne moyenne
    avg_speed = sum(speeds) / len(speeds)
    plt.axhline(y=avg_speed, color='red', linestyle='--', 
                label=f'Moyenne: {avg_speed:.1f} km/h')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('speed_analysis.png', dpi=300)
    plt.show()
    
    print("✅ Graphique sauvegardé: speed_analysis.png")

# Utilisation:
# plot_speed_over_time(tracker)
```

### Heatmap de Positions

```python
def plot_position_heatmap(tracker, frame_width=640, frame_height=480):
    """Crée une heatmap des positions de la balle"""
    if not tracker.all_data:
        print("Aucune donnée disponible")
        return
    
    positions_x = [d['x'] for d in tracker.all_data]
    positions_y = [d['y'] for d in tracker.all_data]
    
    plt.figure(figsize=(10, 8))
    plt.hexbin(positions_x, positions_y, gridsize=20, cmap='YlOrRd')
    plt.colorbar(label='Densité')
    
    plt.title('Heatmap des Positions de la Balle', fontsize=16, fontweight='bold')
    plt.xlabel('X (pixels)', fontsize=12)
    plt.ylabel('Y (pixels)', fontsize=12)
    plt.xlim(0, frame_width)
    plt.ylim(frame_height, 0)  # Inverser Y pour correspondre à l'image
    
    plt.tight_layout()
    plt.savefig('position_heatmap.png', dpi=300)
    plt.show()
    
    print("✅ Heatmap sauvegardée: position_heatmap.png")
```

---

## 5. Détection Multi-Balles

### Tracker pour Plusieurs Balles

```python
class MultiBallTracker:
    def __init__(self, max_balls=3):
        self.max_balls = max_balls
        self.balls = []  # Liste de trackers individuels
    
    def update(self, frame):
        """Détecte et suit plusieurs balles"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Masque
        lower = np.array([5, 100, 100])
        upper = np.array([25, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Nettoyer
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Trouver tous les contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
                                       cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrer et trier par taille
        valid_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                if 5 < radius < 100:
                    valid_contours.append({
                        'position': (int(x), int(y)),
                        'radius': int(radius),
                        'area': cv2.contourArea(contour)
                    })
        
        # Trier par taille (plus grand = plus probable)
        valid_contours.sort(key=lambda c: c['area'], reverse=True)
        
        # Garder seulement les N plus grandes
        return valid_contours[:self.max_balls]
    
    def draw(self, frame, detections):
        """Dessine toutes les balles détectées"""
        colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]  # Vert, Bleu, Rouge
        
        for i, ball in enumerate(detections):
            x, y = ball['position']
            radius = ball['radius']
            color = colors[i % len(colors)]
            
            # Dessiner
            cv2.circle(frame, (x, y), radius, color, 2)
            cv2.circle(frame, (x, y), 3, color, -1)
            cv2.putText(frame, f"Balle {i+1}", (x-30, y-radius-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Utilisation:
# tracker = MultiBallTracker(max_balls=2)
# detections = tracker.update(frame)
# tracker.draw(frame, detections)
```

---

## 6. Notifications Sonores

### Alertes Audio

```python
# Windows uniquement
import winsound

def play_detection_sound():
    """Joue un son quand la balle est détectée"""
    frequency = 2500  # Hz
    duration = 100    # millisecondes
    winsound.Beep(frequency, duration)

def play_speed_alert(speed_kmh):
    """Alerte si vitesse dépasse un seuil"""
    if speed_kmh > 80:
        # Son aigu pour grande vitesse
        winsound.Beep(3000, 200)
    elif speed_kmh > 60:
        # Son moyen
        winsound.Beep(2000, 150)

# Utilisation dans le tracker:
# if position is not None:
#     play_detection_sound()
#     play_speed_alert(self.speed_kmh)
```

### Notifications Windows

```python
# Installer: pip install plyer
from plyer import notification

def notify_analysis_complete(max_speed, avg_speed):
    """Notification Windows en fin d'analyse"""
    notification.notify(
        title='🏒 Analyse Terminée',
        message=f'Vitesse max: {max_speed:.1f} km/h\nVitesse moy: {avg_speed:.1f} km/h',
        app_name='Hockey Trainer',
        timeout=10  # secondes
    )
```

---

## 7. Interface Graphique Simple

### GUI avec Tkinter

```python
import tkinter as tk
from tkinter import ttk, filedialog
import threading

class HockeyTrainerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏒 Hockey Trainer")
        self.root.geometry("500x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Titre
        title = tk.Label(self.root, text="Hockey Trainer", 
                        font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Boutons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="📹 Webcam", 
                 command=self.start_webcam, width=20, height=2).pack(pady=5)
        
        tk.Button(btn_frame, text="📂 Analyser Vidéo", 
                 command=self.analyze_video, width=20, height=2).pack(pady=5)
        
        tk.Button(btn_frame, text="🧪 Test", 
                 command=self.run_test, width=20, height=2).pack(pady=5)
        
        tk.Button(btn_frame, text="❌ Quitter", 
                 command=self.root.quit, width=20, height=2).pack(pady=5)
        
        # Zone de statut
        self.status = tk.Label(self.root, text="Prêt", 
                              font=("Arial", 10), fg="green")
        self.status.pack(pady=20)
    
    def start_webcam(self):
        self.status.config(text="Lancement de la webcam...", fg="blue")
        thread = threading.Thread(target=self._run_webcam)
        thread.start()
    
    def _run_webcam(self):
        import ball_tracking
        ball_tracking.main()
        self.status.config(text="Prêt", fg="green")
    
    def analyze_video(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner une vidéo",
            filetypes=[("Vidéos", "*.mp4 *.avi *.mov"), ("Tous", "*.*")]
        )
        
        if filename:
            self.status.config(text=f"Analyse: {filename}", fg="blue")
            thread = threading.Thread(target=self._analyze_video, args=(filename,))
            thread.start()
    
    def _analyze_video(self, filename):
        import ball_tracking_video
        ball_tracking_video.analyze_video(filename)
        self.status.config(text="Analyse terminée", fg="green")
    
    def run_test(self):
        self.status.config(text="Lancement des tests...", fg="blue")
        thread = threading.Thread(target=self._run_test)
        thread.start()
    
    def _run_test(self):
        import test_detection
        test_detection.main()
        self.status.config(text="Prêt", fg="green")
    
    def run(self):
        self.root.mainloop()

# Pour lancer:
# if __name__ == "__main__":
#     app = HockeyTrainerGUI()
#     app.run()
```

---

## 8. Configuration Persistante

### Sauvegarder les Paramètres

```python
import json
import os

CONFIG_FILE = 'hockey_trainer_config.json'

def save_config(pixels_per_meter, color_ranges, min_area):
    """Sauvegarde la configuration"""
    config = {
        'pixels_per_meter': pixels_per_meter,
        'color_ranges': color_ranges,
        'min_area': min_area
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration sauvegardée dans {CONFIG_FILE}")

def load_config():
    """Charge la configuration"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    print(f"✅ Configuration chargée depuis {CONFIG_FILE}")
    return config

# Utilisation dans BallTracker:
# def __init__(self, ...):
#     config = load_config()
#     if config:
#         self.pixels_per_meter = config['pixels_per_meter']
#     else:
#         self.pixels_per_meter = 100  # défaut
```

---

## 9. Mode Debug Avancé

### Affichage Debug Complet

```python
def draw_debug_info(frame, tracker, position):
    """Affiche toutes les informations de debug"""
    height, width = frame.shape[:2]
    
    # Panneau semi-transparent
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (300, 200), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    
    y_offset = 30
    line_height = 25
    
    # Informations
    info = [
        f"FPS: {tracker.fps:.1f}",
        f"Positions: {len(tracker.positions)}",
        f"Vitesse: {tracker.speed_kmh:.1f} km/h",
        f"Max: {tracker.max_speed:.1f} km/h",
        f"Moy: {tracker.avg_speed:.1f} km/h",
        f"Calib: {tracker.pixels_per_meter} px/m"
    ]
    
    if position:
        x, y, r = position
        info.append(f"Pos: ({x}, {y})")
        info.append(f"Rayon: {r} px")
    
    for i, text in enumerate(info):
        cv2.putText(frame, text, (20, y_offset + i * line_height),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
```

---

## 10. Enregistrement Automatique

### Auto-save des Sessions

```python
from datetime import datetime

def auto_save_session(tracker, output_dir='sessions'):
    """Sauvegarde automatique après chaque session"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV
    csv_file = os.path.join(output_dir, f'session_{timestamp}.csv')
    tracker.export_to_csv(csv_file)
    
    # Rapport texte
    report_file = os.path.join(output_dir, f'rapport_{timestamp}.txt')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"RAPPORT D'ANALYSE\n")
        f.write(f"{'='*50}\n")
        f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"Vitesse maximale: {tracker.max_speed:.1f} km/h\n")
        f.write(f"Vitesse moyenne: {tracker.avg_speed:.1f} km/h\n")
        f.write(f"Détections: {len(tracker.all_data)}\n")
        f.write(f"{'='*50}\n")
    
    print(f"✅ Session sauvegardée dans {output_dir}/")
```

---

## 📚 Ressources Supplémentaires

### Documentation OpenCV
- https://docs.opencv.org/4.x/

### Tutoriels HSV
- https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html

### Suivi d'Objets
- https://docs.opencv.org/4.x/d7/d00/tutorial_py_table_of_contents_tracking.html

---

**💡 Ces exemples sont des points de départ. Expérimentez et adaptez à vos besoins !**
