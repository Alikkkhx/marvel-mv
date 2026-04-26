from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from movies.views import home, dashboard
from users.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Auth
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API
    path('api/', include('api.urls')),
]
