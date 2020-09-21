from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin

admin.register(Recipe)
admin.register(Feedback)
admin.register(Icon)
admin.site.register(Recipe)
admin.site.register(Feedback)
admin.site.register(Icon)

class HookerAdmin(UserAdmin):
    add_form = HookerCreationForm
    form = HookerChangeForm
    model = Hooker
    list_display = ['email', 'username']
    # list_editable = ['Tabaccos']

class TasteAdmin(admin.ModelAdmin):
    list_display = ['Taste']
    admin_order_field = 'Taste'

class TabaccoAdmin(admin.ModelAdmin):
    list_display = ['brand_name']
    admin_order_field = 'brand_name'

admin.site.register(Hooker, HookerAdmin)
admin.site.register(Taste, TasteAdmin)
admin.site.register(Tabacco, TabaccoAdmin)