import requests

url = "https://mapservice.gov.in/gismapservice/rest/services/BharatMapService/Admin_Boundary_District/MapServer/1/query"

params = {
    "where": "stname='Jharkhand' AND dtname='East Singhbhum'",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "geojson"
}

response = requests.get(url)

print("Status:", response.status_code)

if response.status_code == 200:
    output = r"C:\Users\hp\Documents\SIH_Industrial_Fire_Project\data\raw\Boundary\east_singhbhum.geojson"

    with open(output, "wb") as file:
        file.write(response.content)

    print("East Singhbhum boundary downloaded successfully!")
    print(output)
else:
    print(response.text)