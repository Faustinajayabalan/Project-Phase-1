import pandas as pd
import numpy as np
import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# -------------------------------------------------
# 1. LOAD DATASET
# -------------------------------------------------

dataset_path = (
    r"D:\NeuroFuzzy-Security\dataset\processed"
    r"\anfis_ready_dataset.csv"
)

df = pd.read_csv(dataset_path)

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


# -------------------------------------------------
# 2. TRAIN / TEST SPLIT
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)

y_train = torch.tensor(
    y_train,
    dtype=torch.float32
).reshape(-1, 1)

y_test = torch.tensor(
    y_test,
    dtype=torch.float32
).reshape(-1, 1)


# -------------------------------------------------
# 3. IMPROVED SUGENO ANFIS
# -------------------------------------------------

class ANFIS(nn.Module):

    def __init__(self, input_size):

        super().__init__()

        self.input_size = input_size

        # Two Gaussian membership functions
        # for every feature:
        #
        # 0 = Low
        # 1 = High

        self.centers = nn.Parameter(
            torch.tensor(
                [
                    [0.25, 0.75]
                    for _ in range(input_size)
                ],
                dtype=torch.float32
            )
        )

        self.sigmas = nn.Parameter(
            torch.ones(
                input_size,
                2
            ) * 0.35
        )

        # -------------------------------------------------
        # Selected fuzzy rules
        #
        # Each number represents:
        # 0 = Low
        # 1 = High
        #
        # We use 4 rules instead of 2048 possible rules.
        # -------------------------------------------------

        self.rules = torch.tensor(
            [
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
                [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
                [0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]
            ],
            dtype=torch.long
        )

        number_of_rules = self.rules.shape[0]

        # Sugeno consequent parameters
        #
        # Each rule has:
        # 11 feature weights + 1 bias

        self.consequents = nn.Parameter(
            torch.zeros(
                number_of_rules,
                input_size + 1
            )
        )


    def forward(self, x):

        # -------------------------------------------------
        # Layer 1
        # Gaussian membership functions
        # -------------------------------------------------

        membership = torch.exp(
            -(
                (
                    x.unsqueeze(2)
                    - self.centers
                ) ** 2
            )
            /
            (
                2 * self.sigmas.abs() ** 2
                + 1e-6
            )
        )


        # -------------------------------------------------
        # Layer 2
        # Calculate firing strength for each rule
        # -------------------------------------------------

        rule_strengths = []

        for rule in self.rules:

            selected_memberships = []

            for feature_index in range(
                self.input_size
            ):

                membership_index = rule[
                    feature_index
                ]

                selected_memberships.append(
                    membership[
                        :,
                        feature_index,
                        membership_index
                    ]
                )

            selected_memberships = torch.stack(
                selected_memberships,
                dim=1
            )

            strength = torch.prod(
                selected_memberships,
                dim=1
            )

            rule_strengths.append(strength)


        firing_strengths = torch.stack(
            rule_strengths,
            dim=1
        )


        # -------------------------------------------------
        # Layer 3
        # Normalize firing strengths
        # -------------------------------------------------

        normalized_strengths = (
            firing_strengths
            /
            (
                torch.sum(
                    firing_strengths,
                    dim=1,
                    keepdim=True
                )
                + 1e-6
            )
        )


        # -------------------------------------------------
        # Layer 4
        # Sugeno rule outputs
        # -------------------------------------------------

        bias = torch.ones(
            x.shape[0],
            1
        )

        x_with_bias = torch.cat(
            [x, bias],
            dim=1
        )

        rule_outputs = torch.matmul(
            x_with_bias,
            self.consequents.T
        )


        # -------------------------------------------------
        # Layer 5
        # Weighted final output
        # -------------------------------------------------

        output = torch.sum(
            normalized_strengths
            * rule_outputs,
            dim=1,
            keepdim=True
        )

        return torch.sigmoid(output)


# -------------------------------------------------
# 4. CREATE MODEL
# -------------------------------------------------

model = ANFIS(
    input_size=len(feature_columns)
)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.01
)

loss_function = nn.BCELoss()


# -------------------------------------------------
# 5. TRAIN
# -------------------------------------------------

epochs = 1000

for epoch in range(epochs):

    model.train()

    predictions = model(X_train)

    loss = loss_function(
        predictions,
        y_train
    )

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (epoch + 1) % 100 == 0:

        print(
            f"Epoch {epoch + 1}/{epochs} "
            f"- Loss: {loss.item():.6f}"
        )


# -------------------------------------------------
# 6. EVALUATE
# -------------------------------------------------

model.eval()

with torch.no_grad():

    predictions = model(X_test)

    predicted_labels = (
        predictions >= 0.5
    ).float()


accuracy = accuracy_score(
    y_test.numpy(),
    predicted_labels.numpy()
)


print()
print("=" * 50)
print("IMPROVED ANFIS MODEL RESULTS")
print("=" * 50)

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

print()

print(
    classification_report(
        y_test.numpy(),
        predicted_labels.numpy(),
        target_names=[
            "Patched",
            "Vulnerable"
        ],
        zero_division=0
    )
)


# -------------------------------------------------
# 7. SAVE MODEL
# -------------------------------------------------

model_path = (
    r"D:\NeuroFuzzy-Security\ml\models"
    r"\anfis_model.pth"
)

torch.save(
    model.state_dict(),
    model_path
)

print(
    f"ANFIS model saved to: {model_path}"
)