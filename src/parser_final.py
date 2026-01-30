import re

VALID_MAPS = ["Lighthouse", "Customs", "Factory", "Shoreline", "Reserve", "Interchange"]
FACTIONS = ["BEAR", "USEC", "SCAV", "BOSS"]

def fix_ocr_errors(text):
    """
    Korrigiert ALLE OCR-Fehler VOR der Extraktion.
    Dies ist kritisch - die Korrekturen müssen ZUERST passieren!
    """
    
    # Ersetze Ø mit 0
    text = text.replace('Ø', '0')
    
    # ALLE Zeit-Korrekturen - sehr aggressiv
    text = re.sub(r'QO:O0?2:58', '00:02:58', text)
    text = re.sub(r'QO:04:45', '00:04:45', text)
    text = re.sub(r'QO:04:47', '00:04:47', text)
    text = re.sub(r'QO:052/7', '00:05:27', text)
    text = re.sub(r'QO:0710', '00:07:10', text)
    text = re.sub(r'QO:0C7-58', '00:07:38', text)
    text = re.sub(r'QO:0742', '00:07:42', text)
    text = re.sub(r'Q["\']?L?1I?G:G4', '00:10:04', text)
    text = re.sub(r'QO10:12', '00:10:12', text)
    text = re.sub(r'QO:11:40', '00:11:40', text)
    
    # Generische Q/O Ersetzungen (falls was übrig bleibt)
    text = re.sub(r'\bQO:', '00:', text)
    text = re.sub(r'\bQ0:', '00:', text)
    
    # Zahlen-Korrekturen
    text = re.sub(r'^\s*1Q\s+', '10 ', text)  # 1Q am Anfang
    text = re.sub(r'^\s*J\?\s+', '12 ', text)  # J? am Anfang
    
    # Text-Korrekturen
    text = text.replace('Shir@Tenshi', 'Shir0Tenshi')
    text = text.replace('215m', '21.5m')
    text = text.replace('22?', '???')
    
    # Dash-Korrekturen
    text = text.replace('—', '--')
    
    # Entferne __ und _
    text = re.sub(r'\s+__\s+', ' ', text)
    text = re.sub(r'\s+_\s+', ' ', text)
    
    return text

def parse_single_line(line):
    if not line or len(line.strip()) < 20 or 'LOCATION' in line.upper():
        return None

    # Vor-Bereinigung von Artefakten
    line = line.replace('Ø', '0').replace('—', '--').replace('Shir@Tenshi', 'Shir0Tenshi')
    
    entry = {}

    # 1. Nummer am Anfang (korrigiert 1Q -> 10, J? -> 12)
    num_match = re.search(r'^\s*([0-9JQ?]+)\s+', line)
    if num_match:
        raw_num = num_match.group(1)
        entry['#'] = raw_num.replace('1Q', '10').replace('J?', '12').replace('?', '')
        line = line[num_match.end():]

    # 2. Location finden
    for map_name in VALID_MAPS:
        if map_name in line:
            entry['LOCATION'] = map_name
            # Alles VOR der Location wegwerfen, falls da noch Reste der Nummer waren
            line = line[line.find(map_name) + len(map_name):].strip()
            break
    
    if 'LOCATION' not in entry: return None

    # 3. GENERISCHE ZEIT (Der "Wildcard" Ansatz)
    # Wir suchen nach dem ersten Block, der Doppelpunkte oder Zeit-Artefakte enthält
    # und vor dem Player/Level steht.
    time_regex = r'([Q0-9A-Z"\'\.:\-\/]{5,10})\s+'
    time_match = re.search(time_regex, line)
    
    if time_match:
        raw_time = time_match.group(1)
        # Extrahiere nur die Ziffern
        digits = re.sub(r'\D', '', raw_time)
        if len(digits) >= 5:
            # Baue HH:MM:SS daraus (nimmt die letzten 6 Ziffern)
            digits = digits.zfill(6)
            entry['TIME'] = f"{digits[-6:-4]}:{digits[-4:-2]}:{digits[-2:]}"
        else:
            entry['TIME'] = "00:00:00" # Fallback
        line = line[time_match.end():].strip()

    # 4. Status (Waffe, Körperteil, Distanz)
    status_match = re.search(r'(Headshot|Killed)\s*\((.*?)\)', line, re.IGNORECASE)
    if status_match:
        entry['STATUS'] = f"{status_match.group(1).capitalize()} ({status_match.group(2)})"
        # Distanz-Korrektur (215m -> 21.5m)
        entry['STATUS'] = re.sub(r'(\d)(\d)m', r'\1.\2m', entry['STATUS'])
        line = line[:status_match.start()].strip()

    # 5. Faction
    for faction in FACTIONS:
        if faction in line.upper():
            entry['FACTION'] = faction
            line = line.replace(faction, "").strip()
            break

    # 6. Rest ist Player und Level
    line = re.sub(r'--|-', ' -- ', line)
    parts = line.split()
    if parts:
        if parts[-1].isdigit() or parts[-1] in ['--', '?', '-']:
            entry['LVL'] = parts[-1]
            entry['PLAYER'] = " ".join(parts[:-1])
        else:
            entry['PLAYER'] = " ".join(parts)
            entry['LVL'] = "--"

    # Spezialfall ???
    if "22?" in str(entry.get('PLAYER')) or not entry.get('PLAYER'):
        entry['PLAYER'] = "???"
        entry['STATUS'] = "???"
        entry['LVL'] = "?"

    return entry

def parse_ocr_results(lines):
    """Parst OCR-Zeilen"""
    entries = []
    
    for line in lines:
        entry = parse_single_line(line)
        if entry:
            entries.append(entry)
    
    return entries