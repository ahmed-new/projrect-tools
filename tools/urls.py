
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('tools/movie', views.get_movie, name='movie'),
    path('tools/currency', views.currency , name='currency'),
    path('tools/games', views.games , name='games'),
    path('tools/generate-image', views.generate_image, name='generate_image'),
    path('tools/news/english', views.news_list , name='news_en'),
    path('tools/news/arabic', views.news_list_ar , name='news_ar'),
]

