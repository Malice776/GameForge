from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game, UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requis. Entrez une adresse email valide.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Requis.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Requis.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Bootstrap aux champs
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['password1', 'password2']:
                field.widget.attrs['class'] += ' form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class GameCreationForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['genre', 'ambiance', 'keywords', 'cultural_references']
        widgets = {
            'keywords': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: boucle temporelle, vengeance, IA rebelle...'}),
            'cultural_references': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ex: Zelda, Hollow Knight, Disco Elysium... (optionnel)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Bootstrap aux champs
        for field_name, field in self.fields.items():
            if field_name in ['genre', 'ambiance']:
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'


class GameUpdateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Bootstrap aux champs
        for field_name, field in self.fields.items():
            if field_name != 'is_public':
                field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Parlez-nous de vous...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Bootstrap aux champs
        for field_name, field in self.fields.items():
            if field_name == 'bio':
                field.widget.attrs['class'] = 'form-control'
            elif field_name == 'avatar':
                field.widget.attrs['class'] = 'form-control'


class GameSearchForm(forms.Form):
    SEARCH_CHOICES = [
        ('title', 'Titre'),
        ('genre', 'Genre'),
        ('ambiance', 'Ambiance'),
        ('creator', 'Créateur'),
    ]
    
    ORDER_CHOICES = [
        ('-created_at', 'Plus récent'),
        ('created_at', 'Plus ancien'),
        ('title', 'Titre A-Z'),
        ('-title', 'Titre Z-A'),
        ('-views_count', 'Plus populaire'),
    ]

    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Rechercher un jeu...', 'class': 'form-control'})
    )
    search_in = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    genre = forms.ChoiceField(
        choices=[('', 'Tous les genres')] + Game.GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ambiance = forms.ChoiceField(
        choices=[('', 'Toutes les ambiances')] + Game.AMBIANCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    order_by = forms.ChoiceField(
        choices=ORDER_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS Bootstrap aux champs
        for field_name, field in self.fields.items():
            if 'select' in field.widget.__class__.__name__.lower():
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
