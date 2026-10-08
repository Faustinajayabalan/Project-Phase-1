import pandas as pd
import torch
import torch.nn as nn
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


# ============================================================
# FILE PATHS
# ============================================================

BASE_PATH = Path(r"D:\NeuroFuzzy-Security")

DATASET_PATH = (
    BASE_PATH
    / "dataset"
    / "processed"
    / "anfis_multiclass_ready.csv"
)

MODEL_PATH = (
    BASE_PATH
    / "ml"
    / "models"
    / "multiclass_anfis_model.pth"
)


# ============================================================
# SETTINGS
# ============================================================

NUM_FEATURES = 11
NUM_CLASSES = 5
NUM_RULES = 8

EPOCHS = 500
LEARNING_RATE = 0.01

RANDOM_STATE = 42


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATASET_PATH)

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

X = df[feature_columns].values
y = df["label"].values


# ============================================================
# CONVERT TO PYTORCH TENSORS
# ============================================================

X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.long)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print("Dataset loaded successfully.")
print(f"Total samples: {len(X)}")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")
print(f"Features: {NUM_FEATURES}")
print(f"Classes: {NUM_CLASSES}")
print()


# ============================================================
# ANFIS MODEL
# ============================================================

class MulticlassANFIS(nn.Module):

    def __init__(
        self,
        num_features,
        num_rules,
        num_classes
    ):
        super().__init__()

        self.num_features = num_features
        self.num_rules = num_rules
        self.num_classes = num_classes

        # Gaussian membership function parameters
        self.centers = nn.Parameter(
            torch.rand(num_rules, num_features)
        )

        self.sigmas = nn.Parameter(
            torch.ones(num_rules, num_features) * 0.5
        )

        # Consequent parameters
        self.consequent_weights = nn.Parameter(
            torch.randn(
                num_rules,
                num_features,
                num_classes
            ) * 0.01
        )

        self.consequent_bias = nn.Parameter(
            torch.zeros(
                num_rules,
                num_classes
            )
        )


    def forward(self, x):

        # ----------------------------------------------------
        # Layer 1: Gaussian Membership Functions
        # ----------------------------------------------------

        x_expanded = x.unsqueeze(1)

        centers = self.centers.unsqueeze(0)

        sigmas = (
            torch.abs(self.sigmas)
            .unsqueeze(0)
            + 1e-6
        )

        membership = torch.exp(
            -0.5
            * (
                (x_expanded - centers)
                / sigmas
            ) ** 2
        )


        # ----------------------------------------------------
        # Layer 2: Rule Firing Strength
        # ----------------------------------------------------

        firing_strength = torch.prod(
            membership,
            dim=2
        )

        firing_strength = (
            firing_strength + 1e-8
        )


        # ----------------------------------------------------
        # Layer 3: Normalize Firing Strength
        # ----------------------------------------------------

        normalized_strength = (
            firing_strength
            / firing_strength.sum(
                dim=1,
                keepdim=True
            )
        )


        # ----------------------------------------------------
        # Layer 4: Sugeno Consequent
        # ----------------------------------------------------

        rule_outputs = []

        for rule in range(self.num_rules):

            linear_output = (
                torch.matmul(
                    x,
                    self.consequent_weights[rule]
                )
                + self.consequent_bias[rule]
            )

            rule_outputs.append(
                linear_output
            )

        rule_outputs = torch.stack(
            rule_outputs,
            dim=1
        )


        # ----------------------------------------------------
        # Layer 5: Weighted Sum
        # ----------------------------------------------------

        output = (
            normalized_strength.unsqueeze(2)
            * rule_outputs
        ).sum(dim=1)

        return output


# ============================================================
# CREATE MODEL
# ============================================================

model = MulticlassANFIS(
    num_features=NUM_FEATURES,
    num_rules=NUM_RULES,
    num_classes=NUM_CLASSES
)


# ============================================================
# LOSS AND OPTIMIZER
# ============================================================

class_counts = torch.bincount(
    y_train,
    minlength=NUM_CLASSES
).float()

class_weights = (
    len(y_train)
    / (
        NUM_CLASSES * class_counts
    )
)

class_weights = (
    class_weights
    / class_weights.mean()
)

print("Class weights:")

for class_id, weight in enumerate(class_weights):
    print(
        f"Class {class_id}: "
        f"{weight.item():.4f}"
    )

print()

criterion = nn.CrossEntropyLoss(
    weight=class_weights
)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# ============================================================
# TRAINING
# ============================================================

print("Starting ANFIS training...")
print()

for epoch in range(EPOCHS):

    model.train()

    optimizer.zero_grad()

    outputs = model(X_train)

    loss = criterion(
        outputs,
        y_train
    )

    loss.backward()

    optimizer.step()


    if (
        (epoch + 1) % 50 == 0
        or epoch == 0
    ):

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        train_accuracy = (
            predictions == y_train
        ).float().mean().item()

        print(
            f"Epoch {epoch + 1}/{EPOCHS} "
            f"- Loss: {loss.item():.6f} "
            f"- Train Accuracy: "
            f"{train_accuracy * 100:.2f}%"
        )


# ============================================================
# EVALUATION
# ============================================================

model.eval()

with torch.no_grad():

    test_outputs = model(X_test)

    test_predictions = torch.argmax(
        test_outputs,
        dim=1
    )


# ============================================================
# ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test.numpy(),
    test_predictions.numpy()
)

print()
print("=" * 60)
print("ANFIS MODEL EVALUATION")
print("=" * 60)

print(
    f"Test Accuracy: "
    f"{accuracy * 100:.2f}%"
)

print()


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("Classification Report:")

print(
    classification_report(
        y_test.numpy(),
        test_predictions.numpy(),
        labels=list(range(NUM_CLASSES)),
        target_names=[
            "VUL4J-1",
            "VUL4J-11",
            "VUL4J-18",
            "VUL4J-2",
            "VUL4J-6"
        ],
        zero_division=0
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

torch.save(
    {
        "model_state_dict": model.state_dict(),
        "num_features": NUM_FEATURES,
        "num_rules": NUM_RULES,
        "num_classes": NUM_CLASSES,
        "feature_columns": feature_columns
    },
    MODEL_PATH
)

print(
    f"ANFIS model saved to: "
    f"{MODEL_PATH}"
)