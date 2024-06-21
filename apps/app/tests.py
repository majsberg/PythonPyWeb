from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.db_train_alternative.models import Author
from .serializers import AuthorModelSerializer

# Create your tests here.
