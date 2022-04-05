from mock_data import catalog



def find_prod():
    text = "a"
    c = 0
    
    for title in catalog:
        text = text.lower()
        if text in title["title"]:
            c+=1
            print(f'{title["title"]}, Price: ${title["price"]}')
    print(f"{c} items have the word '{text}'")

def unique_categories():
    categories = []
    for prod in catalog:
        category = prod["category"]

        if not category in categories:
            categories.append(category)

    print(categories)


find_prod()
unique_categories()