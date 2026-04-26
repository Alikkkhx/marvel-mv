from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from movies.models import Movie, Phase
from services.services import MovieService, StatsService, RecommendationService

def home(request):
    phase_id = request.GET.get('phase')
    status_filter = request.GET.get('status')
    sort_by = request.GET.get('sort', 'year_asc')
    
    movies = MovieService.get_filtered_movies(
        user=request.user,
        phase_id=phase_id,
        status=status_filter,
        sort_by=sort_by
    )
    
    phases = Phase.objects.all()
    
    context = {
        'movies': movies,
        'phases': phases,
        'current_phase': phase_id,
        'current_status': status_filter,
        'current_sort': sort_by,
    }
    return render(request, 'movies/home.html', context)

@login_required
def dashboard(request):
    stats = StatsService.get_user_stats(request.user)
    recommendation_items = RecommendationService.get_recommendation_items(request.user)
    
    context = {
        'stats': stats,
        'recommendation_items': recommendation_items,
    }
    return render(request, 'movies/dashboard.html', context)
