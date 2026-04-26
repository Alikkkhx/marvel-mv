from django.urls import path
from .views import MovieListView, ToggleWatchView, ProgressView, RecommendationsView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='api-movies'),
    path('toggle-watch/', ToggleWatchView.as_view(), name='api-toggle-watch'),
    path('progress/', ProgressView.as_view(), name='api-progress'),
    path('recommendations/', RecommendationsView.as_view(), name='api-recommendations'),
]
