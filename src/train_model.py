import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    average_precision_score
)

from imblearn.over_sampling import SMOTE

# =========================
# 1. Load Dataset
# =========================
df = pd.read_csv("data/raw/creditcard.csv")

print("Dataset Loaded:", df.shape)

# =========================
# 2. Feature Engineering
# =========================
df['Hour'] = df['Time'] // 3600 % 24
df['Amount_log'] = np.log1p(df['Amount'])

df = df.drop(['Time'], axis=1)

print("Feature Engineering Done")

# =========================
# 3. Split Data
# =========================
X = df.drop('Class', axis=1)
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

print("Train-Test Split Done")

# =========================
# 4. Scaling (SAFE METHOD)
# =========================
scaler = StandardScaler()

X_train.loc[:, 'Amount'] = scaler.fit_transform(X_train[['Amount']])
X_test.loc[:, 'Amount'] = scaler.transform(X_test[['Amount']])

print("Scaling Done")

# =========================
# 5. Handle Imbalance (SMOTE)
# =========================
smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(X_train, y_train)

print("\nAfter SMOTE:")
print(pd.Series(y_train).value_counts())

# =========================
# 6. Train Model
# =========================
model = RandomForestClassifier(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

print("Model Training Done")

# =========================
# 7. Default Prediction (Threshold = 0.5)
# =========================
y_pred = model.predict(X_test)

print("\n=== DEFAULT THRESHOLD (0.5) ===")
print(classification_report(y_test, y_pred))

# =========================
# 8. Confusion Matrix
# =========================
cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix (Default)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("images/confusion_matrix.png")
plt.show()

# =========================
# 9. Probability Predictions
# =========================
y_prob = model.predict_proba(X_test)[:, 1]

# PR-AUC Score
pr_auc = average_precision_score(y_test, y_prob)
print(f"\nPR-AUC Score: {pr_auc:.4f}")

# =========================
# 10. Precision-Recall Curve
# =========================
precision, recall, thresholds = precision_recall_curve(y_test, y_prob)

plt.figure()
plt.plot(thresholds, precision[:-1], label="Precision")
plt.plot(thresholds, recall[:-1], label="Recall")
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision vs Recall Tradeoff")
plt.legend()
plt.savefig("images/precision_recall_curve.png")
plt.show()

# =========================
# 11. Threshold Tuning
# =========================
print("\n=== THRESHOLD TUNING ===")

for t in [0.5, 0.4, 0.3, 0.2]:
    y_pred_t = (y_prob > t).astype(int)
    print(f"\nThreshold: {t}")
    print(classification_report(y_test, y_pred_t))

# =========================
# 12. Best Threshold (Example)
# =========================
best_threshold = 0.3

y_pred_best = (y_prob > best_threshold).astype(int)

print("\n=== BEST MODEL (Threshold = 0.3) ===")
print(classification_report(y_test, y_pred_best))

cm_best = confusion_matrix(y_test, y_pred_best)

plt.figure()
sns.heatmap(cm_best, annot=True, fmt='d', cmap='Reds')
plt.title(f"Confusion Matrix (Threshold={best_threshold})")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("images/confusion_matrix_best.png")
plt.show()

joblib.dump(model, "models/fraud_model.pkl")
print("Model saved successfully!")

MODEL_PATH = "models/fraud_model.pkl"

# =========================
# CHECK IF MODEL EXISTS
# =========================
if os.path.exists(MODEL_PATH):
    print("Loading existing model...")
    model = joblib.load(MODEL_PATH)

else:
    print("Training new model...")

    # =========================
    # Handle Imbalance (SMOTE)
    # =========================
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    print("\nAfter SMOTE:")
    print(pd.Series(y_train_res).value_counts())

    # =========================
    # Train Model
    # =========================
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_res, y_train_res)

    # Save model
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved successfully!")