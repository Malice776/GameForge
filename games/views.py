from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from .models import Game, Character, Location, Favorite, UserProfile
from .forms import CustomUserCreationForm, GameCreationForm, GameUpdateForm, UserProfileForm, GameSearchForm
from .ai_service import AIGameGenerator


class HomeView(ListView):
    model = Game
    template_name = 'games/home.html'
    context_object_name = 'recent_games'
    paginate_by = 6

    def get_queryset(self):
        return Game.objects.filter(is_public=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_games'] = Game.objects.filter(is_public=True).count()
        context['total_users'] = UserProfile.objects.count()
        return context


class GameListView(ListView):
    model = Game
    template_name = 'games/game_list.html'
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        queryset = Game.objects.filter(is_public=True)
        form = GameSearchForm(self.request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_in = form.cleaned_data.get('search_in')
            genre = form.cleaned_data.get('genre')
            ambiance = form.cleaned_data.get('ambiance')
            order_by = form.cleaned_data.get('order_by')

            if query:
                if search_in == 'title':
                    queryset = queryset.filter(title__icontains=query)
                elif search_in == 'genre':
                    queryset = queryset.filter(genre__icontains=query)
                elif search_in == 'ambiance':
                    queryset = queryset.filter(ambiance__icontains=query)
                elif search_in == 'creator':
                    queryset = queryset.filter(creator__username__icontains=query)
                else:
                    queryset = queryset.filter(
                        Q(title__icontains=query) |
                        Q(description__icontains=query) |
                        Q(keywords__icontains=query)
                    )

            if genre:
                queryset = queryset.filter(genre=genre)
            
            if ambiance:
                queryset = queryset.filter(ambiance=ambiance)
            
            if order_by:
                queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = GameSearchForm(self.request.GET)
        return context


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'

    def get_object(self):
        game = get_object_or_404(Game, pk=self.kwargs['pk'])
        
        # Vérifier si le jeu est public ou si l'utilisateur est le créateur
        if not game.is_public and (not self.request.user.is_authenticated or game.creator != self.request.user):
            raise Http404("Ce jeu n'est pas accessible.")
        
        # Incrémenter le compteur de vues
        game.views_count += 1
        game.save(update_fields=['views_count'])
        
        return game

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user,
                game=self.object
            ).exists()
        return context


@login_required
def dashboard_view(request):
    user_games = Game.objects.filter(creator=request.user).order_by('-created_at')
    favorites = Favorite.objects.filter(user=request.user).select_related('game').order_by('-created_at')
    
    context = {
        'user_games': user_games,
        'favorites': favorites,
        'can_create_game': request.user.profile.can_use_api(),
        'api_usage': request.user.profile.api_usage_count,
        'api_limit': request.user.profile.daily_api_limit,
    }
    return render(request, 'games/dashboard.html', context)


@login_required
def create_game_view(request):
    if not request.user.profile.can_use_api():
        messages.error(request, "Vous avez atteint votre limite quotidienne de génération de jeux.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            # Vérifier à nouveau la limite API
            if not request.user.profile.can_use_api():
                messages.error(request, "Vous avez atteint votre limite quotidienne de génération de jeux.")
                return redirect('dashboard')

            try:
                # Générer le jeu avec l'IA
                generator = AIGameGenerator()
                
                if 'random' in request.POST:
                    # Génération aléatoire
                    game_data = generator.generate_random_game()
                else:
                    # Génération basée sur les paramètres du formulaire
                    game_data = generator.generate_game(
                        genre=form.cleaned_data['genre'],
                        ambiance=form.cleaned_data['ambiance'],
                        keywords=form.cleaned_data['keywords'],
                        cultural_references=form.cleaned_data['cultural_references']
                    )

                # Créer le jeu
                game = Game.objects.create(
                    creator=request.user,
                    **game_data
                )
                
                generator.create_characters_for_game(game)
                generator.create_locations_for_game(game)
                generator.create_concept_art_for_game(game)

                # Incrémenter l'utilisation de l'API
                request.user.profile.increment_api_usage()

                messages.success(request, f"Le jeu '{game.title}' a été généré avec succès !")
                return redirect('game_detail', pk=game.pk)

            except Exception as e:
                messages.error(request, f"Erreur lors de la génération : {str(e)}")
                return render(request, 'games/create_game.html', {'form': form})
    else:
        form = GameCreationForm()

    # S'assurer que le token CSRF est disponible
    csrf_token = get_token(request)
    return render(request, 'games/create_game.html', {'form': form, 'csrf_token': csrf_token})


@login_required
def toggle_favorite_view(request, pk):
    if request.method == 'POST':
        game = get_object_or_404(Game, pk=pk)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            game=game
        )
        
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_favorited': is_favorited,
                'favorites_count': game.favorited_by.count()
            })
        
        return redirect('game_detail', pk=pk)
    
    return redirect('game_detail', pk=pk)


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('game').order_by('-created_at')
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'games/favorites.html', {'page_obj': page_obj})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé avec succès.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    # S'assurer que le token CSRF est disponible
    csrf_token = get_token(request)
    return render(request, 'registration/signup.html', {'form': form, 'csrf_token': csrf_token})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'games/profile.html', {'form': form})


@login_required
def edit_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        form = GameUpdateForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, "Le jeu a été mis à jour avec succès.")
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameUpdateForm(instance=game)
    
    return render(request, 'games/edit_game.html', {'form': form, 'game': game})


@login_required
def delete_game_view(request, pk):
    game = get_object_or_404(Game, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        game.delete()
        messages.success(request, "Le jeu a été supprimé avec succès.")
        return redirect('dashboard')
    
    return render(request, 'games/delete_game.html', {'game': game})
