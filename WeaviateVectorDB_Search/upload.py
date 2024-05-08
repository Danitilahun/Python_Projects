import json
from client_config import get_client

JSON_FILE = "Rocket_Propulsion_Elements.json"

def load_data(json_file):
    """Load data from a JSON file."""
    with open(json_file, 'r') as file:
        data = json.load(file)
    print("Top-level keys in JSON:", list(data.keys()))  # Print to debug the structure of JSON
    return data

def add_book(client, book_data):
    """Add a book object to Weaviate and return the UUID."""
    book_data.pop('pages', None)  # Remove 'pages' key safely
    book_id = client.data_object.create(book_data, 'Book')
    print('Book Added:', book_id)
    return book_id

def add_pages(client, pages, book_id):
    """Add pages to Weaviate and set up references to/from the book."""
    for page in pages:
        page['pageNumber'] = page.pop('page', None)  # Rename 'page' to 'pageNumber'
        page_id = client.data_object.create(page, 'Page')
        print('Page Added:', page_id)

        # Add reference from the book to the page
        client.data_object.reference.add(
            from_class_name="Book",
            from_uuid=book_id,
            from_property_name="hasPages",
            to_class_name="Page",
            to_uuid=page_id,
        )
        # Add reference from the page to the book
        client.data_object.reference.add(
            from_class_name="Page",
            from_uuid=page_id,
            from_property_name="inBook",
            to_class_name="Book",
            to_uuid=book_id,
        )

def main():
    client = get_client()
    if client.is_ready():
        print("Client is ready")

        # Load book data
        book_json = load_data(JSON_FILE)

        # Add book to Weaviate
        book_id = add_book(client, book_json)

        # Add pages to Weaviate and create references if 'pages' key exists
        pages = book_json.get('pages', [])  # Default to an empty list if 'pages' is not found
        if pages:  # Only proceed if there are pages
            add_pages(client, pages, book_id)

        print('All data added and referenced successfully.')

if __name__ == "__main__":
    main()
