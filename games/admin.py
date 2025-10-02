from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Game, Character, Location, Favorite, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


class CharacterInline(admin.TabularInline):
    model = Character
    extra = 1


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'genre', 'ambiance', 'is_public', 'created_at', 'views_count')
    list_filter = ('genre', 'ambiance', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'keywords')
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    inlines = [CharacterInline, LocationInline]
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'creator', 'is_public')
        }),
        ('Paramètres de génération', {
            'fields': ('genre', 'ambiance', 'keywords', 'cultural_references')
        }),
        ('Contenu généré', {
            'fields': ('universe_description', 'main_story', 'gameplay_mechanics')
        }),
        ('Images conceptuelles', {
            'fields': ('concept_art_character', 'concept_art_environment')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'role', 'character_class')
    list_filter = ('role', 'game__genre')
    search_fields = ('name', 'game__title', 'character_class')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'game')
    search_fields = ('name', 'game__title', 'description')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'created_at')
    list_filter = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_usage_count', 'daily_api_limit', 'last_api_reset')
    list_filter = ('last_api_reset',)
    search_fields = ('user__username', 'user__email')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
