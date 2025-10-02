from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Game(models.Model):
    GENRE_CHOICES = [
        ('RPG', 'RPG'),
        ('FPS', 'FPS'),
        ('METROIDVANIA', 'Metroidvania'),
        ('VISUAL_NOVEL', 'Visual Novel'),
        ('PLATFORMER', 'Platformer'),
        ('STRATEGY', 'Strategy'),
        ('PUZZLE', 'Puzzle'),
        ('ADVENTURE', 'Adventure'),
        ('SIMULATION', 'Simulation'),
        ('RACING', 'Racing'),
    ]
    
    AMBIANCE_CHOICES = [
        ('POST_APOCALYPTIC', 'Post-apocalyptique'),
        ('DREAMLIKE', 'Onirique'),
        ('CYBERPUNK', 'Cyberpunk'),
        ('DARK_FANTASY', 'Dark Fantasy'),
        ('MEDIEVAL', 'Médiéval'),
        ('SCI_FI', 'Science-Fiction'),
        ('HORROR', 'Horreur'),
        ('STEAMPUNK', 'Steampunk'),
        ('MODERN', 'Moderne'),
        ('FANTASY', 'Fantasy'),
    ]
    
    # Informations de base
    title = models.CharField(max_length=200, verbose_name="Titre du jeu")
    description = models.TextField(verbose_name="Description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Paramètres de génération
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=20, choices=AMBIANCE_CHOICES)
    keywords = models.TextField(help_text="Mots-clés séparés par des virgules")
    cultural_references = models.TextField(blank=True, help_text="Références culturelles (optionnel)")
    
    # Contenu généré par IA
    universe_description = models.TextField(blank=True, verbose_name="Description de l'univers")
    main_story = models.TextField(blank=True, verbose_name="Histoire principale")
    gameplay_mechanics = models.TextField(blank=True, verbose_name="Mécaniques de jeu")
    
    # Images générées
    concept_art_character = models.ImageField(upload_to='concept_art/characters/', blank=True, null=True)
    concept_art_environment = models.ImageField(upload_to='concept_art/environments/', blank=True, null=True)
    
    # Paramètres de visibilité
    is_public = models.BooleanField(default=True, verbose_name="Jeu public")
    
    # Statistiques
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Jeu"
        verbose_name_plural = "Jeux"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})
    
    def get_keywords_list(self):
        return [keyword.strip() for keyword in self.keywords.split(',') if keyword.strip()]


class Character(models.Model):
    ROLE_CHOICES = [
        ('PROTAGONIST', 'Protagoniste'),
        ('ANTAGONIST', 'Antagoniste'),
        ('ALLY', 'Allié'),
        ('MENTOR', 'Mentor'),
        ('NEUTRAL', 'Neutre'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100, verbose_name="Nom")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    character_class = models.CharField(max_length=50, verbose_name="Classe/Type")
    background = models.TextField(verbose_name="Histoire personnelle")
    abilities = models.TextField(verbose_name="Capacités et compétences")
    motivations = models.TextField(verbose_name="Motivations")
    appearance = models.TextField(verbose_name="Apparence physique")
    
    class Meta:
        verbose_name = "Personnage"
        verbose_name_plural = "Personnages"
    
    def __str__(self):
        return f"{self.name} ({self.game.title})"


class Location(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100, verbose_name="Nom du lieu")
    description = models.TextField(verbose_name="Description détaillée")
    atmosphere = models.TextField(verbose_name="Ambiance et atmosphère")
    gameplay_significance = models.TextField(verbose_name="Importance dans le gameplay")
    
    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"
    
    def __str__(self):
        return f"{self.name} ({self.game.title})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'game')
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biographie")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    api_usage_count = models.PositiveIntegerField(default=0, verbose_name="Utilisation API")
    daily_api_limit = models.PositiveIntegerField(default=10, verbose_name="Limite API quotidienne")
    last_api_reset = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def can_use_api(self):
        """Vérifie si l'utilisateur peut utiliser l'API aujourd'hui"""
        today = timezone.now().date()
        if self.last_api_reset < today:
            self.api_usage_count = 0
            self.last_api_reset = today
            self.save()
        return self.api_usage_count < self.daily_api_limit
    
    def increment_api_usage(self):
        """Incrémente le compteur d'utilisation de l'API"""
        self.api_usage_count += 1
        self.save()
