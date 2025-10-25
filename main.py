# main.py - Entry point for SAS Metadata Extractor

import argparse
import sys
from parser import extract_static_metadata
from ml_extract import classify_lines_ml, train_ml_model, load_ml_model
from runtime import verify_runtime_metadata
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='SAS Metadata Extractor')
    parser.add_argument('script', help='Path to SAS script')
    parser.add_argument('--train', action='store_true', help='Train ML model')
    parser.add_argument('--runtime', action='store_true', help='Runtime verification')
    args = parser.parse_args()

    if not args.script.endswith('.sas'):
        print("Error: Input file must be a .sas file.")
        sys.exit(1)

    if args.train:
        train_ml_model('training_data.csv')
        print("ML model trained and saved.")
        return

    # Read SAS script
    with open(args.script, 'r') as f:
        lines = f.readlines()

    if args.runtime:
        verify_runtime_metadata(args.script)
        return

    # Basic extraction: static + ML
    static_metadata = extract_static_metadata(lines)
    model = load_ml_model()
    ml_classifications = classify_lines_ml(lines, model)
    ml_metadata = [line.strip() for line, cls in ml_classifications if cls == 'metadata' and line.strip()]

    # Combine (avoid duplicates)
    all_metadata = list(set(static_metadata + ml_metadata))

    print("Extracted Metadata:")
    for meta in all_metadata:
        print(f"- {meta}")

    # Save to CSV for convenience
    df = pd.DataFrame({'metadata': all_metadata})
    df.to_csv('extracted_metadata.csv', index=False)
    print("\nMetadata saved to extracted_metadata.csv")

if __name__ == '__main__':
    main()
