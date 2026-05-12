# Cuantizador de Color por Clustering

Aplicación web hecha con Streamlit para reducir la cantidad de colores de una imagen mediante KMeans. Permite subir una imagen JPG o PNG, elegir el número de colores y ver el resultado cuantizado junto con el historial de iteraciones en la sesión.

## Funcionalidades

- Carga de imágenes JPG y PNG.
- Cuantización de color con KMeans usando `scikit-learn`.
- Vista comparativa entre la imagen original y la cuantizada.
- Muestra de los colores centroides detectados.
- Historial de iteraciones guardado en `st.session_state` y en `color_quantizer/execution_log.json`.

## Estructura del proyecto

```text
color_quantizer/
├── app.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── quantizer.py
│   └── utils.py
└── components/
	├── __init__.py
	├── uploader.py
	├── controls.py
	├── viewer.py
	└── history.py
```

## Requisitos

- Python 3.10 o superior.
- Dependencias listadas en `color_quantizer/requirements.txt`.

## Instalación

Crear un entorno virtual e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r color_quantizer/requirements.txt
```

## Ejecución

Inicia la aplicación con:

```bash
streamlit run color_quantizer/app.py
```

Luego abre la dirección local que muestra Streamlit, normalmente:

```text
http://localhost:8501
```

## Uso

1. Sube una imagen en formato JPG o PNG.
2. Ajusta el valor de K con el control deslizante.
3. Pulsa el botón Cuantizar.
4. Revisa la comparación visual, los colores centroides y el historial de iteraciones.

## Notas técnicas

- La imagen se carga con PIL y se convierte a un arreglo `numpy` de forma `(H, W, 3)`.
- La cuantización aplasta la imagen a `(H*W, 3)`, aplica KMeans y reconstruye la imagen final.
- El historial se mantiene en memoria de sesión y también se persiste en `color_quantizer/execution_log.json`.

Prompt para la construcción del app. 

You are an expert Python developer. Build a Streamlit application for 
color quantization using KMeans clustering. Follow this EXACT project 
structure and specifications:

---

## PROJECT STRUCTURE

color_quantizer/
├── app.py
├── requirements.txt
├── core/
│   ├── __init__.py
│   ├── quantizer.py
│   └── utils.py
└── components/
    ├── __init__.py
    ├── uploader.py
    ├── controls.py
    ├── viewer.py
    └── history.py

---

## DATA FLOW

1. User uploads JPG or PNG image
2. Read with PIL → convert to numpy array shape (H, W, 3)
3. Reshape to (H*W, 3) — each row is one RGB pixel
4. Apply KMeans(n_clusters=K) from scikit-learn
5. Replace each pixel with its cluster centroid
6. Reshape back to (H, W, 3) → reconstructed quantized image
7. Display original vs quantized side by side
8. Append iteration record to st.session_state["history"]

---

## FILE SPECIFICATIONS

### core/quantizer.py
- Function: quantize(image_array: np.ndarray, k: int) -> dict
- Input: numpy array (H, W, 3), integer K
- Steps inside:
  - Reshape to (H*W, 3)
  - Fit KMeans(n_clusters=k, random_state=42, n_init='auto')
  - Replace each pixel with its centroid using labels_
  - Reshape back to (H, W, 3), cast to uint8
- Returns dict with keys:
  - "quantized_array": np.ndarray (H, W, 3)
  - "centroids_hex": list of K hex color strings (e.g. ["#FF5733", ...])
  - "elapsed_seconds": float (processing time)

### core/utils.py
- Function: load_image(uploaded_file) -> np.ndarray
  - Accepts Streamlit UploadedFile
  - Opens with PIL.Image, converts to RGB, returns numpy array
- Function: array_to_pil(array: np.ndarray) -> PIL.Image
  - Converts numpy uint8 array back to PIL Image

### components/uploader.py
- Function: render_uploader() -> np.ndarray | None
  - Uses st.file_uploader accepting ["jpg", "jpeg", "png"]
  - Calls load_image() and stores result in st.session_state["original_array"]
  - Also stores original filename in st.session_state["filename"]
  - Returns the numpy array or None if no file uploaded

### components/controls.py
- Function: render_controls() -> tuple[int, bool]
  - Renders st.slider for K: min=2, max=32, default=8, step=1, 
    label="Número de colores (K)"
  - Renders st.button labeled "Cuantizar"
  - Returns (k_value, button_pressed)

### components/viewer.py
- Function: render_viewer(original_array, quantized_array, centroids_hex)
  - Uses st.columns(2)
  - Left column: original image with caption "Original"
  - Right column: quantized image with caption f"Cuantizada — {K} colores"
  - Below both columns: render each centroid as a colored swatch using 
    st.markdown with inline HTML div blocks showing hex color and its code

### components/history.py
- Function: render_history()
  - Reads st.session_state["history"] (list of dicts)
  - If empty: st.info("No hay iteraciones registradas aún.")
  - Otherwise renders st.dataframe with columns:
    timestamp | archivo | K | tiempo (s) | colores (hex)
  - "colores (hex)" column shows comma-separated hex strings

### app.py
- Initialize st.session_state["history"] = [] if not present
- Page config: title="Cuantizador de Color", layout="wide"
- Title: st.title("🎨 Cuantizador de Color por Clustering")
- Call render_uploader() → if image loaded, call render_controls()
- On button press:
  - Call quantize() with current array and K
  - Call render_viewer() with results
  - Append to st.session_state["history"]:
    {
      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "archivo": st.session_state["filename"],
      "K": k_value,
      "tiempo (s)": round(elapsed_seconds, 3),
      "colores (hex)": centroids_hex
    }
- Below main content: st.subheader("📋 Historial de iteraciones")
- Call render_history()

### requirements.txt
streamlit
numpy
pillow
scikit-learn

---

## IMPORTANT CONSTRAINTS

- Do NOT use st.experimental_rerun or deprecated Streamlit APIs
- Use st.session_state for ALL shared state between components
- No file I/O — history lives only in session state
- All user-facing text in Spanish
- Each file must be self-contained with its own imports
- quantizer.py must import time and measure elapsed with time.time()
