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
