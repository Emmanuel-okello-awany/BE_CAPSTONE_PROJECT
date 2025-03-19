from django.urls import path
from .views import register_view, login_view, logout_view, RegisterAPI, LoginAPI, home_view, profile_view, browse
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # 🌐 Web URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('browse/', browse, name='browse'),

    # 📌 API URLs
    path('api/register/', RegisterAPI.as_view(), name='api-register'),
    path('api/login/', LoginAPI.as_view(), name='api-login'),
    path('api/token-auth/', obtain_auth_token, name='token-auth'),
    
]
