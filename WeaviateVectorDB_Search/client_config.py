import os
import weaviate

def get_client():
    url = "https://[your-web-app].azurewebsites.net/"
    api_key = os.getenv("WEAVIATE_API_KEY")
    auth_client_secret = weaviate.AuthApiKey(api_key=api_key)
    client = weaviate.Client(url=url, auth_client_secret=auth_client_secret)
    return client
