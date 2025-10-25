# runtime.py - Runtime verification by executing SAS and checking log

import subprocess
import re
import sys

def verify_runtime_metadata(script_path):
    """
    Execute the SAS script and verify metadata from log.
    Assumes SAS is installed and in PATH (e.g., sas.exe on Windows).
    """
    try:
        # Execute SAS script (batch mode)
        cmd = ['sas', '-sysin', script_path, '-log', 'sas_log.log']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"Error executing SAS: {result.stderr}")
            return

        print("SAS execution successful.")
        print("Log output:")
        print(result.stdout)

        # Parse log for metadata verification (simple regex for errors/warnings)
        with open('sas_log.log', 'r') as f:
            log = f.read()

        errors = re.findall(r'ERROR.*', log, re.IGNORECASE)
        notes = re.findall(r'NOTE.*', log, re.IGNORECASE)

        if errors:
            print("Errors in log:")
            for err in errors:
                print(f"- {err.strip()}")
        else:
            print("No errors in log.")

        if notes:
            print("Notes in log:")
            for note in notes[:5]:  # Limit to first 5
                print(f"- {note.strip()}")

        # Basic metadata check: look for created datasets/libraries in log
        datasets = re.findall(r'NOTE: Table (\w+(?:\.\w+)?) created', log, re.IGNORECASE)
        if datasets:
            print("Created datasets:")
            for ds in datasets:
                print(f"- {ds}")

    except FileNotFoundError:
        print("SAS not found in PATH. Install SAS or customize the command in runtime.py.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("SAS execution timed out.")
    except Exception as e:
        print(f"Runtime verification failed: {e}")
