from competition_links.playwright_links import collect_google_links
from filter_links.filter_links import filter_links
from dictionary.manipulate_dict import initialize_dict, remove_entries_without_file_path
from download_html.download_html import save_html
from extract_price.extract_price import extract_price_list
import json


# sku_list = ['HD100-BC', 'MIRA403 BODY ARMOR PLATE LEVEL 4 NIJ', 'BC-TS-33901', 'NRA-EIC COMBAT',
#             'AX13090', '335-01', 'NSGNYX15M5G9DX2', 'TAVT36WN9COLL102', 'TAVT36MNASIDE101',
#             'TIBNBX4381L', '403018', 'B1755111']

upc = '810081911696'
item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'

def main():
    # if not upc:
    #     print('No SKU list found')
    #     return

    # url_list = collect_google_links(item_name)
    # if not url_list:
    #     print('No links found')
    #     return

    # with open('playwright.txt', 'r') as file:
    #     url_list = [line.strip() for line in file.readlines()]
    # if url_list:
    #     print(f'Number of links: {len(url_list)}')
    
    # if not url_list:
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

    with open('filter_url_dict.json', 'r') as file:
        filtered_url_dict = json.load(file)
    
    html_dict = save_html(filtered_url_dict)
    if not html_dict:
        print('No html saved')
        return
    

    # for key, value in html_dict.items():
    #     print(f'{key}: {value}')


    # html_dict = remove_entries_without_file_path(html_dict)
    # if not html_dict:
    #     print('No html saved')
    #     return
    
    # # with open('test.json', 'w') as json_file:
    # #     json.dump(html_dict, json_file, indent=4)

    # # with open('test.json', 'r') as json_file:
    # #     html_dict = json.load(json_file)

    # price_dict = extract_price_list(html_dict)
    # for value in price_dict.values():
    #     if 'value' in value:
    #         print(f'price: {value["value"]}\nurl: {value["url"]}')
    #     else:
    #         print(f'Missing value for URL: {value["url"]}')

    # price_list = [value['value'] for value in price_dict.values() if 'value' in value]
    # price_list.sort()
    # print(price_list)
  

if __name__ == "__main__":
    main()