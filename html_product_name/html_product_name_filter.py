import os
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def filter_dictionary_by_item_name(data_dict, item_name, upc):
    filtered_dict = {}
    item_name = item_name.lower()
    upc = upc.lower()
    
    for key, value in data_dict.items():
        file_path = value.get('file_path')
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                text = soup.get_text().lower()
                item_name_score = fuzz.partial_ratio(item_name, text)
                upc_score = fuzz.partial_ratio(upc, text)
                
                if item_name_score > 70 or upc_score > 70:  # Adjust the threshold as needed
                    filtered_dict[key] = value
        else:
            print(f"File not found: {file_path}")
    
    return filtered_dict

if __name__ == "__main__":
    html_dict = {
        'www.reddit.com': {'file_path': 'temp/www.reddit.com.html'},
        'example.com': {'file_path': 'temp/example.com.html'}
    }
    item_name = "Example Item"
    upc = "123456789012"
    filtered_dict = filter_dictionary_by_item_name(html_dict, item_name, upc)
    print(filtered_dict)