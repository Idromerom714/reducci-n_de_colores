from typing import Optional

import streamlit as st

from core.utils import load_image


def render_uploader() -> Optional["numpy.ndarray"]:
    uploaded = st.file_uploader("Sube una imagen (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded is not None:
        arr = load_image(uploaded)
        st.session_state["original_array"] = arr
        prev_name = st.session_state.get("filename")
        # Only clear last_result when a different file is uploaded
        if prev_name is None or prev_name != uploaded.name:
            st.session_state["last_result"] = None
        st.session_state["filename"] = uploaded.name
        return arr
    return None
