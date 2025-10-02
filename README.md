# 🎮 GameForge - Générateur de jeux vidéo par IA

Une plateforme web complète développée avec Django permettant aux utilisateurs de créer des concepts de jeux vidéo originaux à l'aide de l'intelligence artificielle.

![GameForge Logo](https://img.shields.io/badge/GameForge-IA%20Gaming-purple?style=for-the-badge&logo=gamepad)

## 🌟 Fonctionnalités principales

### 🎯 Génération de jeux par IA
- **Univers cohérent** : Génération automatique d'un monde avec son lore et ses règles
- **Histoire immersive** : Scénario structuré en 3 actes avec retournements narratifs
- **Personnages riches** : Galerie de personnages avec rôles, capacités et motivations
- **Lieux emblématiques** : Création d'environnements détaillés avec leur atmosphère
- **Mécaniques de gameplay** : Suggestions de mécaniques adaptées au genre choisi

### 🎨 Interface utilisateur moderne
- **Design responsive** : Compatible mobile, tablette et desktop
- **Interface intuitive** : Navigation fluide avec animations CSS
- **Thème sombre** : Design moderne avec dégradés et effets visuels
- **Accessibilité** : Interface optimisée pour tous les utilisateurs

### 🔐 Système d'authentification complet
- **Inscription/Connexion** : Système sécurisé avec validation
- **Profils utilisateur** : Personnalisation avec avatar et biographie
- **Gestion des sessions** : Authentification persistante
- **Réinitialisation de mot de passe** : Système de récupération par email

### 📊 Dashboard personnel
- **Mes jeux** : Gestion complète des créations personnelles
- **Favoris** : Système de mise en favoris des jeux appréciés
- **Statistiques** : Suivi de l'utilisation API et des performances
- **Paramètres** : Configuration du profil et des préférences

## 🛠️ Technologies utilisées

### Backend
- **Django 4.2.7** : Framework web Python
- **SQLite** : Base de données (développement)
- **Python 3.x** : Langage de programmation

### Frontend
- **Bootstrap 5.3** : Framework CSS responsive
- **Font Awesome 6.4** : Icônes vectorielles
- **Google Fonts** : Typographies (Orbitron, Roboto)
- **JavaScript ES6** : Interactions dynamiques

### IA et APIs
- **Simulation IA** : Générateur de contenu basé sur des templates
- **Hugging Face** : Prêt pour l'intégration d'APIs IA réelles
- **Système modulaire** : Architecture extensible pour futures intégrations

### Outils de développement
- **Django Crispy Forms** : Rendu avancé des formulaires
- **Pillow** : Traitement d'images
- **Python Decouple** : Gestion des variables d'environnement

## 🚀 Installation et configuration

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd TPgroupejeuV1
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Appliquer les migrations**
```bash
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python create_superuser.py
```

7. **Créer des données de démonstration**
```bash
python create_demo_data.py
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000`

## 👥 Comptes de test

### Administrateur
- **Utilisateur** : `admin`
- **Mot de passe** : `admin123`

### Utilisateurs de démonstration
- **alice_dev** / `test123`
- **bob_creator** / `test123`
- **charlie_gamer** / `test123`

## 📱 Utilisation

### 1. Création d'un compte
- Accédez à la page d'inscription
- Remplissez le formulaire avec vos informations
- Confirmez votre inscription

### 2. Génération d'un jeu
- Connectez-vous à votre compte
- Cliquez sur "Créer un jeu"
- Choisissez le genre et l'ambiance
- Ajoutez des mots-clés inspirants
- Laissez l'IA générer votre univers !

### 3. Gestion de vos créations
- Accédez à votre dashboard
- Visualisez tous vos jeux créés
- Modifiez les paramètres de visibilité
- Partagez vos créations avec la communauté

### 4. Découverte communautaire
- Explorez les créations des autres utilisateurs
- Utilisez les filtres de recherche
- Ajoutez vos jeux préférés en favoris
- Découvrez de nouveaux genres et ambiances

## 🎮 Genres et ambiances disponibles

### Genres de jeux
- **RPG** : Jeux de rôle épiques
- **FPS** : Tir à la première personne
- **Metroidvania** : Exploration interconnectée
- **Visual Novel** : Narration interactive
- **Platformer** : Jeux de plateforme
- **Strategy** : Stratégie et tactique
- **Puzzle** : Réflexion et énigmes
- **Adventure** : Aventure et exploration
- **Simulation** : Simulation réaliste
- **Racing** : Course et vitesse

### Ambiances
- **Post-apocalyptique** : Monde dévasté
- **Onirique** : Frontières du rêve
- **Cyberpunk** : Futur technologique sombre
- **Dark Fantasy** : Fantaisie sombre
- **Médiéval** : Époque médiévale
- **Science-Fiction** : Futur lointain
- **Horreur** : Terreur et suspense
- **Steampunk** : Rétro-futurisme à vapeur
- **Moderne** : Époque contemporaine
- **Fantasy** : Monde magique

## 🔧 Architecture du projet

```
gameforge/
├── gameforge/              # Configuration Django
│   ├── settings.py         # Paramètres de l'application
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
├── games/                  # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues et logique métier
│   ├── forms.py           # Formulaires Django
│   ├── admin.py           # Interface d'administration
│   ├── ai_service.py      # Service de génération IA
│   └── signals.py         # Signaux Django
├── templates/              # Templates HTML
│   ├── base.html          # Template de base
│   ├── games/             # Templates des jeux
│   └── registration/      # Templates d'authentification
├── static/                 # Fichiers statiques
├── media/                  # Fichiers uploadés
└── requirements.txt        # Dépendances Python
```

## 🎨 Fonctionnalités avancées

### Système de favoris
- Ajout/suppression en AJAX
- Interface réactive
- Compteurs en temps réel

### Recherche et filtrage
- Recherche textuelle avancée
- Filtres par genre et ambiance
- Tri par popularité, date, titre

### Limitation d'usage API
- Quota quotidien par utilisateur
- Système anti-spam
- Réinitialisation automatique

### Gestion des médias
- Upload d'avatars utilisateur
- Images conceptuelles (prévu)
- Optimisation automatique

## 🔮 Évolutions futures

### Intégration IA réelle
- [ ] API Hugging Face pour génération de texte
- [ ] Stable Diffusion pour images conceptuelles
- [ ] GPT pour dialogues et quêtes
- [ ] DALL-E pour art conceptuel

### Fonctionnalités communautaires
- [ ] Système de commentaires
- [ ] Notation des jeux
- [ ] Partage sur réseaux sociaux
- [ ] Collaboration entre créateurs

### Export et partage
- [ ] Export PDF stylisé
- [ ] Game Design Document complet
- [ ] API publique pour développeurs
- [ ] Intégration avec moteurs de jeu

### Améliorations techniques
- [ ] Cache Redis pour performances
- [ ] Base de données PostgreSQL
- [ ] Déploiement Docker
- [ ] Tests automatisés

## 🤝 Contribution

Ce projet est développé dans le cadre d'un TP Django. Les contributions sont les bienvenues !

### Comment contribuer
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est développé à des fins éducatives dans le cadre d'un TP Django.

## 👨‍💻 Auteur

Développé avec ❤️ pour le cours de Django

---

**GameForge** - Où l'imagination rencontre l'intelligence artificielle ! 🎮✨
