from django.db import models

class Phase(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    year = models.IntegerField()
    phase = models.ForeignKey(Phase, related_name='movies', on_delete=models.CASCADE)
    poster_url = models.URLField(max_length=500)
    description_en = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    chronological_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['release_date', 'title']

    def __str__(self):
        return f"{self.title} ({self.year})"

class WatchedStatus(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='watched_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchers')
    is_watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({'Watched' if self.is_watched else 'Not Watched'})"
