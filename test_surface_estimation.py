from surface_estimator import SurfaceEstimator
from plant_count_estimator import PlantCountEstimator

# Le dictionnaire de sécurité du maître de stage
ESPACE_MINIMUM = {
    "balançoire": 15.0,
    "piscine": 40.0,
    "salon de jardin": 10.0,
    "barbecue": 5.0
}

def run_demo():
    print("=" * 65)
    print("🧪 RUNNING TEST : PARAMÈTRES, SÉCURITÉ ET TOPOGRAPHIE (PENTE)")
    print("=" * 65)

    scenarii_test = [
        {
            "nom": "TEST AVEC MON IMAGE INTERNET",
            "type_espace": "jardin", 
            "style": "Méditerranéen",
            "projet_client": "piscine",
            "image_path": "mon_image.jpg", 
            
            # 🛑 AMÉLIORATION 4 : On simule un terrain avec 15% de pente !
            "pente_terrain_pourcentage": 15.0, 
            
            "markers": [
                {"x": 102, "y": 119, "height_px": 49},   
                {"x": 31, "y": 23, "height_px": 70},   
                {"x": 223, "y": 44, "height_px": 26},  
                {"x": 277, "y": 154, "height_px": 75}   
            ]
        }
    ]

    surface_tool = SurfaceEstimator()
    count_tool = PlantCountEstimator()

    for sc in scenarii_test:
        print(f"\n📸 ÉVALUATION : {sc['nom']}")
        print("-" * 50)
        
        # Calcul de base avec repère personnalisé (Amélioration 2)
        surf_res = surface_tool.estimate(
            photo_path_or_width=sc["image_path"], 
            markers=sc["markers"],
            reference_height_cm=200.0, 
            ratio_plantable=1.0        
        )
        
        surface_2d = surf_res['surface_totale_m2']
        pente = sc["pente_terrain_pourcentage"]
        
        # 🛑 AMÉLIORATION 4 : Calcul mathématique de la surface réelle (3D)
        # Une pente augmente la surface de contact avec le sol
        surface_3d_corrigee = round(surface_2d * (1 + (pente / 100)), 1)
            
        print(f"   📐 Surface 2D (Platte) : {surface_2d} m²")
        print(f"   ⛰️  Dénivelé détecté   : {pente} %")
        print(f"   🏔️  Surface 3D (Réelle): {surface_3d_corrigee} m²")

        print("\n   🚨 CONTRÔLE DE SÉCURITÉ AMÉNAGEMENT :")
        projet = sc["projet_client"]
        if projet in ESPACE_MINIMUM:
            place_requise = ESPACE_MINIMUM[projet]
            
            # Le contrôle se fait maintenant sur la vraie surface 3D !
            if surface_3d_corrigee < place_requise:
                print(f"      ❌ IMPOSSIBLE : Le client veut un(e) '{projet}'.")
                print(f"      Il faut au moins {place_requise} m², mais le terrain réel n'en fait que {surface_3d_corrigee} m² !")
            else:
                print(f"      ✅ VALIDÉ : Il y a la place pour un(e) '{projet}' ({place_requise} m² requis).")

        styles_comparaison = [sc["style"]]
        print("\n   🔢 Volume de plantes estimé :")
        for st in styles_comparaison:
            # On donne la surface 3D à l'estimateur de plantes
            counts = count_tool.estimate(surface_3d_corrigee, sc["type_espace"], st)
            print(f"      * Style [{st}] ➡️  Idéal: {counts['ideal_plantes']} plantes")
    print("\n" + "=" * 65)

if __name__ == "__main__":
    run_demo()