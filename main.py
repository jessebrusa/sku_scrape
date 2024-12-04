from competition_links.collect_links import collect_links


sku_list = ['HD100-BC', 'MIRA403 BODY ARMOR PLATE LEVEL 4 NIJ', 'BC-TS-33901', 'NRA-EIC COMBAT',
            'AX13090', '335-01', 'NSGNYX15M5G9DX2', 'TAVT36WN9COLL102', 'TAVT36MNASIDE101',
            'TIBNBX4381L', '403018', 'B1755111']

def main():
    if not sku_list:
        print('No SKU list found')
        return

    links_list = collect_links(sku_list)
    if not links_list:
        print('No links found')
        return



if __name__ == "__main__":
    main()