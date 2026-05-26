from __future__ import annotations
import logging
from pathlib import Path
from PIL import Image

logger = logging.getLogger(__name__)

class SurfaceEstimator:
    """Estime la surface plantable d'un jardin depuis les perspective markers."""

    # 🛑 NOUVEAUTÉ : On permet de choisir la taille du repère et le % plantable !
    def estimate(self, photo_path_or_width: str | Path | int, photo_height_px: int | None = None, markers: list[dict] = None, reference_height_cm: float = 170.0, ratio_plantable: float = 0.80) -> dict:
        
        if isinstance(photo_path_or_width, (str, Path)):
            with Image.open(photo_path_or_width) as img:
                photo_width_px, photo_height_px = img.size
        else:
            photo_width_px = photo_path_or_width

        sorted_markers = sorted(markers, key=lambda m: m['y'])
        top_markers = sorted_markers[:2]      
        bottom_markers = sorted_markers[2:]   

        # 🛑 NOUVEAUTÉ : On utilise 'reference_height_cm' au lieu de 170 en dur
        scale_top_px_cm = (top_markers[0]['height_px'] + top_markers[1]['height_px']) / 2 / reference_height_cm
        scale_top_px_m = scale_top_px_cm * 100

        scale_bottom_px_cm = (bottom_markers[0]['height_px'] + bottom_markers[1]['height_px']) / 2 / reference_height_cm
        scale_bottom_px_m = scale_bottom_px_cm * 100

        width_top_m = photo_width_px / scale_top_px_m
        width_bottom_m = photo_width_px / scale_bottom_px_m

        avg_y_top = (top_markers[0]['y'] + top_markers[1]['y']) / 2
        avg_y_bottom = (bottom_markers[0]['y'] + bottom_markers[1]['y']) / 2
        depth_px = avg_y_bottom - avg_y_top

        avg_scale_px_m = (scale_top_px_m + scale_bottom_px_m) / 2
        depth_m = depth_px / avg_scale_px_m

        surface_totale_m2 = ((width_top_m + width_bottom_m) / 2) * depth_m

        # 🛑 NOUVEAUTÉ : On utilise le ratio choisi par l'utilisateur
        surface_plantable_m2 = surface_totale_m2 * ratio_plantable

        return {
            "surface_totale_m2": round(surface_totale_m2, 1),
            "surface_plantable_m2": round(surface_plantable_m2, 1),
            "scale_top": round(scale_top_px_cm, 3),
            "scale_bottom": round(scale_bottom_px_cm, 3)
        }