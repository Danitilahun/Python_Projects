import json
from client_config import get_client

def initialize_client():
    """Initialize and return a Weaviate client instance."""
    return get_client()

def perform_query(client, query, limit=10, distance=0.6):
    """Perform a text-based search query in Weaviate and return the response."""
    response = (
        client.query
        .get("Page", ["chapter", "body", "pageNumber", "inBook{ ... on Book{title}}"])
        .with_near_text({
            "concepts": [query],
            "distance": distance,
        })
        .with_limit(limit)
        .with_additional(["id", "distance", "vector"])
        .do()
    )
    return response

def process_results(response):
    """Extract relevant information from the query response and return a list of results."""
    results = []
    pages = response['data']['Get']['Page']
    for page in pages:
        result = {
            'id': page['_additional']['id'],
            'title': page['inBook'][0]['title'],
            'chapter': page['chapter'],
            'content': page['body'],
            'page': page['pageNumber']
        }
        results.append(result)
    return results

def main():
    client = initialize_client()
    query = "supersonic combustion"
    response = perform_query(client, query)
    
    results = process_results(response)
    
    print(json.dumps(response, indent=2))  # Printing the full raw response for debugging or detailed review
    print(f"Results: {len(results)}")      # Printing the number of results
    print(results)                         # Printing the processed results

if __name__ == "__main__":
    main()
