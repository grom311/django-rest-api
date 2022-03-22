from dataclasses import fields
from multiprocessing import context
from rest_framework import serializers

from .models import Movie, Rating, Review

class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.Serializer):
    """View recursion children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
    
class MovieListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ('id','title', 'tagline', 'category', 'rating_user', 'middle_star')

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """View review"""
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')

class MovieDetailSerializer(serializers.ModelSerializer):
    """Detail movie"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft', )


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie',)

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating

    