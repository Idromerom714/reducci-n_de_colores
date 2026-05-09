from typing import Any
import numpy as np
from PIL import Image


def load_image(uploaded_file: Any) -> np.ndarray:
    """Load a Streamlit UploadedFile into a RGB numpy array.

    Args:
        uploaded_file: file-like object from Streamlit `st.file_uploader`.

    Returns:
        numpy array with shape (H, W, 3) and dtype uint8
    """
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)


def array_to_pil(array: np.ndarray) -> Image.Image:
    """Convert a uint8 numpy array (H, W, 3) back to a PIL Image."""
    return Image.fromarray(array)
