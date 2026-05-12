from datetime import datetime
import json
from pathlib import Path

import streamlit as st

from components.uploader import render_uploader
from components.controls import render_controls
from components.viewer import render_viewer
from components.history import render_history
from core.quantizer import quantize


LOG_FILE = Path(__file__).with_name("execution_log.json")


def load_history() -> list[dict]:
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return data


def save_history(history: list[dict]) -> None:
    with LOG_FILE.open("w", encoding="utf-8") as file_handle:
        json.dump(history, file_handle, ensure_ascii=False, indent=2)


def main():
    if "history" not in st.session_state:
        st.session_state["history"] = load_history()
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None

    st.set_page_config(page_title="Cuantizador de Color", layout="wide")
    st.title("🎨 Cuantizador de Color por Clustering")

    original = render_uploader()

    if original is not None:
        k_value, pressed = render_controls()

        if pressed:
            result = quantize(original, k_value)
            st.session_state["last_result"] = result
            st.session_state["history"].append(
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "archivo": st.session_state.get("filename", "-"),
                    "K": k_value,
                    "tiempo (s)": round(result["elapsed_seconds"], 3),
                    "colores (hex)": result["centroids_hex"],
                    "nombres de color": result["centroids_names"],
                }
            )
            save_history(st.session_state["history"])

        last_result = st.session_state.get("last_result")
        if last_result is not None:
            quantized_array = last_result["quantized_array"]
            centroids_hex = last_result["centroids_hex"]
            centroids_names = last_result["centroids_names"]
            elapsed = last_result["elapsed_seconds"]

            render_viewer(original, quantized_array, centroids_hex, centroids_names)

    st.subheader("📋 Historial de iteraciones")
    render_history()


if __name__ == "__main__":
    main()
