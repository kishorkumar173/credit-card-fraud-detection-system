import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

print("Training model...")

# Load dataset
df = pd.read_csv("data/raw/creditcard.csv")

# Feature Engineering
df['Hour'] = df['Time'] // 3600 % 24
df['Amount_log'] = np.log1p(df['Amount'])
df = df.drop(['Time'], axis=1)

# Split
X = df.drop('Class', axis=1)
y = df['Class']

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train.loc[:, 'Amount'] = scaler.fit_transform(X_train[['Amount']])

# SMOTE
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/fraud_model.pkl")

print("✅ Model saved successfully!")