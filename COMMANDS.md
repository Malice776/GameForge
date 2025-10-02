# 🎮 GameForge - Commandes utiles

## 🚀 Démarrage rapide

### Configuration initiale
```bash
# Cloner le projet
git clone <url-du-repo>
cd TPgroupejeuV1

# Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Configuration automatique
python setup.py setup
```

### Lancement du serveur
```bash
python manage.py runserver
```

## 🛠️ Commandes de développement

### Gestion de la base de données
```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Réinitialiser la base de données
python manage.py flush

# Créer un superutilisateur
python manage.py createsuperuser
```

### Gestion des données
```bash
# Créer des données de démonstration
python setup.py demo

# Collecter les fichiers statiques
python manage.py collectstatic

# Vider le cache (si configuré)
python manage.py clear_cache
```

### Tests et vérifications
```bash
# Vérifier la configuration
python manage.py check

# Lancer les tests
python manage.py test

# Vérifier la syntaxe des templates
python manage.py validate_templates
```

## 🔧 Commandes d'administration

### Shell Django
```bash
# Ouvrir le shell Django
python manage.py shell

# Exemples d'utilisation dans le shell
from games.models import Game, User
from games.ai_service import AIGameGenerator

# Lister tous les jeux
Game.objects.all()

# Créer un jeu de test
generator = AIGameGenerator()
user = User.objects.first()
game_data = generator.generate_game('RPG', 'FANTASY', 'magie, aventure', '')
```

### Gestion des utilisateurs
```bash
# Changer le mot de passe d'un utilisateur
python manage.py changepassword <username>

# Créer un utilisateur en ligne de commande
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.create_user('testuser', 'test@example.com', 'password123')
"
```

### Sauvegarde et restauration
```bash
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json

# Exporter seulement l'app games
python manage.py dumpdata games > games_backup.json
```

## 📊 Commandes de monitoring

### Statistiques
```bash
# Compter les objets
python manage.py shell -c "
from games.models import Game, Character, Location, User
print(f'Jeux: {Game.objects.count()}')
print(f'Personnages: {Character.objects.count()}')
print(f'Lieux: {Location.objects.count()}')
print(f'Utilisateurs: {User.objects.count()}')
"
```

### Nettoyage
```bash
# Supprimer les sessions expirées
python manage.py clearsessions

# Nettoyer les fichiers orphelins
python manage.py cleanup_unused_media
```

## 🐛 Débogage

### Logs et debug
```bash
# Lancer avec debug verbeux
python manage.py runserver --verbosity=2

# Afficher les requêtes SQL
python manage.py shell -c "
from django.conf import settings
settings.LOGGING['loggers']['django.db.backends'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
}
"
```

### Résolution de problèmes courants
```bash
# Problème de migrations
python manage.py migrate --fake-initial

# Recréer les migrations
rm games/migrations/0*.py
python manage.py makemigrations games
python manage.py migrate

# Problème de permissions
python manage.py collectstatic --clear
```

## 🔄 Workflow de développement

### Avant de commencer
```bash
# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Vérifier les mises à jour
pip list --outdated

# Lancer les tests
python manage.py test
```

### Après modifications
```bash
# Vérifier la configuration
python manage.py check

# Créer les migrations si nécessaire
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Tester l'application
python manage.py runserver
```

## 📦 Déploiement

### Préparation
```bash
# Installer les dépendances de production
pip install gunicorn psycopg2-binary

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Vérifier la configuration de production
python manage.py check --deploy
```

### Variables d'environnement
```bash
# Créer un fichier .env
echo "DEBUG=False" > .env
echo "SECRET_KEY=your-secret-key" >> .env
echo "DATABASE_URL=your-database-url" >> .env
```

## 🎯 Commandes personnalisées

### Créer une commande personnalisée
```python
# games/management/commands/generate_sample_games.py
from django.core.management.base import BaseCommand
from games.ai_service import AIGameGenerator

class Command(BaseCommand):
    help = 'Génère des jeux d\'exemple'
    
    def handle(self, *args, **options):
        generator = AIGameGenerator()
        # Logique de génération
        self.stdout.write('Jeux générés avec succès!')
```

### Utilisation
```bash
python manage.py generate_sample_games
```

## 🔍 Inspection et analyse

### Modèles et structure
```bash
# Afficher la structure des modèles
python manage.py inspectdb

# Visualiser les relations
python manage.py graph_models games -o models.png

# Analyser les performances
python manage.py shell -c "
from django.db import connection
print(connection.queries)
"
```

---

💡 **Astuce** : Créez des alias pour les commandes fréquentes dans votre shell !

```bash
# Exemple d'aliases
alias dj="python manage.py"
alias djrun="python manage.py runserver"
alias djmig="python manage.py migrate"
alias djmake="python manage.py makemigrations"
```
