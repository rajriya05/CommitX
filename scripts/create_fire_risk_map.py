import pandas as pd
import folium

# ============================================================
# 1. LOAD PREDICTION DATA
# ============================================================

input_file = "data/cleaned/FIRMS/jamshedpur_fire_risk_predictions.csv"

df = pd.read_csv(input_file)

print("==============================================")
print("       JAMSHEDPUR FIRE RISK MAP")
print("==============================================")

print("Total records:", len(df))


# ============================================================
# 2. CREATE MAP
# ============================================================

m = folium.Map(
    location=[22.80, 86.22],
    zoom_start=12,
    tiles="OpenStreetMap"
)


# ============================================================
# 3. ADD FIRE POINTS
# ============================================================

for _, row in df.iterrows():

    risk = row["predicted_risk"]

    if risk == "High":
        color = "red"

    elif risk == "Medium":
        color = "orange"

    else:
        color = "green"

    popup_text = f"""
    <b>Fire Risk:</b> {risk}<br>
    <b>FRP:</b> {row['frp']}<br>
    <b>Brightness:</b> {row['brightness']}<br>
    <b>Confidence:</b> {row['confidence']}<br>
    <b>Land Cover:</b> {row['landcover_name']}<br>
    <b>Distance to Industry:</b> {row['distance_to_industry_m']:.2f} m<br>
    <b>Near Industry:</b> {row['near_industry']}
    """

    folium.CircleMarker(
        location=[
            row["latitude"],
            row["longitude"]
        ],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(
            popup_text,
            max_width=300
        )
    ).add_to(m)


# ============================================================
# 4. SAVE MAP
# ============================================================

output_file = "data/cleaned/FIRMS/jamshedpur_fire_risk_map.html"

m.save(output_file)


print("\n==============================================")
print("MAP CREATION COMPLETE")
print("==============================================")

print("Map saved at:")
print(output_file)

print("\nDONE!")