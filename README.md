# Tarkov Kill Log Parser

Dieses Python-Programm extrahiert Kill-Log-Daten aus Tarkov-Screenshots mittels OCR und konvertiert sie in strukturiertes JSON-Format.

## Voraussetzungen

### 1. Python 3.12
Stelle sicher, dass Python installiert ist:
```bash
python --version
```

### 2. Tesseract OCR
Tesseract muss auf deinem System installiert sein:

**Windows:**
- Download von: https://github.com/UB-Mannheim/tesseract/wiki
- Installiere Tesseract und füge es zum PATH hinzu
- Standard-Installationspfad: `C:\Program Files\Tesseract-OCR\`

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### 3. Python-Bibliotheken
Installiere die benötigten Python-Pakete:
```bash
pip install pytesseract pillow opencv-python
```

## Installation

1. Alle Python-Dateien in einen Ordner kopieren:
   - `run_parser.py` (Hauptprogramm)
   - `ocr_pytesseract.py` (OCR-Modul)
   - `parser_final.py` (Parser-Modul)

2. Dein Screenshot-Bild im selben Ordner platzieren oder den Pfad anpassen

## Verwendung

### Schnellstart
```bash
python run_parser.py
```

### Pfad zum Bild anpassen
Öffne `run_parser.py` und ändere die Zeile:
```python
IMAGE_PATH = "/home/claude/image.png"
```
zu deinem Bild-Pfad, z.B.:
```python
IMAGE_PATH = "C:/Users/DeinName/Desktop/tarkov_screenshot.png"
```

### Ausgabe
Das Programm erstellt eine JSON-Datei mit folgendem Format:
```json
{
  "#": "3",
  "LOCATION": "Lighthouse",
  "TIME": "00:02:38",
  "PLAYER": "Cookie",
  "LVL": "11",
  "FACTION": "BEAR",
  "STATUS": "Killed (AK-12, thorax, 22.4m)"
}
```

Die Datei wird gespeichert als: `tarkov_kills_parsed.json`

## Fehlerbehebung

### "Tesseract not found"
- Stelle sicher, dass Tesseract installiert ist
- Windows: Füge den Tesseract-Pfad zu den Umgebungsvariablen hinzu
- Oder setze den Pfad explizit in `ocr_pytesseract.py`:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### OCR-Qualität verbessern
- Verwende hochauflösende Screenshots
- Stelle sicher, dass der Text gut lesbar ist
- Vermeide Komprimierung des Screenshots

### Manuelle Nachbearbeitung
Da OCR nicht 100% perfekt ist, können einige Einträge Fehler enthalten. 
Überprüfe die JSON-Ausgabe und korrigiere bei Bedarf manuell.

## Dateien

- **run_parser.py**: Hauptprogramm - startet OCR und Parser
- **ocr_pytesseract.py**: OCR-Modul mit pytesseract
- **parser_final.py**: Parser der OCR-Text in strukturierte Daten umwandelt

## Unterstützte Felder

- `#`: Eintragsnummer
- `LOCATION`: Map-Name (Lighthouse, Customs, Factory, etc.)
- `TIME`: Zeitstempel (HH:MM:SS)
- `PLAYER`: Spielername
- `LVL`: Level (Zahl, "--" oder "?")
- `FACTION`: BEAR, USEC, SCAV, BOSS
- `STATUS`: Kill-Details (Waffe, Körperteil, Distanz)

## Hinweise

- Das Programm wurde für Tarkov Kill-Log-Screenshots optimiert
- OCR-Fehler werden automatisch korrigiert (z.B. "GO" → "00", "1Q" → "10")
- Die Genauigkeit hängt von der Qualität des Screenshots ab

## Lizenz

Frei verwendbar für persönliche Zwecke.
