from django.urls import path
from .views import AudioUploadView

app_name = 'jist'

urlpatterns = [
    path('', AudioUploadView.as_view(), name='AudioUploadView')
]