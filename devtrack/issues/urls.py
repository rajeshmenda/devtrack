from django.urls import path
from .views import issues, reporters

urlpatterns = [
    path('api/issues/', issues),
    path('api/reporters/', reporters),
]