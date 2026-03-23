from django.urls import path
from . import views

app_name = 'about_us'

urlpatterns = [
    path("our_story", views.our_story, name="our_story"),
    path("career", views.career, name="career"),
    path("press", views.press, name="press"),
]
