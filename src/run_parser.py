#!/usr/bin/env python3
from config import Config
import json
import sys
from ocr_pytesseract import run_ocr_pytesseract
from parser_final import parse_ocr_results

IMAGE_PATH = Config.DEFAULT_IMAGE_PATH


def main():
    print("=" * 60)
    print("Tarkov Kill Log Parser")
    print("=" * 60)
    
    print("\n1. Running OCR on image...")
    try:
        lines = run_ocr_pytesseract(IMAGE_PATH)
        print(f"   ✓ Found {len(lines)} text lines\n")
    except Exception as e:
        print(f"   ✗ Error during OCR: {e}")
        return
    
    print("2. Raw OCR Output:")
    print("-" * 60)
    for i, line in enumerate(lines, 1):
        print(f"   {i:2d}: {line}")
    print("-" * 60)
    
    print("\n3. Parsing extracted data...")
    try:
        parsed = parse_ocr_results(lines)
        print(f"   ✓ Parsed {len(parsed)} entries\n")
    except Exception as e:
        print(f"   ✗ Error during parsing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("4. Parsed Results:")
    print("=" * 60)
    for entry in parsed:
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        print("-" * 60)
    
    # Speichere JSON
    output_file = "tarkov_kills_parsed.json"
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Successfully saved {len(parsed)} entries to:")
        print(f"  {output_file}")
    except Exception as e:
        print(f"\n✗ Error saving file: {e}")
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

















