import pandas as pd

vulnerable_file = (
    r"D:\NeuroFuzzy-Security\dataset\processed\VUL4J-10-features.csv"
)

patched_file = (
    r"D:\NeuroFuzzy-Security\dataset\processed\VUL4J-10-patched-features.csv"
)

output_file = (
    r"D:\NeuroFuzzy-Security\dataset\processed\anfis_training_dataset.csv"
)


vulnerable = pd.read_csv(vulnerable_file)
patched = pd.read_csv(patched_file)

vulnerable["label"] = 1
patched["label"] = 0

dataset = pd.concat(
    [vulnerable, patched],
    ignore_index=True
)

dataset.to_csv(
    output_file,
    index=False
)

print("Training dataset created successfully.")
print(f"Total samples: {len(dataset)}")
print(f"Vulnerable samples: {sum(dataset['label'] == 1)}")
print(f"Patched samples: {sum(dataset['label'] == 0)}")
print(f"Saved to: {output_file}")