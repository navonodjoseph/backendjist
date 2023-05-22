from django.urls import path
from .views import AudioUploadView

app_name = 'whisper'

urlpatterns = [
    path('', AudioUploadView.as_view(), name='AudioUploadView')
]