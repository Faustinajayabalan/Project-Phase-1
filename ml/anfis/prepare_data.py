import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

input_file = (
    r"D:\NeuroFuzzy-Security\dataset\processed"
    r"\anfis_training_dataset.csv"
)

output_file = (
    r"D:\NeuroFuzzy-Security\dataset\processed"
    r"\anfis_ready_dataset.csv"
)

scaler_file = (
    r"D:\NeuroFuzzy-Security\ml\models"
    r"\feature_scaler.pkl"
)

df = pd.read_csv(input_file)

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
y = df["label"]

scaler = MinMaxScaler()

X_scaled = scaler.fit_transform(X)

prepared = pd.DataFrame(
    X_scaled,
    columns=feature_columns
)

prepared["label"] = y.values

prepared.to_csv(
    output_file,
    index=False
)

joblib.dump(
    scaler,
    scaler_file
)

print("ANFIS training data prepared successfully.")
print(f"Samples: {len(prepared)}")
print(f"Features: {len(feature_columns)}")
print(f"Saved dataset: {output_file}")
print(f"Saved scaler: {scaler_file}")