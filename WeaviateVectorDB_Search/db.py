import weaviate
from client_config import get_client

def initialize_client():
    """Initialize and return a Weaviate client instance."""
    client = get_client()
    if client.is_ready():
        print("Client is ready")
    else:
        print("Client is not ready")
    return client

def create_class(client, schema):
    """Create a class in the Weaviate schema."""
    try:
        result = client.schema.create_class(schema)
        print(f"Class '{schema['class']}' created successfully.")
        return result
    except Exception as ex:
        print(f"Failed to create class '{schema['class']}': {ex}")

def create_property(client, class_name, property_schema):
    """Add a property to a class in the Weaviate schema."""
    try:
        client.schema.property.create(class_name, property_schema)
        print(f"Property '{property_schema['name']}' added to class '{class_name}'.")
    except Exception as ex:
        print(f"Failed to add property '{property_schema['name']}' to class '{class_name}': {ex}")

def get_schema(client):
    """Retrieve and print the current schema from Weaviate."""
    schema = client.schema.get()
    print("Current Schema:", schema)
    return schema

def main():
    client = initialize_client()

    book_schema = {
        "class": "Book",
        "properties": [
            {"name": "title", "dataType": ["text"]},
            {"name": "author", "dataType": ["text"]},
            {"name": "hasPages", "dataType": ["Page"]}
        ],
    }

    page_schema = {
        "class": "Page",
        "properties": [
            {"name": "chapter", "dataType": ["text"]},
            {"name": "body", "dataType": ["text"]},
            {"name": "pageNumber", "dataType": ["int"]},
            {"name": "inBook", "dataType": ["Book"]}
        ],
    }

    # Create Book and Page classes
    create_class(client, book_schema)
    create_class(client, page_schema)

    # Optionally, create a property explicitly if needed
    # create_property(client, 'Book', book_schema['properties'][2])

    # Display the current schema
    get_schema(client)

if __name__ == "__main__":
    main()
