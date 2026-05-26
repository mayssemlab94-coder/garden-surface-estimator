import matplotlib.pyplot as plt
from PIL import Image

def lancer_outil():
    print("="*60)
    print("🪄 OUTIL DE MESURE AUTOMATIQUE DES PIXELS")
    print("="*60)
    print("L'image va s'ouvrir. Tu dois faire EXACTEMENT 8 clics :")
    print("  👉 MANNEQUIN 1 (Fond Gauche) : Clic 1 sur ses pieds, Clic 2 sur sa tête")
    print("  👉 MANNEQUIN 2 (Fond Droit)  : Clic 3 sur ses pieds, Clic 4 sur sa tête")
    print("  👉 MANNEQUIN 3 (Devant Gauche): Clic 5 sur ses pieds, Clic 6 sur sa tête")
    print("  👉 MANNEQUIN 4 (Devant Droit) : Clic 7 sur ses pieds, Clic 8 sur sa tête")
    
    # On ouvre l'image
    img = Image.open('mon_image.jpg')
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_title("Fais tes 8 clics ! (Pieds puis Tête pour chaque point)")
    
    # On demande à matplotlib d'enregistrer 8 clics
    points = plt.ginput(8, timeout=-1)
    plt.close()

    # Si l'utilisateur a bien fait ses 8 clics
    if len(points) == 8:
        print("\n✅ SUPER ! Voici tes mesures prêtes à être copiées :")
        print("\n" + "-"*40)
        print('            "markers": [')
        
        for i in range(4):
            x_pied, y_pied = points[i*2]
            x_tete, y_tete = points[i*2 + 1]
            hauteur = abs(y_pied - y_tete)
            
            # Formatage exact pour ton code
            print(f'                {{"x": {int(x_pied)}, "y": {int(y_pied)}, "height_px": {int(hauteur)}}},')
            
        print('            ]')
        print("-"*40 + "\n")
        print("Copie ce bloc et remplace l'ancien 'markers' dans test_surface_estimation.py !")
    else:
        print("❌ Oups, tu n'as pas fait les 8 clics. Relance le script !")

if __name__ == "__main__":
    lancer_outil()