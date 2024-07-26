from django.urls import path
from .views import HomepageView

urlpatterns = [
path('homepage/', HomepageView.as_view(), name='homepage'),
]