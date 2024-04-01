from django.contrib import admin
from .models import Author

# Зарегистрируйте свои модели в админ панели здесь
admin.site.register(Author)