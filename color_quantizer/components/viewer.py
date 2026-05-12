from typing import List

import streamlit as st

from core.utils import array_to_image_bytes, array_to_pil


def render_viewer(
    original_array,
    quantized_array,
    centroids_hex: List[str],
    centroids_names: List[str],
):
    download_format = st.radio(
        "Formato de descarga",
        ["png", "jpg"],
        horizontal=True,
        index=0,
    )

    cols = st.columns(2)
    original_bytes = array_to_image_bytes(original_array, download_format)
    cols[0].image(array_to_pil(original_array), caption="Original", width="stretch")
    cols[0].download_button(
        label="Descargar original",
        data=original_bytes,
        file_name=f"original_1.{download_format}",
        mime="image/jpeg" if download_format == "jpg" else "image/png",
        use_container_width=True,
    )

    k = len(centroids_hex)
    quantized_bytes = array_to_image_bytes(quantized_array, download_format)
    cols[1].image(
        array_to_pil(quantized_array), caption=f"Cuantizada — {k} colores", width="stretch"
    )
    cols[1].download_button(
        label="Descargar cuantizada",
        data=quantized_bytes,
        file_name=f"cuantizada_1.{download_format}",
        mime="image/jpeg" if download_format == "jpg" else "image/png",
        use_container_width=True,
    )

    # Render color swatches below
    swatches_html = ""
    for hx, name in zip(centroids_hex, centroids_names):
        swatches_html += (
            f'<div style="display:inline-block;margin:6px;text-align:center;">'
            f'<div style="width:64px;height:36px;background:{hx};border:1px solid #000"></div>'
            f'<div style="font-size:12px">{hx}</div>'
            f'<div style="font-size:12px">{name}</div>'
            f'</div>'
        )

    st.markdown(swatches_html, unsafe_allow_html=True)
