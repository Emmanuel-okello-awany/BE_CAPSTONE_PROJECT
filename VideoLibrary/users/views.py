from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm
from .serializers import UserSerializer


def home_view(request):
    return render(request, 'home.html')  # home.html is placed in the global templates folder


# 🌐 Web Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# 🌐 Web Login View
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to a dashboard/home page
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

# 🌐 Web Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# User Profile (Protected View)
@login_required
def profile_view(request):
    return render(request, 'users/profile.html')  # Renders profile page

def browse(request):
    return render(request, 'browse.html')

# 📌 API: User Registration
class RegisterAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# 📌 API: Login & Get Token
class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid credentials"}, status=400)
