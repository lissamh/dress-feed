import requests
import json

API_URL = "https://www.asos.com/api/product/search/v2"

params = {
    "country": "AU",
    "lang": "en-AU",
    "currency": "AUD",
    "store": "COM",
    "offset": 0,
    "limit": 30,
    "q": "dress",
    "categoryId": "8799",  # dresses
    "refine": "attribute_1047:Size 18",
    "sort": "freshness"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_asos():
    all_dresses = []

    for offset in range(0, 120, 30):  # scrape first 4 pages (adjust as needed)
        params["offset"] = offset
        response = requests.get(API_URL, params=params, headers=headers)
        data = response.json()
        
        for item in data.get("products", []):
            price = item.get("price", {}).get("current", {}).get("value", 0)
            if price <= 70:
                dress = {
                    "image": item.get("imageUrl"),
                    "name": item.get("name"),
                    "price": f"${price:.2f}",
                    "link": f"https://www.asos.com/au/{item.get('url')}",
                }
                all_dresses.append(dress)

    with open("dresses.json", "w") as f:
        json.dump(all_dresses, f, indent=2)

if __name__ == "__main__":
    scrape_asos()
