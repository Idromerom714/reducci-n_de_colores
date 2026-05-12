import time
from typing import Dict, List

import numpy as np
from sklearn.cluster import KMeans


COLOR_NAME_PALETTE = [
    ("Negro", (0, 0, 0)),
    ("Blanco", (255, 255, 255)),
    ("Gris", (128, 128, 128)),
    ("Plateado", (192, 192, 192)),
    ("Rojo", (255, 0, 0)),
    ("Granate", (128, 0, 0)),
    ("Naranja", (255, 165, 0)),
    ("Amarillo", (255, 255, 0)),
    ("Verde", (0, 128, 0)),
    ("Lima", (0, 255, 0)),
    ("Oliva", (128, 128, 0)),
    ("Cian", (0, 255, 255)),
    ("Verde azulado", (0, 128, 128)),
    ("Azul", (0, 0, 255)),
    ("Azul marino", (0, 0, 128)),
    ("Morado", (128, 0, 128)),
    ("Fucsia", (255, 0, 255)),
]


def quantize(image_array: np.ndarray, k: int) -> Dict:
    """Quantize an RGB image array using KMeans clustering.

    Args:
        image_array: numpy array shape (H, W, 3), dtype uint8
        k: number of clusters/colors

    Returns:
        dict with keys: 'quantized_array', 'centroids_hex', 'centroids_names', 'elapsed_seconds'
    """
    start = time.time()

    h, w, c = image_array.shape
    flat = image_array.reshape(-1, 3).astype(float)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(flat)

    centroids = np.rint(kmeans.cluster_centers_).astype(int)
    centroids = np.clip(centroids, 0, 255)

    quant_flat = centroids[labels]
    quant_array = quant_flat.reshape(h, w, 3).astype(np.uint8)

    def rgb_to_hex(rgb):
        return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def rgb_to_name(rgb):
        distances = [
            (
                (int(rgb[0]) - base_rgb[0]) ** 2
                + (int(rgb[1]) - base_rgb[1]) ** 2
                + (int(rgb[2]) - base_rgb[2]) ** 2,
                name,
            )
            for name, base_rgb in COLOR_NAME_PALETTE
        ]
        return min(distances, key=lambda item: item[0])[1]

    centroids_hex: List[str] = [rgb_to_hex(c) for c in centroids]
    centroids_names: List[str] = [rgb_to_name(c) for c in centroids]

    elapsed = time.time() - start

    return {
        "quantized_array": quant_array,
        "centroids_hex": centroids_hex,
        "centroids_names": centroids_names,
        "elapsed_seconds": elapsed,
    }
