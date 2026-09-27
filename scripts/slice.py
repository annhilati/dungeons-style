import argparse
import os
import sys
from pathlib import Path
from PIL import Image

def slice_image(file_path, x_size, y_size):
    try:
        img = Image.open(file_path)
    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    width, height = img.size

    slice_width = width // x_size
    slice_height = height // y_size

    if width % x_size != 0 or height % y_size != 0:
        print(f"WARNUNG: Die Bildabmessungen ({width}x{height} Pixel) lassen sich nicht restlos in das {x_size}x{y_size}-Raster aufteilen.")
        print(f"Es werden am rechten und unteren Rand Pixel abgeschnitten. Jedes Einzelbild wird {slice_width}x{slice_height} Pixel groß sein.")

    # Erstelle Ausgabeordner
    base_path = Path(file_path)
    output_dir = base_path.parent / f"{base_path.stem}_slices"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Zerteile Bild in {x_size * y_size} Einzelbilder ({x_size} Spalten, {y_size} Zeilen)...")

    for y in range(y_size):
        for x in range(x_size):
            left = x * slice_width
            upper = y * slice_height
            right = left + slice_width
            lower = upper + slice_height

            # Bereich ausschneiden
            cropped = img.crop((left, upper, right, lower))

            # Speichern unter x_y.png
            output_filename = f"{x}_{y}.png"
            output_filepath = output_dir / output_filename
            cropped.save(output_filepath, "PNG")

    print(f"Erfolgreich abgeschlossen! Die {x_size * y_size} Bilder wurden im Ordner '{output_dir}' gespeichert.")

def main():
    parser = argparse.ArgumentParser(
        description="Zerteilt ein Bild mittels PIL in ein Raster aus Einzelbildern."
    )
    parser.add_argument("file", help="Pfad zur Eingabebilddatei")
    parser.add_argument("x_size", type=int, help="Anzahl der Einzelbilder entlang der X-Achse (Spalten)")
    parser.add_argument("y_size", type=int, help="Anzahl der Einzelbilder entlang der Y-Achse (Zeilen)")

    args = parser.parse_args()

    if args.x_size <= 0 or args.y_size <= 0:
        print("Fehler: x_size und y_size müssen mindestens 1 betragen.", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(args.file):
        print(f"Fehler: Die Datei '{args.file}' konnte nicht gefunden werden.", file=sys.stderr)
        sys.exit(1)

    slice_image(args.file, args.x_size, args.y_size)

if __name__ == "__main__":
    main()