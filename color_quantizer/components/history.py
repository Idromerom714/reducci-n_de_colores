from typing import List
import json

import streamlit as st
import pandas as pd


def render_history():
    history: List[dict] = st.session_state.get("history", [])
    if not history:
        st.info("No hay iteraciones registradas aún.")
        return

    st.download_button(
        label="Descargar bitácora JSON",
        data=json.dumps(history, ensure_ascii=False, indent=2),
        file_name="execution_log.json",
        mime="application/json",
    )

    df = pd.DataFrame(history)
    if "colores (hex)" in df.columns:
        df["colores (hex)"] = df["colores (hex)"].apply(
            lambda x: ", ".join(x) if isinstance(x, (list, tuple)) else x
        )

    st.dataframe(df)
