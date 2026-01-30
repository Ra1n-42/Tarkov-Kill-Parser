import os
from pathlib import Path
from dotenv import load_dotenv

# Pfad zum Root-Verzeichnis (Tarkov-Kill-Parser/)
ROOT_DIR = Path(__file__).resolve().parent.parent

# .env laden
load_dotenv(ROOT_DIR / ".env")

class Config:
    TESSERACT_CMD = os.getenv("TESSERACT_PATH", "tesseract")
    # Standardmäßig ein Bild im Root-Ordner suchen, falls nichts in .env steht
    DEFAULT_IMAGE_PATH = os.getenv("IMAGE_PATH", str(ROOT_DIR / "image.png"))
    
    # Hier kannst du später weitere globale Einstellungen ergänzen
    DEBUG_MODE = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")