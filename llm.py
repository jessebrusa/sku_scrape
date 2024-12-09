from bs4 import BeautifulSoup
import re
import json
import os

delete_html_files = True

def extract_price(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check for price in script tags
    script_tags = soup.find_all("script")
    for script in script_tags:
        if script.string and "ecomm_totalvalue" in script.string:
            match = re.search(r'"ecomm_totalvalue":(\d+\.\d+)', script.string)
            if match:
                return float(match.group(1))

    # Check for price in specific tag with id="lspr"
    price_tag = soup.find("input", {"id": "lspr"})
    if price_tag and price_tag.has_attr("value"):
        return float(price_tag["value"])

    # Fallback: Extract visible price
    price_tags = soup.find_all(
        lambda tag: tag.name in ["span", "div", "p"] and 
                    ("price" in tag.get("class", []) or "price" in tag.get("id", ""))
    )
    for tag in price_tags:
        text = tag.get_text(strip=True)
        prices = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
        if prices:
            # Filter out prices that are too low (e.g., $4.99)
            valid_prices = [price for price in prices if float(price.replace("$", "").replace(",", "")) > 100]
            if valid_prices:
                return float(valid_prices[0].replace("$", "").replace(",", ""))

    # Fallback: Regex
    prices = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', html_content)
    if prices:
        # Filter out prices that are too low (e.g., $4.99)
        valid_prices = [price for price in prices if float(price.replace("$", "").replace(",", "")) > 100]
        if valid_prices:
            return float(valid_prices[0].replace("$", "").replace(",", ""))

    return None


def extract_price_dict(data_dict):
    keys_to_remove = []
    for key, value in data_dict.items():
        file_path = value.get("file_path")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            price = extract_price(html_content)
            if price is not None:
                value["price"] = price
            else:
                keys_to_remove.append(key)
    
            if delete_html_files:
                os.remove(file_path)

    for key in keys_to_remove:
        del data_dict[key]
    
    return data_dict

# Example Usage
if __name__ == "__main__":
    with open('product_name_dict.json', 'r') as file:
        product_name_dict = json.load(file)

    for value in product_name_dict.values():
        file_path = value["file_path"]
    
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        result = extract_price(html_content)
        print(f'price: {result['price']}\nurl: {value['url']}')