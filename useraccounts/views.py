from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import render, redirect
from .forms import RegistrationForm 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model




def auth_page(request):
    User = get_user_model()

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('auth_page')

        # Create a new user
        user = User.objects.create_user(
            email=email, password=password,
            first_name=first_name, last_name=last_name,
            company_name=company_name, phone_number=phone_number,
            country=country, state=state, city=city
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'useraccounts/register.html')

# def auth_page(request):
#     User = get_user_model()

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists")
#             return redirect('auth_page')

#         user = User.objects.create_user(
#             email=email, password=password,
#             first_name=first_name, last_name=last_name
#         )
#         messages.success(request, "Registration successful! Please log in.")
#         return redirect('login')

#     return render(request, 'useraccounts/register.html')


# def auth_page(request):
#     User = get_user_model()  # Use the custom user model

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')

#         # Check if the user with the given email already exists
#         if User.objects.filter(email=email).exists():
#             return render(request, 'useraccounts/register.html', {'error': 'Email already exists'})

#         # Create a new user
#         user = User.objects.create_user(
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.save()

#         return redirect('login')  # Redirect to login page after successful registration

#     return render(request, 'useraccounts/register.html')
# def auth_page(request):
#     User = get_user_model()  # Use the custom user model
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Check if the user already exists
#         if User.objects.filter(username=username).exists():
#             return render(request, 'useraccounts/register.html', {'error': 'Username already exists'})

#         # Create a new user
#         user = User.objects.create_user(username=username, password=password)
#         user.save()

#         return redirect('login')  # Redirect to login page after registration

#     return render(request, 'useraccounts/register.html')

# def auth_page(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         # Validate that passwords match
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'useraccounts/register.html')

#         # Check if user already exists
#         User = get_user_model() 
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return render(request, 'useraccounts/register.html')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email is already in use.")
#             return render(request, 'useraccounts/register.html')

#         # Create new user
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()

#         # Authenticate and login the user (optional)
#         login(request, user)

#         # Redirect to a different page (e.g., login)
#         messages.success(request, "Registration successful! You are now logged in.")
#         return redirect('login')

#     return render(request, 'useraccounts/register.html')


# def auth_page(request):
#     if request.method == 'POST':
#         # Handle form submission here if needed
#         return redirect('login')  # Redirect to login page after registration (optional)
#     return render(request, 'useraccounts/register.html')

# def auth_page(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to login page after successful registration
#     else:
#         form = RegistrationForm()
#     return render(request, 'useraccounts/register.html', {'form': form})

# def auth_page(request):
#     form = RegistrationForm()
#     return render(request, 'useraccounts/register.html', {'form': form})

# def auth_page(request):
#     return render(request, 'useraccounts/auth.html')

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    'message': 'User registered successfully',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        return data
    
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = RefreshToken.for_user(user)

            return Response({
                            'message': 'Login successful',
                            'access': str(token.access_token),
                            'refresh': str(token)
                        }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
           
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
