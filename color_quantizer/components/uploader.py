from typing import Optional

import streamlit as st

from core.utils import load_image


def render_uploader() -> Optional["numpy.ndarray"]:
    uploaded = st.file_uploader("Sube una imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        arr = load_image(uploaded)
        st.session_state["original_array"] = arr
        st.session_state["filename"] = uploaded.name
        st.session_state["last_result"] = None
        return arr
    return None
