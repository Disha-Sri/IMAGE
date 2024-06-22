from django.urls import path
from .views import ImageMetadataView

urlpatterns = [
    path('metadata/', ImageMetadataView.as_view(), name='image-metadata'),

]