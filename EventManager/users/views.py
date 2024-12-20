from urllib import request
from django.shortcuts import redirect, render
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, logout

from .forms import SignUpForm

from .serializers import UserSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        serializer.save()
    def signup(request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                (request, user)  
                return redirect('login')  
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
        })
    
    

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token_deleted = Token.objects.filter(user=request.user).delete()
        if token_deleted:
            logout(request)
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'No active session found.'}, status=status.HTTP_400_BAD_REQUEST)
