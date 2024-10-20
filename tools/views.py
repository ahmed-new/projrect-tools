from django.shortcuts import render
import requests
from django.http import JsonResponse

import base64

    

def home(request):
    return render(request,'home.html',{})

def currency(request):
    return render(request,'cureency.html',{})


def get_movie(request):
    url = "https://api.themoviedb.org/3/search/movie"
    API_KEY = 'cd2c1f86e898553bc96f9fc531770353'
    context = {}  # تأكد من تعريف context قبل استخدامه

    if request.method == 'POST':
        query = request.POST.get('searched', None)
        if query:  # تحقق من أن هناك استعلام
            params = {
                'api_key': API_KEY,
                'query': query
            }
            r = requests.get(url, params=params)
            data = r.json()

            # تحقق من أن هناك نتائج
            if data['results']:
                movie = data['results'][0]  # استخدم [0] للوصول إلى أول فيلم

                # جلب مراجعات الفيلم
                movie_id = movie.get('id')  # احصل على معرف الفيلم
                reviews_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
                reviews_response = requests.get(reviews_url, params={'api_key': API_KEY})
                reviews_data = reviews_response.json()
                reviews = reviews_data.get('results', [])  # تأكد من أن هذا ليس دالة

                context = {
                    'original_title': movie.get('original_title', 'N/A'),
                    'release_date': movie.get('release_date', 'N/A'),
                    'overview': movie.get('overview', 'N/A'),
                    'original_language': movie.get('original_language', 'N/A'),
                    'backdrop_path': movie.get('backdrop_path', None),
                    'reviews': reviews  # أضف المراجعات إلى السياق
                }
            else:
                context = {
                    'error': 'No movies found for the given search term.'  # رسالة في حالة عدم وجود أفلام
                }

    return render(request, 'movie.html', {'context': context})





def games(request):
    url = 'https://www.freetogame.com/api/games'
    
    # تحقق مما إذا كان هناك تصنيف محدد في GET parameters
    cat = request.GET.get('category')  # استخدام GET لالتقاط التصنيف
    if cat:
        url += f'?category={cat}'
    
    try:
        respo = requests.get(url)
        respo.raise_for_status()  
        data = respo.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        data = []  # إذا حدث خطأ، يتم تعيين البيانات كقائمة فارغة

    return render(request, 'games.html', {'data': data})



def generate_image(request):
    image = None
    error = None
    
    if request.method == 'POST':
        text = request.POST.get('text')
        
        if not text:
            error = 'يجب إدخال نص.'
            return render(request, 'generate_image.html', {'error': error})

        api_token = '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'  
        url = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1'
        
        try:
            response = requests.post(
                url,
                headers={
                    'Authorization': f'Bearer {api_token}',
                    'Content-Type': 'application/json',
                },
                json={'inputs': text}
            )

            if response.status_code == 200:
                image_data = response.content
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                return render(request, 'generate_image.html', {'image': image_base64})
            elif response.status_code == 503:
                error = 'We Have a problem now ,try again later'
            else:
                error = f'خطأ من واجهة البرمجة: {response.status_code} - {response.text}'

        except requests.RequestException as e:
            error = f'فشل في الاتصال بالواجهة: {str(e)}'

    return render(request, 'generate_image.html', {'error': error})





def news_list(request):
    API_KEY = '0b6272f4173844e8ae6b7af604ff7f4e'
    BASE_URL = 'https://newsapi.org/v2/top-headlines'
   
    query = request.GET.get('query', '')  
    category = request.GET.get('category', '')  
    

  
    params = {
        'apiKey': API_KEY,
        'q': query,
       
    }
    
  
    if category:
        params['category'] = category

   
    response = requests.get(BASE_URL, params=params)

    
    articles = response.json().get('articles', [])

    return render(request, 'news_list.html', {'articles': articles})



def news_list_ar(request):
    API_KEY = '0b6272f4173844e8ae6b7af604ff7f4e'
    BASE_URL = 'https://newsapi.org/v2/everything'
    query = request.GET.get('query', '')

    params = {
        'apiKey': API_KEY,
        'q': query,
        'language': 'ar',
    }

    response = requests.get(BASE_URL, params=params)

    
    articles = response.json().get('articles', [])

    return render(request, 'news_list_ar.html', {'articles': articles})


    
