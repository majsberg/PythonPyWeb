from django.contrib import admin
from .models import Author, AuthorProfile, Entry, Tag


# Зарегистрируйте свои модели в админ панели здесь
admin.site.register(Author)
admin.site.register(AuthorProfile)
admin.site.register(Entry)
admin.site.register(Tag)