import requests

def get_product_links(upc, api_key):
    url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'products' in data:
            products = data['products']
            links = []
            for product in products:
                if 'stores' in product:
                    for store in product['stores']:
                        if 'link' in store:
                            links.append(store['link'])
            return links
        else:
            print(f"Error: No products found for UPC {upc}")
            return []
    else:
        print(f"HTTP Error: {response.status_code}")
        return []

if __name__ == "__main__":
    upc = "810081911696"  # Example UPC code
    api_key = "your_api_key_here"  # Replace with your Barcode Lookup API key
    links = get_product_links(upc, api_key)
    print(links)