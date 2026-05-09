import time
from typing import Dict, List

import numpy as np
from sklearn.cluster import KMeans


def quantize(image_array: np.ndarray, k: int) -> Dict:
    """Quantize an RGB image array using KMeans clustering.

    Args:
        image_array: numpy array shape (H, W, 3), dtype uint8
        k: number of clusters/colors

    Returns:
        dict with keys: 'quantized_array', 'centroids_hex', 'elapsed_seconds'
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

    centroids_hex: List[str] = [rgb_to_hex(c) for c in centroids]

    elapsed = time.time() - start

    return {
        "quantized_array": quant_array,
        "centroids_hex": centroids_hex,
        "elapsed_seconds": elapsed,
    }
