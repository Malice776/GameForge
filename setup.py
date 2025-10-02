#!/usr/bin/env python
"""
Script de configuration et de gestion pour GameForge
"""
import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Terminé")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de {description}: {e}")
        if e.stdout:
            print(f"Sortie: {e.stdout}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False

def setup_project():
    """Configuration initiale du projet"""
    print("🎮 Configuration de GameForge")
    print("=" * 50)
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou supérieur requis")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} détecté")
    
    # Installer les dépendances
    if not run_command("pip install -r requirements.txt", "Installation des dépendances"):
        return False
    
    # Appliquer les migrations
    if not run_command("python manage.py migrate", "Application des migrations"):
        return False
    
    # Créer les répertoires nécessaires
    directories = ['static', 'media', 'templates']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Répertoires créés")
    
    print("\n🎉 Configuration terminée avec succès !")
    print("\nÉtapes suivantes :")
    print("1. Créer un superutilisateur : python manage.py createsuperuser")
    print("2. Lancer le serveur : python manage.py runserver")
    print("3. Accéder à l'application : http://127.0.0.1:8000")
    
    return True

def create_demo_data():
    """Crée des données de démonstration"""
    print("🎲 Création des données de démonstration")
    print("=" * 50)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameforge.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    from games.models import Game, Character, Location
    from games.ai_service import AIGameGenerator
    
    # Créer des utilisateurs de test
    users_data = [
        {'username': 'alice_dev', 'first_name': 'Alice', 'last_name': 'Developer', 'email': 'alice@gameforge.com'},
        {'username': 'bob_creator', 'first_name': 'Bob', 'last_name': 'Creator', 'email': 'bob@gameforge.com'},
        {'username': 'charlie_gamer', 'first_name': 'Charlie', 'last_name': 'Gamer', 'email': 'charlie@gameforge.com'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            print(f"✅ Utilisateur créé : {user.username}")
        else:
            print(f"ℹ️  Utilisateur existant : {user.username}")
        users.append(user)
    
    # Créer des jeux de démonstration
    games_data = [
        {
            'title': 'Neon Rebellion',
            'genre': 'FPS',
            'ambiance': 'CYBERPUNK',
            'keywords': 'IA rebelle, résistance, mégalopole, hacking',
            'cultural_references': 'Cyberpunk 2077, Ghost in the Shell',
            'creator': users[0]
        },
        {
            'title': 'Les Chroniques d\'Aetheria',
            'genre': 'RPG',
            'ambiance': 'FANTASY',
            'keywords': 'magie ancienne, prophétie, dragons, quête épique',
            'cultural_references': 'The Elder Scrolls, Dragon Age',
            'creator': users[1]
        },
        {
            'title': 'Echoes of Tomorrow',
            'genre': 'METROIDVANIA',
            'ambiance': 'SCI_FI',
            'keywords': 'voyage temporel, station spatiale, mystère',
            'cultural_references': 'Metroid, Hollow Knight',
            'creator': users[2]
        },
        {
            'title': 'Shadowmere Academy',
            'genre': 'VISUAL_NOVEL',
            'ambiance': 'DARK_FANTASY',
            'keywords': 'école de magie, secrets sombres, amitié',
            'cultural_references': 'Harry Potter, Persona',
            'creator': users[0]
        },
        {
            'title': 'Wasteland Survivor',
            'genre': 'ADVENTURE',
            'ambiance': 'POST_APOCALYPTIC',
            'keywords': 'survie, communauté, espoir, reconstruction',
            'cultural_references': 'Fallout, The Last of Us',
            'creator': users[1]
        }
    ]
    
    generator = AIGameGenerator()
    
    for game_data in games_data:
        if Game.objects.filter(title=game_data['title']).exists():
            print(f"ℹ️  Jeu existant : {game_data['title']}")
            continue
            
        generated_content = generator.generate_game(
            genre=game_data['genre'],
            ambiance=game_data['ambiance'],
            keywords=game_data['keywords'],
            cultural_references=game_data['cultural_references']
        )
        
        generated_content['title'] = game_data['title']
        generated_content['creator'] = game_data['creator']
        
        game = Game.objects.create(**generated_content)
        generator.create_characters_for_game(game)
        generator.create_locations_for_game(game)
        
        print(f"✅ Jeu créé : {game.title}")
    
    print(f"\n🎉 Données de démonstration créées !")
    print(f"📊 Statistiques :")
    print(f"   - Jeux : {Game.objects.count()}")
    print(f"   - Personnages : {Character.objects.count()}")
    print(f"   - Lieux : {Location.objects.count()}")
    print(f"\n👥 Comptes de test :")
    for user in users:
        print(f"   - {user.username} / test123")

def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        print("🎮 GameForge - Script de gestion")
        print("=" * 40)
        print("Usage:")
        print("  python setup.py setup     - Configuration initiale")
        print("  python setup.py demo      - Créer des données de démo")
        print("  python setup.py help      - Afficher cette aide")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'setup':
        setup_project()
    elif command == 'demo':
        create_demo_data()
    elif command == 'help':
        main()
    else:
        print(f"❌ Commande inconnue : {command}")
        main()

if __name__ == '__main__':
    main()
