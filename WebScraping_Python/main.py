import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.flipkart.com/search?q=canon+cameras&sid=jek%2Cp31%2Ctrv&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_5_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_5_na_na_na&as-pos=2&as-type=HISTORY&suggestionId=canon+cameras%7CDSLR+%26+Mirrorless&requestId=14604aab-7662-46f2-9f8e-0bb4cbb8a4e3&p%5B%5D=facets.price_range.from%3D30000&p%5B%5D=facets.price_range.to%3DMax"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

camera_data = []

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
camera_cards = soup.find_all("div", class_="_1AtVbE")

for camera_card in camera_cards:
    try:
        camera_name = camera_card.find("div", class_="_4rR01T").text
        camera_price = camera_card.find("div", class_="_30jeq3").text if camera_card.find("div", class_="_30jeq3") else "N/A"
        camera_rating = camera_card.find("div", class_="_3LWZlK").text if camera_card.find("div", class_="_3LWZlK") else "N/A"

        camera_data.append({
            "Name": camera_name,
            "Price": camera_price,
            "Rating": camera_rating
        })
    except Exception as e:
        print("Error in extracting camera data:", e)

df = pd.DataFrame(camera_data)
df.to_csv("Cameras.csv", index=False)

print("Data successfully extracted and CSV saved.")