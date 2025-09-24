from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

# Create your models here.


class Genre(models.Model):
    type = models.CharField(max_length=255, verbose_name="Janri", unique=True)

    def __str__(self) -> str:
        return self.type
    
    class Meta:
        verbose_name = "Janr"
        verbose_name_plural = "Janrlar"
        ordering = ['type']
        permissions = [
            ("films.change_genre", "Can change genre"),
            ("films.delete_genre", "Can delete genre"),
        ]


class Movie(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    director = models.CharField(max_length=255, verbose_name="Rejissori")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsifi")
    image = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name="Rasmi")
    video = models.FileField(upload_to="videos/", null=True, blank=True, verbose_name="Videosi", 
                             validators=[FileExtensionValidator(["mp4", "mov", "avi", "mkv"])])
    views = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    year = models.IntegerField(verbose_name="Yili", 
                               validators=[MinValueValidator(1990, message="1990-yildan katta yilni kiriting"), MaxValueValidator(2025, message="2025 yildan kichik yilni kiriting")])
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Janri")

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Kino"
        verbose_name_plural = "Kinolar"
        ordering = ['name']


class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name="Matni")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Kino")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['-created']

    def __str__(self) -> str:
        return self.text
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="user/images/", null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"
        ordering = ['job']