from django.contrib import admin
from .models import Recipe, Ingredient, Upvote

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Upvote)
