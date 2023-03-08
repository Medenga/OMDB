import requests
from django.http import HttpResponse
from django.http import JsonResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Remplacez "votre_api_key" par votre propre clé d'API OMDB
API_KEY = "bf76dbe3"
def get_common_actors(title):
    api_key = 'votre_clé_d_api_omdb'
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}&plot=full"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        star_wars_actors = []
        if "Star Wars" in data['Title']:
            for actor in data['Actors'].split(','):
                star_wars_actors.append(actor.strip())
        return star_wars_actors
    else:
        return []
    
def get_pirates(request):
    parametres = {
        "apikey": API_KEY,
        "s": "Pirates of the Caribbean",
    }
    url = f"http://www.omdbapi.com/"
    response = requests.get(url, params = parametres)
    if response.status_code == 200:
        data = response.json()
        movies = []
        for movie in data['Search']:
            movie_details = {}
            movie_details['Titre'] = movie['Title']
            movie_details['Année'] = movie['Year']
            movie_details['Image'] = movie['Poster']
            #Je ne peux pas rajouter l'auteur car je n'ai pas accès au Director
            #movie_details['Le film a été produit avant 2015'] = True if int(movie['Year']) < 2015 else False
            #movie_details['Paul Walker est un des acteurs du film'] = 'Paul Walker' in movie['Actors']
            #common_actors = get_common_actors(movie['Title'])
            #movie_details['common_actors'] = common_actors
            movies.append(movie_details)
        # Store movies in a Google Spreadsheet
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('projet/credentials.json', scope)
        client = gspread.authorize(credentials)
        spreadsheet = client.open("omdb")
        worksheet = spreadsheet.add_worksheet(title='Les Pirates des Caraïbes', rows=len(movies), cols=3)
        worksheet.insert_row(['Titre', 'Année', 'Image'], index=1)
        row_num = 2
        for movie in movies:
            worksheet.update_cell(row_num, 1, movie['Titre'])
            worksheet.update_cell(row_num, 2, movie['Année'])
            worksheet.update_cell(row_num, 3, movie['Image'])
            row_num += 1

        return JsonResponse({'movies': movies})
    else:
        return JsonResponse({'movies': []})



def index(request):
    return HttpResponse("Bonjour, monde !")

def listing(request):
    print('entrer le type de film souhaiter')
    nn = input()
    parametres = {
        "apikey": API_KEY,
        "s": nn,
    }
    url = f"http://www.omdbapi.com/"
    response = requests.get(url, params = parametres)
    if response.status_code == 200:
        data = response.json()
        movies = []
        if data['Error'] == 'Movie not found!':
            return JsonResponse({'movies': "le mot entré est n'est pas correcte"}) 
        print(data)
        for movie in data['Search']:
            movie_details = {}
            movie_details['title'] = movie['Title']
            movie_details['year'] = movie['Year']
            movie_details['poster'] = movie['Poster']
            movies.append(movie_details)
        return JsonResponse({'movies': movies})
    else:
        return JsonResponse({'movies': []})
    #return render(request, 'portfolio/portfolio.html', context)

def get_fast_and_furious_movies(request):
    parametres = {
        "apikey": API_KEY,
        "s": "Fast & Furious",
    }
    url = f"http://www.omdbapi.com/"
    response = requests.get(url, params = parametres)
    if response.status_code == 200:
        data = response.json()
        movies = []
        for movie in data['Search']:
            movie_details = {}
            movie_details['title'] = movie['Title']
            movie_details['year'] = movie['Year']
            movie_details['poster'] = movie['Poster']
            movies.append(movie_details)
        return JsonResponse({'movies': movies})
    else:
        return JsonResponse({'movies': []})
    
