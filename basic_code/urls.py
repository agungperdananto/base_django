from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pattern_data/', include('pattern_data.urls'), name='pattern_data'),
    path('account/', include('account.urls'), name='account'),
]
