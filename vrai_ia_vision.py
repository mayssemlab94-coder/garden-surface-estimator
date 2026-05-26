import cv2
import numpy as np
import time

def analyser_image_reelle():
    print("="*65)
    print("🤖 MODULE IA : VISION PAR ORDINATEUR EN ARRIÈRE-PLAN")
    print("="*65)
    
    print("   ⏳ [IA] Chargement de l'image 'mon_image.jpg'...")
    time.sleep(0.5) # Petite pause pour l'effet de calcul
    img = cv2.imread('mon_image.jpg')
    
    if img is None:
        print("   ❌ Erreur : Image introuvable.")
        return

    print("   ⏳ [IA] Scan des pixels et conversion colorimétrique (HSV)...")
    time.sleep(0.5)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    print("   ⏳ [IA] Détection algorithmique de la chlorophylle (Vert)...")
    time.sleep(0.5)
    # Définition des nuances de vert
    vert_clair = np.array([35, 40, 40])
    vert_fonce = np.array([85, 255, 255])
    masque_ia = cv2.inRange(img_hsv, vert_clair, vert_fonce)

    print("   ⏳ [IA] Compilation des données mathématiques...")
    time.sleep(0.5)
    pixels_totaux = masque_ia.shape[0] * masque_ia.shape[1]
    pixels_verts = cv2.countNonZero(masque_ia)
    pourcentage_vert = (pixels_verts / pixels_totaux) * 100

    print("\n" + "-" * 50)
    print("📊 RAPPORT FINAL DE L'IA :")
    print("-" * 50)
    print(f"   * Résolution analysée : {img.shape[1]}x{img.shape[0]} pixels")
    print(f"   * Total des pixels du terrain : {pixels_totaux:,}".replace(",", " "))
    print(f"   * Pixels de végétation isolés : {pixels_verts:,}".replace(",", " "))
    print(f"\n   🌱 TAUX DE VÉGÉTATION DÉTECTÉ : {pourcentage_vert:.2f}%")
    print("="*65)

if __name__ == "__main__":
    analyser_image_reelle()