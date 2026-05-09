from typing import Tuple

import streamlit as st


def render_controls() -> Tuple[int, bool]:
    k_value = st.slider(
        "Número de colores (K)", min_value=2, max_value=32, value=8, step=1
    )
    button_pressed = st.button("Cuantizar")
    return k_value, button_pressed
