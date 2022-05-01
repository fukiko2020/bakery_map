from django.contrib import admin
from .models import CustomUser, Bakery, Review, Favorite

admin.site.register(CustomUser)
admin.site.register(Bakery)
admin.site.register(Review)
admin.site.register(Favorite)
