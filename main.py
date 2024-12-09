from competition_links.playwright_links import collect_google_links
from filter_links.filter_links import filter_links, extract_keywords
from dictionary.manipulate_dict import initialize_dict, remove_entries_without_file_path
from download_html.download_html import save_html
from html_product_name.html_product_name_filter import filter_dictionary_by_item_name
from extract_price.extract_price import extract_price_list
from extract_price_2.extract_price import extract_prices_from_dict
from graph.graph import filter_outliers, save_table
from llm import extract_price_dict
import json


# sku_list = ['HD100-BC', 'MIRA403 BODY ARMOR PLATE LEVEL 4 NIJ', 'BC-TS-33901', 'NRA-EIC COMBAT',
#             'AX13090', '335-01', 'NSGNYX15M5G9DX2', 'TAVT36WN9COLL102', 'TAVT36MNASIDE101',
#             'TIBNBX4381L', '403018', 'B1755111']

upc = '810081911696'
item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
# item_name = 'Anker 2x SOLIX F3800 + Double Power Hub'
# item_name = 'Ace Link Armor Ballistic Helmet Gen 2 Coyote Brown'
# item_name = 'ATN BinoX 4T 384 1.25-5x Thermal Binoculars'
# item_name = 'Renogy 12V 100Ah Smart Lithium Iron Phosphate Battery & BT-2 & Renogy ONE Core'
# item_name = 'Ace Link Armor Level 3 Armor Plate Swimmers Cut'


def main():
    # if not upc:
    #     print('No SKU list found')
    #     return

    # url_list = collect_google_links(item_name, 30, extract_keywords(item_name))
    # if not url_list:
    #     print('No links found')
    #     return
    
    # filtered_url_dict = filter_links(url_list, item_name)
    # if not filtered_url_dict:
    #     print('No filtered links found')
    #     return
    
    # print(f'Number of filtered links: {len(filtered_url_dict)}')
    # with open('filter_url_dict.json', 'w') as file:
    #     json.dump(filtered_url_dict, file, indent=4)
    
    
    # url_dict = initialize_dict(url_list)
    # if not url_dict:
    #     print('No dictionary created')
    #     return

    # with open('filter_url_dict.json', 'r') as file:
    #     filtered_url_dict = json.load(file)
    
    # html_dict = save_html(filtered_url_dict)
    # if not html_dict:
    #     print('No html saved')
    #     return
    
    # with open('html_dict.json', 'w') as file:
    #     json.dump(html_dict, file, indent=4)
    
    # # with open('html_dict.json', 'r') as file:
    # #     html_dict = json.load(file)

    # product_name_dict = filter_dictionary_by_item_name(html_dict, item_name, upc)
    # if not product_name_dict:
    #     print('No product name found')
    #     return
    
    # with open('product_name_dict.json', 'w') as file:
    #     json.dump(product_name_dict, file, indent=4)

    # # for key, value in html_dict.items():
    # #     print(f'{key}: {value}')


    # html_dict = remove_entries_without_file_path(html_dict)
    # if not html_dict:
    #     print('No html saved')
    #     return
    
    # with open('test.json', 'w') as json_file:
    #     json.dump(html_dict, json_file, indent=4)

    # # with open('test.json', 'r') as json_file:
    # #     html_dict = json.load(json_file)

    # # with open('product_name_dict.json', 'r') as file:
    # #     product_name_dict = json.load(file)

    # price_dict = extract_price_dict(html_dict)
    # with open('price_dict.json', 'w') as file:
    #     json.dump(price_dict, file, indent=4)

    with open('price_dict.json', 'r') as file:
        price_dict = json.load(file)

    # price_dict = extract_prices_from_dict(product_name_dict, item_name)
    # for key, value in price_dict.items():
    #     print(f'{key}: {value}')

    # price_dict = extract_price_list(product_name_dict, item_name)
    price_dict = filter_outliers(price_dict)
    with open('filtered_price_dict.json', 'w') as file:
        json.dump(price_dict, file, indent=4)
    # for value in price_dict.values():
    #     if 'value' in value:
    #         print(f'price: {value["value"]}\nurl: {value["url"]}')
    #     else:
    #         print(f'Missing value for URL: {value["url"]}')

    # price_list = [value['value'] for value in price_dict.values() if 'value' in value]
    # price_list.sort()
    # print(price_list)

    # # print(price_dict)

    # save_table(price_dict, 'data.xlsx')
  

if __name__ == "__main__":
    main()