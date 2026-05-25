from django.urls import path
from . import views

app_name = 'album'

urlpatterns = [
    # Album URLs
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('album/create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/update/', views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('my-albums/', views.UserAlbumsView.as_view(), name='user-albums'),
    
    # Photo URLs
    path('album/<int:album_pk>/photo/upload/', views.PhotoCreateView.as_view(), name='photo-upload'),
    path('photo/<int:photo_pk>/edit/', views.PhotoUpdateView.as_view(), name='photo-edit'),
    path('photo/<int:photo_pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
]
