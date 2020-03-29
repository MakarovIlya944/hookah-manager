from django.contrib import admin
from website.website.models import Tabacco, Recipe

admin.register(Tabacco)
admin.register(Recipe)
admin.site.register(Tabacco)
admin.site.register(Recipe)