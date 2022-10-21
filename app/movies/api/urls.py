from django.urls import path, include

app_name = 'movies'
urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]
