# backend/src/analysis/plant_count_estimator.py
from __future__ import annotations
import math

class PlantCountEstimator:
    """Estime la fourchette et le nombre idéal de plantes pour une composition."""

    # Matrice des densités (Min, Max) au m² indexée par (Type d'espace, Style)
    # Données issues des abaques de conception paysagère et des consignes du brief.
    DENSITY_PER_M2 = {
        ("jardin", "Japonais"): (1.0, 2.0),
        ("jardin", "Méditerranéen"): (3.0, 5.0),
        ("jardin", "Anglais"): (5.0, 8.0),
        ("jardin", "Au naturel"): (4.0, 6.0),
        ("jardin", "Contemporain"): (2.0, 4.0),
        ("jardin", "Exotique"): (3.0, 5.0),
        ("jardin", "A la française"): (4.0, 6.0),
        ("jardin", "Traditionnel"): (3.0, 5.0),
        # Fallbacks globaux par défaut pour les conteneurs et surfaces restreintes
        ("terrasse", "*"): (0.5, 1.0),
        ("balcon", "*"): (0.3, 0.5),
    }

    def estimate(self, surface_plantable_m2: float, type_espace: str, style: str) -> dict:
        """Calcule la fourchette basse, haute et la cible idéale de végétaux à placer.
        
        Args:
            surface_plantable_m2: Surface nette allouée à la plantation.
            type_espace: Type d'environnement ("jardin", "terrasse", "balcon").
            style: Label de style (ex: "Anglais", "Japonais").
            
        Returns:
            Dictionnaire des volumes de plantes recommandés.
        """
        type_espace = str(type_espace).lower().strip()
        
        # 1. Recherche de la densité dans la matrice avec fallback générique
        if type_espace in ("terrasse", "balcon"):
            density_range = self.DENSITY_PER_M2.get((type_espace, "*"))
        else:
            # Gestion des espaces de type Jardin
            density_range = self.DENSITY_PER_M2.get((type_espace, style))
            if not density_range:
                # Si le style est inconnu, application d'un profil "Traditionnel / Moyen" par défaut
                density_range = self.DENSITY_PER_M2.get(("jardin", "Traditionnel"))

        min_density, max_density = density_range

        # 2. Calcul des volumes bruts (Fourchettes basse et haute)
        min_plantes = surface_plantable_m2 * min_density
        max_plantes = surface_plantable_m2 * max_density

        # Calcul de la valeur idéale (Médiane géométrique de la fourchette pour équilibrer le RAG)
        densite_appliquee = (min_density + max_density) / 2
        ideal_plantes = surface_plantable_m2 * densite_appliquee

        # 3. Arrondis horticoles logiques (On ne peut pas planter une demi-plante, math.ceil sécurise l'espace)
        return {
            "min_plantes": max(1, math.floor(min_plantes)),
            "max_plantes": max(1, math.ceil(max_plantes)),
            "ideal_plantes": max(1, round(ideal_plantes)),
            "densite_appliquee": round(densite_appliquee, 2)
        }