# Third
# SAS Metadata Extractor

A tool to extract metadata (e.g., libraries, datasets, macros) from SAS scripts using hybrid static parsing and ML-based line classification. Optional runtime verification via SAS execution.

## Setup

Install dependencies: `pip install scikit-learn pandas`

Ensure SAS is installed for runtime verification (optional).

## Usage

Basic extraction: `python main.py sample.sas`

Outputs static + ML-extracted metadata.

Train ML model first: `python main.py sample.sas --train`

Uses `training_data.csv` for training.

Runtime verification: `python main.py sample.sas --runtime`

Executes the script and checks log against metadata.

## Files

- `main.py`: Entry point.
- `parser.py`: Regex + AST for static analysis.
- `runtime.py`: Executes SAS and verifies.
- `ml_extract.py`: Classifies lines as metadata/code.
- `sample.sas`: Test script.
- `training_data.csv`: ML training data (expand as needed).
- `README.md`: This file.

## Extending

Add more regex in `parser.py` for SAS elements.

Improve ML with more features/labels in `ml_extract.py`.

Customize SAS path in `runtime.py`.
