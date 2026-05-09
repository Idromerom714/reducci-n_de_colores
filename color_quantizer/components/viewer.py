from typing import List

import streamlit as st

from core.utils import array_to_pil


def render_viewer(original_array, quantized_array, centroids_hex: List[str]):
    cols = st.columns(2)
    cols[0].image(array_to_pil(original_array), caption="Original", width="stretch")
    k = len(centroids_hex)
    cols[1].image(
        array_to_pil(quantized_array), caption=f"Cuantizada — {k} colores", width="stretch"
    )

    # Render color swatches below
    swatches_html = ""
    for hx in centroids_hex:
        swatches_html += (
            f'<div style="display:inline-block;margin:6px;text-align:center;">'
            f'<div style="width:64px;height:36px;background:{hx};border:1px solid #000"></div>'
            f'<div style="font-size:12px">{hx}</div>'
            f'</div>'
        )

    st.markdown(swatches_html, unsafe_allow_html=True)
