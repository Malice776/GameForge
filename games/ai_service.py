import requests
import random
import json
from django.conf import settings
from .models import Game, Character, Location


class AIGameGenerator:
    """Service pour générer du contenu de jeu avec l'IA"""
    
    def __init__(self):
        # Pour l'instant, nous utiliserons des données simulées
        # Plus tard, vous pourrez intégrer Hugging Face API
        self.api_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
        
    def generate_game(self, genre, ambiance, keywords, cultural_references=""):
        """Génère un jeu complet basé sur les paramètres donnés"""
        
        # Simulation de génération IA (remplacez par l'API Hugging Face)
        game_data = self._simulate_ai_generation(genre, ambiance, keywords, cultural_references)
        
        return game_data
    
    def generate_random_game(self):
        """Génère un jeu complètement aléatoire"""
        genre = random.choice([choice[0] for choice in Game.GENRE_CHOICES])
        ambiance = random.choice([choice[0] for choice in Game.AMBIANCE_CHOICES])
        
        random_keywords = [
            "mystère", "aventure", "magie", "technologie", "exploration",
            "combat", "puzzle", "survie", "amitié", "trahison",
            "découverte", "ancien", "futur", "robot", "dragon"
        ]
        keywords = ", ".join(random.sample(random_keywords, random.randint(3, 6)))
        
        return self.generate_game(genre, ambiance, keywords)
    
    def _simulate_ai_generation(self, genre, ambiance, keywords, cultural_references):
        """Simule la génération IA avec des templates prédéfinis"""
        
        # Templates de base selon le genre et l'ambiance
        templates = self._get_game_templates()
        
        # Sélectionner un template approprié
        template_key = f"{genre}_{ambiance}"
        if template_key not in templates:
            template_key = "default"
        
        template = templates.get(template_key, templates["default"])
        
        # Personnaliser avec les mots-clés
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        # Générer le contenu
        title = self._generate_title(genre, ambiance, keywords_list)
        description = self._generate_description(template, keywords_list)
        universe_description = self._generate_universe(template, ambiance, keywords_list)
        main_story = self._generate_story(template, keywords_list)
        gameplay_mechanics = self._generate_gameplay(genre, template)
        
        game_data = {
            'title': title,
            'description': description,
            'genre': genre,
            'ambiance': ambiance,
            'keywords': keywords,
            'cultural_references': cultural_references,
            'universe_description': universe_description,
            'main_story': main_story,
            'gameplay_mechanics': gameplay_mechanics,
        }
        
        return game_data
    
    def _get_game_templates(self):
        """Retourne les templates de jeux prédéfinis"""
        return {
            "RPG_FANTASY": {
                "title_prefix": ["Légendes de", "Chroniques de", "L'Épopée de"],
                "title_suffix": ["Aetheria", "Valdris", "Mystralion"],
                "universe": "Un monde fantastique où la magie et la technologie coexistent",
                "story_base": "Un héros improbable doit sauver le royaume",
                "gameplay": "Combat au tour par tour, système de classes, quêtes épiques"
            },
            "FPS_CYBERPUNK": {
                "title_prefix": ["Neon", "Cyber", "Neural"],
                "title_suffix": ["Strike", "Protocol", "Nexus"],
                "universe": "Une mégalopole cyberpunk où les corporations règnent",
                "story_base": "Un hacker rebelle découvre un complot",
                "gameplay": "Tir à la première personne, amélioration cybernétique, infiltration"
            },
            "METROIDVANIA_DARK_FANTASY": {
                "title_prefix": ["Ombres de", "Malédiction de", "Secrets de"],
                "title_suffix": ["Ravencroft", "Shadowmere", "Grimhaven"],
                "universe": "Un château gothique aux secrets sombres",
                "story_base": "Un explorateur découvre les mystères d'un lieu maudit",
                "gameplay": "Exploration interconnectée, capacités déblocables, boss épiques"
            },
            "default": {
                "title_prefix": ["Aventures de", "Mystères de", "Quête de"],
                "title_suffix": ["l'Inconnu", "Destiny", "Infinity"],
                "universe": "Un monde unique aux règles particulières",
                "story_base": "Une aventure extraordinaire commence",
                "gameplay": "Mécaniques innovantes adaptées au genre"
            }
        }
    
    def _generate_title(self, genre, ambiance, keywords):
        """Génère un titre de jeu"""
        templates = self._get_game_templates()
        template_key = f"{genre}_{ambiance}"
        template = templates.get(template_key, templates["default"])
        
        prefix = random.choice(template["title_prefix"])
        suffix = random.choice(template["title_suffix"])
        
        # Parfois utiliser un mot-clé dans le titre
        if keywords and random.random() > 0.5:
            keyword = random.choice(keywords).title()
            return f"{prefix} {keyword}"
        
        return f"{prefix} {suffix}"
    
    def _generate_description(self, template, keywords):
        """Génère une description du jeu"""
        base_desc = template["story_base"]
        
        if keywords:
            keyword_context = f" impliquant {', '.join(keywords[:3])}"
            return base_desc + keyword_context + "."
        
        return base_desc + "."
    
    def _generate_universe(self, template, ambiance, keywords):
        """Génère la description de l'univers"""
        universe_base = template["universe"]
        
        ambiance_descriptions = {
            'POST_APOCALYPTIC': "dans un monde post-apocalyptique dévasté",
            'DREAMLIKE': "aux frontières entre rêve et réalité",
            'CYBERPUNK': "dominé par la haute technologie et la corruption",
            'DARK_FANTASY': "où la magie sombre règne en maître",
            'MEDIEVAL': "dans un cadre médiéval authentique",
            'SCI_FI': "dans un futur lointain parmi les étoiles",
            'HORROR': "hanté par des terreurs indicibles",
            'STEAMPUNK': "propulsé par la vapeur et l'ingéniosité",
            'MODERN': "ancré dans notre époque contemporaine",
            'FANTASY': "peuplé de créatures magiques et de merveilles"
        }
        
        ambiance_desc = ambiance_descriptions.get(ambiance, "aux caractéristiques uniques")
        
        detailed_universe = f"{universe_base} {ambiance_desc}. "
        
        if keywords:
            detailed_universe += f"Les thèmes centraux incluent {', '.join(keywords[:4])}, "
            detailed_universe += "créant une expérience narrative riche et immersive."
        
        return detailed_universe
    
    def _generate_story(self, template, keywords):
        """Génère l'histoire principale en 3 actes"""
        story_base = template["story_base"]
        
        act1 = f"**Acte I - L'Appel à l'Aventure**\n{story_base}. "
        if keywords:
            act1 += f"Les premiers indices concernant {keywords[0] if keywords else 'le mystère'} apparaissent."
        
        act2 = f"\n\n**Acte II - Le Développement**\nLes défis s'intensifient et les véritables enjeux se révèlent. "
        if len(keywords) > 1:
            act2 += f"L'importance de {keywords[1]} devient cruciale pour la suite des événements."
        
        act3 = f"\n\n**Acte III - La Résolution**\nLe climax épique où tous les éléments convergent. "
        if len(keywords) > 2:
            act3 += f"Le rôle de {keywords[2]} dans le dénouement surprend et satisfait."
        
        return act1 + act2 + act3
    
    def _generate_gameplay(self, genre, template):
        """Génère les mécaniques de gameplay"""
        base_gameplay = template["gameplay"]
        
        genre_mechanics = {
            'RPG': "Système de progression de personnage, inventaire détaillé, dialogues à embranchements",
            'FPS': "Visée précise, arsenal varié, multijoueur compétitif",
            'METROIDVANIA': "Carte interconnectée, progression par capacités, secrets cachés",
            'VISUAL_NOVEL': "Choix narratifs impactants, multiples fins, développement de relations",
            'PLATFORMER': "Contrôles précis, niveaux créatifs, collectibles secrets",
            'STRATEGY': "Gestion de ressources, planification tactique, diplomatie",
            'PUZZLE': "Énigmes progressives, mécaniques innovantes, satisfaction intellectuelle",
            'ADVENTURE': "Exploration libre, résolution d'énigmes, narration immersive",
            'SIMULATION': "Systèmes complexes, gestion détaillée, réalisme",
            'RACING': "Physique de conduite, personnalisation de véhicules, circuits variés"
        }
        
        specific_mechanics = genre_mechanics.get(genre, "Mécaniques adaptées au genre")
        
        return f"{base_gameplay}. {specific_mechanics}."
    
    def create_characters_for_game(self, game):
        """Crée des personnages pour un jeu donné"""
        characters_data = self._generate_characters(game.genre, game.ambiance, game.get_keywords_list())
        
        characters = []
        for char_data in characters_data:
            character = Character.objects.create(
                game=game,
                **char_data
            )
            characters.append(character)
        
        return characters
    
    def create_locations_for_game(self, game):
        """Crée des lieux pour un jeu donné"""
        locations_data = self._generate_locations(game.genre, game.ambiance, game.get_keywords_list())
        
        locations = []
        for loc_data in locations_data:
            location = Location.objects.create(
                game=game,
                **loc_data
            )
            locations.append(location)
        
        return locations
    
    def _generate_characters(self, genre, ambiance, keywords):
        """Génère des données de personnages"""
        # Templates de personnages selon le genre
        character_templates = {
            'RPG': [
                {'role': 'PROTAGONIST', 'class_base': 'Guerrier', 'archetype': 'héros reluctant'},
                {'role': 'ALLY', 'class_base': 'Mage', 'archetype': 'mentor sage'},
                {'role': 'ANTAGONIST', 'class_base': 'Sorcier', 'archetype': 'tyran corrompu'},
            ],
            'FPS': [
                {'role': 'PROTAGONIST', 'class_base': 'Soldat', 'archetype': 'vétéran endurci'},
                {'role': 'ALLY', 'class_base': 'Hacker', 'archetype': 'génie rebelle'},
                {'role': 'ANTAGONIST', 'class_base': 'Agent', 'archetype': 'corporation impitoyable'},
            ]
        }
        
        templates = character_templates.get(genre, character_templates['RPG'])
        characters = []
        
        for i, template in enumerate(templates[:3]):  # Maximum 3 personnages
            name = self._generate_character_name(template['archetype'])
            character = {
                'name': name,
                'role': template['role'],
                'character_class': template['class_base'],
                'background': f"Histoire de {name}, un {template['archetype']} aux motivations complexes.",
                'abilities': f"Maîtrise de {template['class_base'].lower()}, compétences spécialisées.",
                'motivations': f"Motivé par {keywords[i] if i < len(keywords) else 'la justice'}.",
                'appearance': f"Apparence distinctive d'un {template['class_base'].lower()} expérimenté."
            }
            characters.append(character)
        
        return characters
    
    def _generate_locations(self, genre, ambiance, keywords):
        """Génère des données de lieux"""
        location_templates = {
            'FANTASY': ['Forêt Enchantée', 'Château Ancien', 'Cavernes Mystiques'],
            'CYBERPUNK': ['Mégalopole Néon', 'Sous-sols Technologiques', 'Tours Corporatives'],
            'POST_APOCALYPTIC': ['Ruines Urbaines', 'Bunker Abandonné', 'Désert Radioactif']
        }
        
        templates = location_templates.get(ambiance, location_templates['FANTASY'])
        locations = []
        
        for i, template in enumerate(templates[:3]):  # Maximum 3 lieux
            location = {
                'name': template,
                'description': f"Un lieu emblématique : {template.lower()}. Description détaillée de l'environnement.",
                'atmosphere': f"Atmosphère {ambiance.lower()} caractéristique, immersion totale.",
                'gameplay_significance': f"Zone clé pour {keywords[i] if i < len(keywords) else 'la progression'}."
            }
            locations.append(location)
        
        return locations
    
    def _generate_character_name(self, archetype):
        """Génère un nom de personnage"""
        names = {
            'héros': ['Aiden', 'Lyra', 'Kael', 'Zara'],
            'mentor': ['Eldric', 'Morgana', 'Theron', 'Seraphina'],
            'tyran': ['Malachar', 'Vex', 'Grimwald', 'Nyx'],
            'default': ['Alex', 'Jordan', 'Casey', 'Riley']
        }
        
        name_list = names.get(archetype.split()[0], names['default'])
        return random.choice(name_list)
