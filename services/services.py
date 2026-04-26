from django.db.models import BooleanField, Exists, OuterRef, Value
from django.shortcuts import get_object_or_404

from movies.models import Movie, WatchedStatus, Phase


class MovieService:
    @staticmethod
    def get_filtered_movies(user=None, phase_id=None, status=None, sort_by=None):
        movies = Movie.objects.select_related("phase").all()

        if phase_id:
            movies = movies.filter(phase_id=phase_id)

        if user and user.is_authenticated:
            watched_row = WatchedStatus.objects.filter(
                user=user, movie_id=OuterRef("pk"), is_watched=True
            )
            movies = movies.annotate(is_watched=Exists(watched_row))
        else:
            movies = movies.annotate(is_watched=Value(False, output_field=BooleanField()))

        if user and user.is_authenticated:
            if status == "watched":
                movies = movies.filter(is_watched=True)
            elif status == "unwatched":
                movies = movies.filter(is_watched=False)

        sort_by = sort_by or "year_asc"
        if sort_by == "year_asc":
            movies = movies.order_by("release_date", "title")
        elif sort_by == "year_desc":
            movies = movies.order_by("-release_date", "title")
        elif sort_by == "title_az":
            movies = movies.order_by("title", "release_date")
        elif sort_by == "title_za":
            movies = movies.order_by("-title", "release_date")
        else:
            movies = movies.order_by("release_date", "title")

        return movies


class WatchService:
    @staticmethod
    def toggle_watched(user, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        status_obj, _ = WatchedStatus.objects.get_or_create(
            user=user, movie=movie, defaults={"is_watched": False}
        )
        status_obj.is_watched = not status_obj.is_watched
        status_obj.save(update_fields=["is_watched"])
        return movie, status_obj.is_watched


class StatsService:
    @staticmethod
    def get_user_stats(user):
        if not user.is_authenticated:
            return None

        total_movies = Movie.objects.count()
        watched_count = WatchedStatus.objects.filter(user=user, is_watched=True).count()
        remaining_count = total_movies - watched_count
        progress_pct = (watched_count / total_movies * 100) if total_movies > 0 else 0

        phases = Phase.objects.all()
        phase_stats = []
        for phase in phases:
            phase_total = phase.movies.count()
            phase_watched = WatchedStatus.objects.filter(
                user=user, movie__phase=phase, is_watched=True
            ).count()
            phase_stats.append(
                {
                    "name": phase.name,
                    "total": phase_total,
                    "watched": phase_watched,
                    "pct": (phase_watched / phase_total * 100) if phase_total > 0 else 0,
                }
            )

        return {
            "total_watched": watched_count,
            "total_remaining": remaining_count,
            "progress_pct": round(progress_pct, 1),
            "phase_stats": phase_stats,
        }


class RecommendationService:
    @staticmethod
    def get_recommendation_items(user, limit=3):
        if not user.is_authenticated:
            q = Movie.objects.select_related("phase").order_by("release_date", "year")
            return [
                {
                    "movie": m,
                    "reason": "Sign in to sync your list; showing next releases by order.",
                }
                for m in q[:limit]
            ]

        watched_ids = WatchedStatus.objects.filter(
            user=user, is_watched=True
        ).values_list("movie_id", flat=True)
        unwatched = (
            Movie.objects.select_related("phase")
            .exclude(id__in=watched_ids)
            .order_by("release_date", "year")
        )
        recs = list(unwatched[:limit])
        items = []
        for m in recs:
            year = m.release_date.year if m.release_date else m.year
            items.append(
                {
                    "movie": m,
                    "reason": f"Next in MCU release order ({year}) — {m.phase.name} timeline.",
                }
            )
        return items

    @staticmethod
    def get_recommendations(user, limit=3):
        return [i["movie"] for i in RecommendationService.get_recommendation_items(user, limit=limit)]
