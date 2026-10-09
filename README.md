# AI Shape Detector

AI Shape Detector is a small web application that detects geometric shapes in uploaded images using OpenCV and Flask.

## Features

- Detects Circle, Triangle, Rectangle, Square, Pentagon, Hexagon
- Heuristics for Star and Ellipse
- Shows original and processed images side-by-side
- Download processed image
- Drag & drop, preview, animated UI and dark mode

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
# open http://127.0.0.1:5000
```

## Folder Structure

AI_Shape_Detector/

- app.py
- requirements.txt
- README.md
- static/
  - css/style.css
  - js/script.js
  - uploads/
  - outputs/
  - images/logo.svg
- templates/
  - index.html
- detector/
  - detect_shapes.py

## Usage

1. Open the web app in your browser
2. Upload or drag-and-drop an image containing geometric shapes
3. Click "Detect Shapes"
4. View or download the processed annotated image

## Troubleshooting

- If images fail to upload, check file type and size (max 16MB).
- If detection fails, inspect server logs for errors.

## Notes

This project is intended as a demo and local tool. Images are stored in `static/uploads` and results in `static/outputs`.
