import sys
import re
from pathlib import Path
import pandas as pd


FEATURE_PATTERNS = {
    "file_input_operations": [
        r"FileInputStream",
        r"FileReader",
        r"BufferedInputStream",
        r"InputStream"
    ],
    "file_output_operations": [
        r"FileOutputStream",
        r"FileWriter",
        r"BufferedOutputStream",
        r"OutputStream"
    ],
    "file_creation_operations": [
        r"new\s+File\s*\(",
        r"createNewFile\s*\("
    ],
    "file_path_operations": [
        r"getFile\s*\(",
        r"getPath\s*\(",
        r"getAbsolutePath\s*\(",
        r"getCanonicalPath\s*\("
    ],
    "repository_usage": [
        r"\brepository\b",
        r"tempDir",
        r"java\.io\.tmpdir"
    ],
    "serialization_operations": [
        r"ObjectOutputStream",
        r"writeObject\s*\("
    ],
    "deserialization_operations": [
        r"ObjectInputStream",
        r"readObject\s*\("
    ],
    "input_validation": [
        r"validate",
        r"check",
        r"sanitize",
        r"verify"
    ],
    "exception_handling": [
        r"catch\s*\(\s*IOException",
        r"throws\s+IOException",
        r"throw\s+new\s+IOException"
    ],
    "null_character_handling": [
        r"\\0",
        r"NULL",
        r"NUL"
    ]
}


def extract_features_from_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    features = {}

    for feature_name, patterns in FEATURE_PATTERNS.items():
        count = 0

        for pattern in patterns:
            count += len(re.findall(pattern, source, re.IGNORECASE))

        features[feature_name] = count

    features["source_lines"] = len(source.splitlines())

    return features


def extract_features(project_path, output_file):
    project_path = Path(project_path)

    java_files = list(project_path.rglob("*.java"))

    print(f"Java files found: {len(java_files)}")

    rows = []

    for java_file in java_files:
        features = extract_features_from_file(java_file)

        features["file"] = str(java_file.relative_to(project_path))

        rows.append(features)

    df = pd.DataFrame(rows)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Features saved to: {output_path}")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(
            "Usage: python extract_features.py "
            "<project_path> <output_csv>"
        )
        sys.exit(1)

    project_path = sys.argv[1]
    output_file = sys.argv[2]

    extract_features(project_path, output_file)