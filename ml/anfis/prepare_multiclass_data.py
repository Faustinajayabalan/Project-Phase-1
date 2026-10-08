import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
from pathlib import Path


# ---------------- FILE PATHS ----------------

base_path = Path(r"D:\NeuroFuzzy-Security")

input_file = (
    base_path
    / "dataset"
    / "processed"
    / "anfis_multiclass_dataset.csv"
)

output_file = (
    base_path
    / "dataset"
    / "processed"
    / "anfis_multiclass_ready.csv"
)

scaler_file = (
    base_path
    / "ml"
    / "models"
    / "multiclass_feature_scaler.pkl"
)

label_mapping_file = (
    base_path
    / "ml"
    / "models"
    / "vulnerability_label_mapping.pkl"
)


# ---------------- LOAD DATASET ----------------

df = pd.read_csv(input_file)


# ---------------- FEATURES ----------------

feature_columns = [
    "file_input_operations",
    "file_output_operations",
    "file_creation_operations",
    "file_path_operations",
    "repository_usage",
    "serialization_operations",
    "deserialization_operations",
    "input_validation",
    "exception_handling",
    "null_character_handling",
    "source_lines"
]

X = df[feature_columns]


# ---------------- VULNERABILITY LABELS ----------------

vulnerability_classes = sorted(df["vul_id"].unique())

label_mapping = {
    vul_id: index
    for index, vul_id in enumerate(vulnerability_classes)
}

df["label"] = df["vul_id"].map(label_mapping)

y = df["label"]


# ---------------- FEATURE SCALING ----------------

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)


# ---------------- CREATE PREPARED DATASET ----------------

prepared = pd.DataFrame(
    X_scaled,
    columns=feature_columns
)

prepared["label"] = y.values


# ---------------- SAVE DATASET ----------------

prepared.to_csv(
    output_file,
    index=False
)


# ---------------- SAVE SCALER ----------------

joblib.dump(
    scaler,
    scaler_file
)


# ---------------- SAVE LABEL MAPPING ----------------

joblib.dump(
    label_mapping,
    label_mapping_file
)


# ---------------- RESULTS ----------------

print("Multiclass ANFIS training data prepared successfully.")
print(f"Samples: {len(prepared)}")
print(f"Features: {len(feature_columns)}")
print()

print("Vulnerability label mapping:")

for vul_id, label in label_mapping.items():
    print(f"{label} -> {vul_id}")

print()

print(f"Prepared dataset: {output_file}")
print(f"Feature scaler: {scaler_file}")
print(f"Label mapping: {label_mapping_file}")