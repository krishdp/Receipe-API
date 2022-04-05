from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from drf_spectacular.utils import extend_schema

from .models import Recipe, Ingredient, Upvote
from .serializers import RecipeSerializer, IngredientSerializer, UpvoteSerializer, RecipeDetailserializer, UserRegistrationSerializer


class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]


class IngredientCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CreateUpvoteView(generics.ListCreateAPIView):
    serializer_class = UpvoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        return Upvote.objects.filter(user=user, recipe=recipe)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("You've already voted on this.")
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, recipe=recipe)


class RecipeDetailsView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailserializer
    permission_classes = [permissions.AllowAny]


class RecipeUpdateView(generics.RetrieveDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(author=self.request.user, pk=kwargs['pk'])
        if recipe.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("Hry There..!! This is'ny your recipe..")


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {
                'token': token
            }
        else:
            data = serializer.errors
        return Response(data=data, status=201)


class LoginView(generics.CreateAPIView):
    serializer_class = AuthTokenSerializer
    
    def create(self, request):
        return ObtainAuthToken().as_view()(request=request._request)
