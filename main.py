from competition_links.collect_links import collect_links
from dictionary.manipulate_dict import initialize_dict, remove_entries_without_file_path
from download_html.download_html import save_html
from extract_price.extract_price import extract_price_list


# sku_list = ['HD100-BC', 'MIRA403 BODY ARMOR PLATE LEVEL 4 NIJ', 'BC-TS-33901', 'NRA-EIC COMBAT',
#             'AX13090', '335-01', 'NSGNYX15M5G9DX2', 'TAVT36WN9COLL102', 'TAVT36MNASIDE101',
#             'TIBNBX4381L', '403018', 'B1755111']

sku = 'HD100-BC'

def main():
    if not sku:
        print('No SKU list found')
        return

    url_list = collect_links(sku)
    if not url_list:
        print('No links found')
        return
    
    url_dict = initialize_dict(url_list)
    if not url_dict:
        print('No dictionary created')
        return
    
    html_dict = save_html(url_dict)
    if not html_dict:
        print('No html saved')
        return

    html_dict = remove_entries_without_file_path(html_dict)
    if not html_dict:
        print('No html saved')
        return

    price_dict = extract_price_list(html_dict)
    for key, value in price_dict.items():
        print(f'price: {value["value"]}\nurl: {value["url"]}')
  

    


    

    




if __name__ == "__main__":
    main()