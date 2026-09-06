import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib


# ============================================================
# 1. LOAD COMBINED DATASET
# ============================================================

input_file = "data/cleaned/FIRMS/firms_osm_landcover_clean.csv"

df = pd.read_csv(input_file)

print("==============================================")
print("      INDUSTRIAL FIRE RISK ML MODEL")
print("==============================================")

print("Total records:", len(df))


# ============================================================
# 2. CREATE FIRE RISK TARGET
# ============================================================
# Risk is based mainly on FIRMS fire radiative power (FRP)
#
# LOW    : FRP < 5
# MEDIUM : 5 <= FRP < 15
# HIGH   : FRP >= 15
#
# Higher FRP = stronger detected fire signal.

def assign_risk(frp):

    if frp < 5:
        return "Low"

    elif frp < 15:
        return "Medium"

    else:
        return "High"


df["risk_level"] = df["frp"].apply(assign_risk)


print("\nRisk distribution:")
print(df["risk_level"].value_counts())


# ============================================================
# 3. SELECT FEATURES
# ============================================================

features = [
    "latitude",
    "longitude",
    "brightness",
    "scan",
    "track",
    "confidence",
    "bright_t31",
    "frp",
    "distance_to_industry_m",
    "near_industry",
    "landcover_class",
    "near_industry_500m",
    "near_industry_1km",
    "near_industry_2km"
]

target = "risk_level"


# ============================================================
# 4. PREPARE FEATURES
# ============================================================

X = df[features].copy()
y = df[target].copy()


# Convert confidence into numbers
confidence_mapping = {
    "l": 0,
    "n": 1,
    "h": 2
}

X["confidence"] = X["confidence"].map(confidence_mapping)


# Convert everything to numeric
for column in X.columns:
    X[column] = pd.to_numeric(X[column], errors="coerce")


# Fill missing values
X = X.fillna(X.median(numeric_only=True))


# ============================================================
# 5. ENCODE TARGET
# ============================================================

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)


# ============================================================
# 6. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ============================================================
# 7. TRAIN RANDOM FOREST
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)


print("\nRandom Forest training completed!")


# ============================================================
# 8. EVALUATE MODEL
# ============================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================================")
print("MODEL EVALUATION")
print("==============================================")

print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ============================================================
# 9. SAVE MODEL
# ============================================================

model_file = "models/fire_risk_model.pkl"

joblib.dump(model, model_file)

joblib.dump(
    label_encoder,
    "models/risk_label_encoder.pkl"
)


print("\n==============================================")
print("MODEL SAVED")
print("==============================================")

print("Model:", model_file)
print("Label encoder: models/risk_label_encoder.pkl")
print("\nDONE!")