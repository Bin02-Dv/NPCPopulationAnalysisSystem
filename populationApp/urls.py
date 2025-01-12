from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('upload/', views.upload, name="upload"),
    path('api/population-data/', views.get_population_data, name="upload"),
    path('clear_data/', views.clear_data, name="clear"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('search/', views.search_population, name='search_population')
]
