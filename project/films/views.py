from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from typing import Any

from .models import Genre, Movie, Comment, Profile
from .forms import CommentForm, MovieForm
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin



# Create your views here.
class HomeView(ListView):
    template_name = "film/index.html"
    context_object_name = "movies"
    extra_context = {
        "title": "Barcha Kinolar"
    }
    ordering = ['-year']
    
    def get_queryset(self):
        return Movie.objects.all()
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["genres"] = Genre.objects.all()
        return context
    


def home(request: HttpRequest):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    context = {
        "movies": movies,
        "genres": genres,
        "title": "Barcha Kinolar"
    }
    return render(request, "film/index.html", context)


class MovieByGenreView(HomeView):
    def get_queryset(self):
        queryset = Movie.objects.filter(genre_id=self.kwargs.get('genre_id'))
        return queryset
    


def movie_by_genre(request: HttpRequest, genre_id: int):
    movies = Movie.objects.filter(genre_id=genre_id)
    genres = Genre.objects.all()

    context = {
        "movies": movies,
        "genres": genres,
        "title": get_object_or_404(Genre, pk=genre_id).type
    }
    return render(request, "film/index.html", context)


class MovieDetailView(DetailView):
    model = Movie
    template_name = "film/movie_detail.html"
    extra_context = {
        "genres": Genre.objects.all(),
        "form": CommentForm()
    }

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        movie = get_object_or_404(Movie, pk=self.kwargs.get("pk"))
        movie.views += 1
        movie.save()
        context["title"] = movie.name
        context["comments"] = Comment.objects.filter(movie=movie)
        return context
    


@login_required
def movie_detail(request: HttpRequest, pk: int):
    genres = Genre.objects.all()
    movie = get_object_or_404(Movie, pk=pk)
    comments = Comment.objects.filter(movie=movie)

    movie.views += 1
    movie.save()

    context = {
        "movie": movie,
        "genres": genres,
        "title": movie.name,
        "form": CommentForm(),
        "comments": comments
    }
    return render(request, "film/film-detail.html", context)


class SaveCommentView(View):
    def post(self, request: HttpRequest, movie_id: int):
        if request.method == "POST":
            form = CommentForm(data=request.POST)
            if form.is_valid():
                Comment.objects.create(
                    text=request.POST.get("text"),
                    movie_id=movie_id,
                    user=request.user
                )
        return redirect("movie_detail", pk=movie_id)


def save_comment(request: HttpRequest, movie_id: int):
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                text=request.POST.get("text"),
                movie_id=movie_id,
                user=request.user
            )
    return redirect("movie_detail", pk=movie_id)


class SaveMovieView(PermissionRequiredMixin, CreateView):
    model = Movie
    form_class = MovieForm
    template_name = "film/add-film.html"
    # success_url = '/movie/{pk}/'

    def get_success_url(self) -> str:
        return reverse_lazy('movie_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "Yangi Kino Qo'shish"
        return context
    
    def form_valid(self, form):
        movie = form.save(commit=True)
        messages.success(self.request, "Kino muvaffaqiyatli qo'shildi!!!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Ma'lumotlar to'liq yoki noto'g'ri kiritildi!!!")
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('films.add_films'):
            messages.warning(request, "Sizda kino qo'shish uchun ruxsat yo'q!!!")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    


# @permission_required('films.add_films', raise_exception=True)
@permission_required('films.add_films')
def save_movie(request: HttpRequest):
    if request.method == "POST":
        form = MovieForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            movie = form.save()
            messages.success(request, "Kino qo'shildi !!!")
            return redirect("movie_detail", pk=movie.pk)
    else:
        form = MovieForm()
    context = {
        "form": form
    }
    return render(request, "film/add-film.html", context)


class UpdateMovieView(PermissionRequiredMixin, UpdateView):
    model = Movie
    form_class = MovieForm
    permission_required = "films.add_films"
    template_name = "film/add-film.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.has_perm('films.change_films'):
            messages.warning(request, "Sizda kino o'zgartirish uchun ruxsat yo'q!!!")
            return redirect('home')
        messages.success(request, "Kino muvoffaqiyatli o'zgartirildi")
        return super().dispatch(request, *args, **kwargs)
    


@permission_required('films.change_films', raise_exception=True)
def update_movie(request: HttpRequest, pk: int):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        form = MovieForm(data=request.POST, files=request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            messages.success(request, "Kino o'zgartirildi!!!")
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        "form": form
    }
    return render(request, "film/add-film.html", context)


class DeleteMovieView(PermissionRequiredMixin, DeleteView):
    model = Movie
    template_name = "film/confirm-delete.html"
    permission_required = "films.delete_films"
    success_url = reverse_lazy("home")

    def delete(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        messages.success(request, "Kino muvaffaqqiyatli o'chirildi!!!")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        messages.warning(self.request, "Aniq o'chirmoqchimisiz?")
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('films.delete_films'):
            messages.warning(request, "Sizda kinoni o'chirish uchun ruxsat yo'q!!!")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


@permission_required('films.delete_films')
def delete_movie(request: HttpRequest, pk: int):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == "POST":
        movie.delete()
        messages.success(request, "Kino o'chirildi!!!")
        return redirect('home')
    else:
        context = {
            "title": movie.name
        }
        messages.warning(request, "Aniq o'chirmoqchimimsiz?")
        return render(request, "film/confirm-delete.html", context)
    

class ProfileView(View):
    def get(self, request: HttpRequest, username: str):
        user = get_object_or_404(User, username=username)
        context = {
            "user": user,
            "title": str(user.username).title() + " profili"
        }

        try:
            profile = Profile.objects.get(user=user)
            context["profile"] = profile
        except:
            pass
        return render(request, "profile.html", context)


def profile(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    context = {
        "user": user,
        "title": str(user.username).title() + " profili"
    }

    try:
        profile = Profile.objects.get(user=user)
        context["profile"] = profile
    except:
        pass
    return render(request, "profile.html", context)


class UpdateGenreView(PermissionRequiredMixin, UpdateView):
    model = Genre
    fields = ['type']
    permission_required = "films.change_genre"
    template_name = "film/update-genre.html"
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.object.type} janrini yangilash"
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Janr muvoffaqiyatli o'zgartirildi!!!")
        return super().form_valid(form)
    
    def form_invalid(self, form) -> HttpResponse:
        messages.error(self.request, "Ma'lumotlar noto'g'ri kiritildi!!!")
        return super().form_invalid(form)
    

class DeleteGenreView(PermissionRequiredMixin, DeleteView):
    model = Genre
    permission_required = "films.delete_genre"
    template_name = "film/confirm-delete-genre.html"
    success_url = reverse_lazy('home')

    def delete(self, request: HttpRequest, *args: str, **kwargs):
        messages.success(request, "janr muvaffaqiyatli o'chirildi!!!")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.object.type} janrini o'chirish"
        messages.warning(self.request, "Aniq o'chirmoqchimisiz?")
        return context