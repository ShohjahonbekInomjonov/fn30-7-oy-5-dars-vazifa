from django.urls import path
from .views import (HomeView, MovieByGenreView, MovieDetailView, SaveCommentView, SaveMovieView, UpdateGenreView, DeleteGenreView,
                    UpdateMovieView, DeleteMovieView, ProfileView)

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('genre/<int:genre_id>/', MovieByGenreView.as_view(), name="movie_by_genre"),
    path('movie/add/', SaveMovieView.as_view(), name="add_movie"),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name="movie_detail"),
    path('movie/<int:pk>/update/', UpdateMovieView.as_view(), name="update_movie"),
    path('movie/<int:pk>/delete/', DeleteMovieView.as_view(), name="delete_movie"),
    path('movie/comment/add/<int:movie_id>/', SaveCommentView.as_view(), name="add_comment"),
    path('profile/<str:username>/', ProfileView.as_view(), name="profile"),
    path('genre/<int:pk>/update/', UpdateGenreView.as_view(), name="update_genre"),
    path('genre/<int:pk>/delete/', DeleteGenreView.as_view(), name="delete_genre")
]
