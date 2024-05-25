from django.urls import path
from. import views

app_name ='piece_api'

urlpatterns = [
    path('pieces/', views.PieceListCreateAPIView.as_view(), name='piece-list-create-api'),
    path('pieces/suggestions/', views.PieceRandomListAPIView.as_view(), name='piece-random-list-api'),
    path('pieces/<slug:slug>/', views.PieceRetrieveUpdateDestroyAPIView.as_view(), name='piece-retrieve-update-destroy-api'),
]