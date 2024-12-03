import json

# Path to the text file with links
links_file_path = './old/scrape_prices/urls/AX13090_urls.txt'

# Path to the JSON file
json_file_path = 'safe.json'

# Read the links from the text file
with open(links_file_path, 'r') as file:
    links = file.readlines()

# Create a dictionary with each link as a key and 0.0 as the value
data = {link.strip(): 0.0 for link in links}

# Write the dictionary to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data has been written to {json_file_path}")