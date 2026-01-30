from config import Config
import pytesseract
from PIL import Image
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD

def run_ocr_pytesseract(img_path):
    """
    Optimierte OCR speziell für Tarkov Screenshots.
    Verwendet nur Konfigurationen die ganze Zeilen liefern.
    """
    img = cv2.imread(img_path)
    
    if img is None:
        raise ValueError(f"Konnte Bild nicht laden: {img_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Moderate Vergrößerung
    gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # Sanfte Rauschunterdrückung
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # Prüfe Helligkeit
    avg_brightness = np.mean(gray)
    
    if avg_brightness < 128:
        # Dunkler Hintergrund -> invertieren
        gray = cv2.bitwise_not(gray)
    
    # Thresholding
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Speichere Debug-Bild
    cv2.imwrite('debug_preprocessed.png', binary)
    print(f"   Debug-Bild gespeichert (Helligkeit: {avg_brightness:.1f})")
    
    # NUR Konfigurationen die ganze Zeilen liefern (PSM 6)
    configs = [
        ('Standard PSM 6', r'--oem 1 --psm 6'),
        ('Mit Whitelist', r'--oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.:,()@-?#/Ø '),
        ('PSM 4 (Single Column)', r'--oem 1 --psm 4'),
    ]
    
    best_lines = []
    best_score = 0
    best_config_name = ""
    
    print(f"   Probiere {len(configs)} OCR-Konfigurationen...")
    
    for config_name, config in configs:
        try:
            text = pytesseract.image_to_string(binary, config=config, lang='eng')
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            # Ersetze Ø mit 0
            lines = [line.replace('Ø', '0') for line in lines]
            
            # Filtere sehr kurze Zeilen (< 5 Zeichen)
            lines = [line for line in lines if len(line) > 5]
            
            # Score: Bevorzuge Zeilen mit mehr als 20 Zeichen (ganze Zeilen)
            # und ca. 10-12 Zeilen (für 10 Einträge + Header)
            long_lines = [line for line in lines if len(line) > 20]
            score = len(long_lines)
            
            # Bonus wenn Anzahl nahe bei 10-12 liegt
            if 10 <= len(long_lines) <= 12:
                score += 10
            
            print(f"   {config_name}: {len(lines)} Zeilen ({len(long_lines)} lange Zeilen, Score: {score})")
            
            if score > best_score:
                best_lines = lines
                best_score = score
                best_config_name = config_name
                
        except Exception as e:
            print(f"   {config_name} fehlgeschlagen: {e}")
            continue
    
    # Wenn immer noch zu wenig gute Zeilen, versuche mit Original-Graustufen
    if best_score < 8:
        print(f"   Versuche mit Original-Graustufen...")
        try:
            text = pytesseract.image_to_string(gray, config=r'--oem 1 --psm 6', lang='eng')
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            lines = [line.replace('Ø', '0') for line in lines]
            lines = [line for line in lines if len(line) > 5]
            
            long_lines = [line for line in lines if len(line) > 20]
            score = len(long_lines)
            
            if 10 <= len(long_lines) <= 12:
                score += 10
            
            print(f"   Original-Graustufen: {len(lines)} Zeilen ({len(long_lines)} lange Zeilen, Score: {score})")
            
            if score > best_score:
                best_lines = lines
                best_score = score
                best_config_name = "Original-Graustufen"
        except Exception as e:
            print(f"   Original-Graustufen fehlgeschlagen: {e}")
    
    print(f"   ✓ Beste Config: {best_config_name} mit {len(best_lines)} Zeilen")
    
    return best_lines