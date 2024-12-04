def initialize_dict(links):
    return {i: {'url': link} for i, link in enumerate(links)}

def remove_entries_without_file_path(data_dict):
    keys_to_remove = [key for key, value in data_dict.items() if 'file_path' not in value]
    for key in keys_to_remove:
        del data_dict[key]
    return data_dict

if __name__ == "__main__":
    # Example usage
    links = [
        'https://www.example.com',
        'https://www.example.org',
        'https://www.example.net'
    ]
    result = initialize_dict(links)
    print("Initial dictionary:")
    print(result)

    # Example dictionary with some entries missing 'file_path'
    example_dict = {
        0: {'url': 'https://www.example.com', 'file_path': 'temp/0.html'},
        1: {'url': 'https://www.example.org'},
        2: {'url': 'https://www.example.net', 'file_path': 'temp/2.html'},
        3: {'url': 'https://www.example.info'}
    }
    print("\nDictionary before removing entries without 'file_path':")
    print(example_dict)

    updated_dict = remove_entries_without_file_path(example_dict)
    print("\nDictionary after removing entries without 'file_path':")
    print(updated_dict)