from rest_framework import serializers
from movies.models import Movie, Phase, WatchedStatus

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['id', 'name', 'order']

class MovieSerializer(serializers.ModelSerializer):
    phase_name = serializers.CharField(source='phase.name', read_only=True)
    is_watched = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'title_ru', 'year', 'release_date', 'director',
            'phase', 'phase_name', 'poster_url', 
            'description_en', 'description_ru', 'rating', 'is_watched'
        ]

    def get_is_watched(self, obj):
        user = self.context.get('request').user
        if user and user.is_authenticated:
            return WatchedStatus.objects.filter(user=user, movie=obj, is_watched=True).exists()
        return False
