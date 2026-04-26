from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from .serializers import MovieSerializer
from services.services import MovieService, StatsService, RecommendationService, WatchService


class MovieListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        movie_id = request.query_params.get("id")
        if movie_id:
            movie = get_object_or_404(Movie, id=movie_id)
            serializer = MovieSerializer(movie, context={"request": request})
            return Response(serializer.data)

        phase_id = request.query_params.get("phase")
        status_filter = request.query_params.get("status")
        sort_by = request.query_params.get("sort")

        movies = MovieService.get_filtered_movies(
            user=request.user,
            phase_id=phase_id,
            status=status_filter,
            sort_by=sort_by,
        )
        serializer = MovieSerializer(
            movies, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ToggleWatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        movie_id = request.data.get("movie_id")
        if movie_id in (None, ""):
            return Response(
                {"error": "movie_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            movie_id = int(movie_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid movie_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        movie, is_watched = WatchService.toggle_watched(request.user, movie_id)
        return Response({"movie_id": movie.id, "is_watched": is_watched})


class ProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = StatsService.get_user_stats(request.user)
        return Response(stats)


class RecommendationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = RecommendationService.get_recommendation_items(request.user)
        out = []
        for item in items:
            out.append(
                {
                    "movie": MovieSerializer(
                        item["movie"], context={"request": request}
                    ).data,
                    "reason": item["reason"],
                }
            )
        return Response(out)
