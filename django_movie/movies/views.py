from rest_framework import generics
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor
from .serializers import (
    ActorListSerializer, CreateRatingSerializer, 
    MovieListSerializer, MovieDetailSerializer, 
    ReviewCreateSerializer,
    ActorDetailSerializer
    )
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                "ratings", filter=models.Q(ratings__ip=get_client_ip(self.request))
            )
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
        return movies

class MovieDetailView(generics.RetrieveAPIView):
    """"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer

class ReviewCreateView(generics.CreateAPIView):

    serializer_class = ReviewCreateSerializer

        
class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer
    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
            

class ActorListView(generics.ListAPIView):
    """list actors"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailView(generics.RetrieveAPIView):
    """list actors"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
