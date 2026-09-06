import pandas as pd
import joblib


# ============================================================
# 1. LOAD DATASET
# ============================================================

input_file = "data/cleaned/FIRMS/firms_osm_landcover_clean.csv"

df = pd.read_csv(input_file)

print("==============================================")
print("       INDUSTRIAL FIRE RISK PREDICTION")
print("==============================================")

print("Total records:", len(df))


# ============================================================
# 2. LOAD TRAINED MODEL
# ============================================================

model = joblib.load("models/fire_risk_model.pkl")
label_encoder = joblib.load("models/risk_label_encoder.pkl")

print("Trained model loaded successfully!")


# ============================================================
# 3. SELECT SAME FEATURES USED DURING TRAINING
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

X = df[features].copy()


# ============================================================
# 4. CONVERT CONFIDENCE TO NUMBERS
# ============================================================

confidence_mapping = {
    "l": 0,
    "n": 1,
    "h": 2
}

X["confidence"] = X["confidence"].map(confidence_mapping)


# ============================================================
# 5. CONVERT FEATURES TO NUMERIC
# ============================================================

for column in X.columns:
    X[column] = pd.to_numeric(X[column], errors="coerce")


# Fill missing values
X = X.fillna(X.median(numeric_only=True))


# ============================================================
# 6. GENERATE PREDICTIONS
# ============================================================

predictions = model.predict(X)


# Convert numbers back to Low / Medium / High
df["predicted_risk"] = label_encoder.inverse_transform(predictions)


# ============================================================
# 7. SAVE PREDICTIONS
# ============================================================

output_file = "data/cleaned/FIRMS/jamshedpur_fire_risk_predictions.csv"

df.to_csv(output_file, index=False)


# ============================================================
# 8. DISPLAY RESULTS
# ============================================================

print("\n==============================================")
print("PREDICTION COMPLETE")
print("==============================================")

print("Total predictions:", len(df))

print("\nRisk distribution:")
print(df["predicted_risk"].value_counts())

print("\nOutput file:")
print(output_file)

print("\nDONE!")