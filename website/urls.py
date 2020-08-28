from django.contrib import admin
from django.urls import path, include
from website.views import HookahIndex

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HookahIndex.as_view()),
    path('add', HookahIndex.as_view(template='add')),
    path('stat', HookahIndex.as_view(template='statistic')),
    path('test', HookahIndex.as_view(template='login')),
    path('accounts/', include('django.contrib.auth.urls')),
]
