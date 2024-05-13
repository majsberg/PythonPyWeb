from django.urls import path
from .views import AutoREST

urlpatterns = [
    path('authors/', AutoREST.as_view()),
    path('author/<int:id>/', AutoREST.as_view()),
]