from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

admin.register(Tabacco)
admin.register(Recipe)
admin.register(Feedback)
admin.register(Taste)
admin.site.register(Tabacco)
admin.site.register(Recipe)
admin.site.register(Feedback)
admin.site.register(Taste)

class HookerAdmin(UserAdmin):
    add_form = HookerCreationForm
    form = HookerChangeForm
    model = Hooker
    list_display = ['email', 'username','Tabaccos']
    list_editable = ['Tabaccos']

admin.site.register(Hooker, HookerAdmin)