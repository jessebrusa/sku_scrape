def count_and_write_product_links(file_path, keywords, output_file):
    count = 0
    good_links = set()  # Use a set to store unique links
    with open(file_path, 'r') as file:
        for line in file:
            link = line.strip()
            if any(keyword.lower() in link.lower() for keyword in keywords):
                good_links.add(link)  # Add link to the set

    # Write the good links to the output file
    with open(output_file, 'w') as file:
        for link in good_links:
            file.write(link + '\n')

    return len(good_links)  # Return the count of unique links

if __name__ == "__main__":
    file_path = 'playwright.txt'
    output_file = 'good_links.txt'
    keywords = ['armasight', 'collector', '320', '1.5-6x19', 'compact', 'thermal', 'weapon', 'sight']
    product_link_count = count_and_write_product_links(file_path, keywords, output_file)
    print(f"Number of product-related links: {product_link_count}")