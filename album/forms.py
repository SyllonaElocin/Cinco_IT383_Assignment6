from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    """Form for creating and updating albums"""
    class Meta:
        model = Album
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Album Name',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)',
                'rows': 3
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class PhotoForm(forms.ModelForm):
    """Form for uploading and updating photos"""
    class Meta:
        model = Photo
        fields = ['image', 'title', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Photo Title (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Photo Description (optional)',
                'rows': 3
            })
        }
