# parser.py - Static analysis using regex for SAS metadata

import re

def extract_static_metadata(lines):
    """
    Extract metadata like libraries, datasets, macros using regex.
    Returns list of metadata strings.
    """
    metadata = []

    # Library: libname <name> <path>;
    lib_pattern = r'libname\s+(\w+)\s+[\'"].*?[\'"]\s*;'
    for line in lines:
        lib_match = re.search(lib_pattern, line, re.IGNORECASE)
        if lib_match:
            metadata.append(f"Library: {lib_match.group(1)}")

    # Dataset: data <lib.>?<dataset>;
    data_pattern = r'data\s+(\w+(?:\.\w+)?)\s*;'
    for line in lines:
        data_match = re.search(data_pattern, line, re.IGNORECASE)
        if data_match:
            metadata.append(f"Dataset: {data_match.group(1)}")

    # Macro: %macro <name>;
    macro_pattern = r'%macro\s+(\w+)\s*;'
    for line in lines:
        macro_match = re.search(macro_pattern, line, re.IGNORECASE)
        if macro_match:
            metadata.append(f"Macro: {macro_match.group(1)}")

    # Macro end: %mend <name>?; (optional name)
    mend_pattern = r'%mend\s+(\w+)?\s*;'
    for line in lines:
        mend_match = re.search(mend_pattern, line, re.IGNORECASE)
        if mend_match and mend_match.group(1):
            metadata.append(f"Macro end: {mend_match.group(1)}")

    # Run statements
    run_pattern = r'run\s*;'
    for line in lines:
        if re.search(run_pattern, line, re.IGNORECASE):
            metadata.append("Run statement")

    return metadata
