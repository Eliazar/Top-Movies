from dotenv import load_dotenv
import requests
import os

class MovieHandler:
    load_dotenv()
    
    def __init__(self):
        token = os.getenv("AUTHORIZATION_TOKEN")
        
        self.base_url = "https://api.themoviedb.org/3/"
        self.headers = {
            "Authorization": token
        }

        uri = f"{self.base_url}configuration"

        self.response = requests.get(url=uri, headers=self.headers)
        self.response.raise_for_status()

        result = self.response.json()

        image_configuration = result.get("images")
        self.img_base_url = image_configuration.get("base_url")
        self.img_poster_ratio = image_configuration.get("poster_sizes")[4]

    
    def get_movies(self, movie_name):
        payload = {
            "query": movie_name
        }

        uri = f"{self.base_url}search/movie"
        
        self.response = requests.get(
            url=uri,
            headers=self.headers,
            params=payload)
        self.response.raise_for_status()
        
        results = self.response.json()
        movies = results.get("results")
        selected_movies = [{"id":movie["id"], "title":movie["title"], "release_date":movie["release_date"]} for movie in movies]
        
        return selected_movies


    def get_movie_detail(self, movie_id):
        uri = f"{self.base_url}movie/{movie_id}"

        self.response = requests.get(
            url=uri,
            headers=self.headers
        )
        self.response.raise_for_status()

        result = self.response.json()

        return result
    
