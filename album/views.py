from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm


# ============ RBAC Helper Mixin ============
class IsOwnerOrAdminMixin(UserPassesTestMixin):
    """
    Mixin to check if user is the owner of the object or an admin
    """
    def test_func(self):
        obj = self.get_object()
        user = self.user
        is_admin = hasattr(user, 'profile') and user.profile.role == 'admin'
        return obj.owner == user or is_admin


# ============ ALBUM VIEWS ============
class AlbumListView(ListView):
    """Display all public albums and user's private albums"""
    model = Album
    template_name = 'album/album_list.html'
    context_object_name = 'albums'
    paginate_by = 12
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            # Show user's albums and public albums
            return Album.objects.filter(
                Q(is_public=True) | Q(owner=self.request.user)
            ).select_related('owner')
        else:
            # Show only public albums for anonymous users
            return Album.objects.filter(is_public=True).select_related('owner')


class AlbumDetailView(DetailView):
    """Display album details with photos"""
    model = Album
    template_name = 'album/album_detail.html'
    context_object_name = 'album'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Album.objects.filter(
                Q(is_public=True) | Q(owner=self.request.user)
            )
        else:
            return Album.objects.filter(is_public=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = (
            self.request.user.is_authenticated and
            (self.object.owner == self.request.user or
             (hasattr(self.request.user, 'profile') and 
              self.request.user.profile.role == 'admin'))
        )
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    """Create a new album"""
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'
    success_url = reverse_lazy('album-list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Album created successfully!')
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, IsOwnerOrAdminMixin, UpdateView):
    """Update an existing album"""
    model = Album
    form_class = AlbumForm
    template_name = 'album/album_form.html'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    
    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Album updated successfully!')
        return super().form_valid(form)


class AlbumDeleteView(LoginRequiredMixin, IsOwnerOrAdminMixin, DeleteView):
    """Delete an album"""
    model = Album
    template_name = 'album/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Album deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============ PHOTO VIEWS ============
class PhotoCreateView(LoginRequiredMixin, CreateView):
    """Upload a photo to an album"""
    model = Photo
    form_class = PhotoForm
    template_name = 'album/photo_form.html'
    
    def get_album(self):
        return get_object_or_404(Album, pk=self.kwargs['album_pk'])
    
    def dispatch(self, request, *args, **kwargs):
        album = self.get_album()
        # Check if user is owner or admin
        is_admin = hasattr(request.user, 'profile') and request.user.profile.role == 'admin'
        if album.owner != request.user and not is_admin:
            messages.error(request, 'You do not have permission to add photos to this album.')
            return redirect('album-detail', pk=album.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.album = self.get_album()
        messages.success(self.request, 'Photo uploaded successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.kwargs['album_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.get_album()
        return context


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    """Update photo metadata"""
    model = Photo
    form_class = PhotoForm
    template_name = 'album/photo_form.html'
    slug_field = 'pk'
    slug_url_kwarg = 'photo_pk'
    
    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        # Check if user is album owner or admin
        is_admin = hasattr(request.user, 'profile') and request.user.profile.role == 'admin'
        if photo.album.owner != request.user and not is_admin:
            messages.error(request, 'You do not have permission to edit this photo.')
            return redirect('album-detail', pk=photo.album.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Photo updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album'] = self.object.album
        return context


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a photo"""
    model = Photo
    template_name = 'album/photo_confirm_delete.html'
    slug_field = 'pk'
    slug_url_kwarg = 'photo_pk'
    
    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        # Check if user is album owner or admin
        is_admin = hasattr(request.user, 'profile') and request.user.profile.role == 'admin'
        if photo.album.owner != request.user and not is_admin:
            messages.error(request, 'You do not have permission to delete this photo.')
            return redirect('album-detail', pk=photo.album.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Photo deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('album-detail', kwargs={'pk': self.object.album.pk})


# ============ DASHBOARD / USER ALBUMS ============
class UserAlbumsView(LoginRequiredMixin, ListView):
    """Display current user's albums"""
    model = Album
    template_name = 'album/user_albums.html'
    context_object_name = 'albums'
    paginate_by = 12
    
    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user).select_related('owner')
