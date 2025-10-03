import random
from django.conf import settings
from .models import Game, Character, Location
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import re


class AIGameGenerator:
    """Service simplifié avec LangChain"""

    def __init__(self):
        api_key = settings.AI_API_KEY

        if api_key:
            # Utiliser un modèle actif Groq (à adapter selon la console Groq)
            self.llm = ChatGroq(
                api_key=api_key,
                model_name="llama-3.1-8b-instant",  # modèle actuel
                temperature=0.8,
                max_tokens=1500,
            )
        else:
            self.llm = None

    def _generate_with_chain(self, template, variables):
        if not self.llm:
            return None

        try:
            prompt = PromptTemplate(
                input_variables=list(variables.keys()),
                template=template
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = chain.invoke(variables)

            # Extraction du texte si c'est un dict
            if isinstance(result, dict):
                result_text = result.get("text", "")
            else:
                result_text = result

            print("=== Résultat IA ===")
            print(result_text)
            print("==================")

            return result_text.strip()
        except Exception as e:
            print(f"Erreur LangChain: {str(e)}")
            return None


    def generate_game(self, genre, ambiance, keywords, cultural_references=""):
        if self.llm:
            game_data = self._generate_with_ai(genre, ambiance, keywords, cultural_references)
            if game_data:
                return game_data

        return self._generate_with_templates(genre, ambiance, keywords, cultural_references)

    def _generate_with_ai(self, genre, ambiance, keywords, cultural_references):
        template = """Tu es un expert en game design. Crée un concept complet de jeu vidéo.
    Genre: {genre}
    Ambiance: {ambiance}
    Mots-clés: {keywords}
    {cultural_ref}

    Fournis les éléments suivants:

    TITRE:
    DESCRIPTION:
    UNIVERS:
    HISTOIRE:
    MECANIQUES:"""

        cultural_ref = f"Références culturelles: {cultural_references}" if cultural_references else ""
        result = self._generate_with_chain(template, {
            "genre": genre,
            "ambiance": ambiance,
            "keywords": keywords,
            "cultural_ref": cultural_ref
        })

        if not result:
            return None

        # Regex pour capturer les sections, en tolérant ** et les espaces
        pattern = r'\**\s*(TITRE|DESCRIPTION|UNIVERS|HISTOIRE|MECANIQUES)\s*:*\**\s*(.*?)(?=(\**\s*(TITRE|DESCRIPTION|UNIVERS|HISTOIRE|MECANIQUES)\s*:)|\Z)'
        matches = re.findall(pattern, result, flags=re.DOTALL | re.IGNORECASE)

        sections = {}
        for match in matches:
            key = match[0].strip().lower()
            value = match[1].strip()
            sections[key] = value

        # Mapping vers les champs du modèle
        key_map = {
            "titre": "title",
            "description": "description",
            "univers": "universe_description",
            "histoire": "main_story",
            "mecaniques": "gameplay_mechanics"
        }

        parsed_data = {
            model_field: sections.get(section_name, "")
            for section_name, model_field in key_map.items()
        }

        return {
            "title": parsed_data.get("title", f"Jeu {genre}"),
            "description": parsed_data.get("description", ""),
            "genre": genre,
            "ambiance": ambiance,
            "keywords": keywords,
            "cultural_references": cultural_references,
            "universe_description": parsed_data.get("universe_description", ""),
            "main_story": parsed_data.get("main_story", ""),
            "gameplay_mechanics": parsed_data.get("gameplay_mechanics", ""),
        }

    
    def create_characters_for_game(self, game):
        """Crée des personnages"""
        if self.llm:
            characters_data = self._generate_characters_with_ai(game)
        else:
            characters_data = self._generate_characters_template(game)
        
        characters = []
        for char_data in characters_data:
            character = Character.objects.create(game=game, **char_data)
            characters.append(character)
        
        return characters
    
    def _generate_characters_with_ai(self, game):
        """Génère des personnages avec LangChain"""
        
        template = """Crée 3 personnages pour le jeu vidéo "{title}".
Genre: {genre}
Ambiance: {ambiance}

Format JSON strict (retourne uniquement le JSON, rien d'autre):
[
  {{
    "name": "Nom du personnage",
    "role": "PROTAGONIST ou ALLY ou ANTAGONIST",
    "character_class": "Classe",
    "background": "Background en 2 phrases",
    "abilities": "Capacités en 1 phrase",
    "motivations": "Motivations en 1 phrase",
    "appearance": "Apparence en 1 phrase"
  }}
]"""

        result = self._generate_with_chain(template, {
            'title': game.title,
            'genre': game.genre,
            'ambiance': game.ambiance
        })
        
        if result:
            try:
                import json
                # Extraire le JSON du résultat
                start = result.find('[')
                end = result.rfind(']') + 1
                if start != -1 and end > start:
                    json_str = result[start:end]
                    characters = json.loads(json_str)
                    return characters[:3]
            except:
                pass
        
        return self._generate_characters_template(game)
    
    def create_locations_for_game(self, game):
        """Crée des lieux"""
        if self.llm:
            locations_data = self._generate_locations_with_ai(game)
        else:
            locations_data = self._generate_locations_template(game)
        
        locations = []
        for loc_data in locations_data:
            location = Location.objects.create(game=game, **loc_data)
            locations.append(location)
        
        return locations
    
    def _generate_locations_with_ai(self, game):
        """Génère des lieux avec LangChain"""
        
        template = """Crée 3 lieux pour le jeu vidéo "{title}".
Genre: {genre}
Ambiance: {ambiance}

Format JSON strict:
[
  {{
    "name": "Nom du lieu",
    "description": "Description en 2-3 phrases",
    "atmosphere": "Atmosphère en 2 phrases",
    "gameplay_significance": "Importance gameplay en 1-2 phrases"
  }}
]"""

        result = self._generate_with_chain(template, {
            'title': game.title,
            'genre': game.genre,
            'ambiance': game.ambiance
        })
        
        if result:
            try:
                import json
                start = result.find('[')
                end = result.rfind(']') + 1
                if start != -1 and end > start:
                    json_str = result[start:end]
                    locations = json.loads(json_str)
                    return locations[:3]
            except:
                pass
        
        return self._generate_locations_template(game)
    
    # Templates de fallback (gardez vos fonctions existantes)
    def _generate_with_templates(self, genre, ambiance, keywords, cultural_references):
        """Fallback template"""
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        return {
            'title': self._generate_title_template(genre, ambiance, keywords_list),
            'description': f"Une aventure {genre.lower()} dans un univers {ambiance.lower()}",
            'genre': genre,
            'ambiance': ambiance,
            'keywords': keywords,
            'cultural_references': cultural_references,
            'universe_description': f"Un monde {ambiance.lower()} unique",
            'main_story': "Une histoire épique en trois actes",
            'gameplay_mechanics': "Mécaniques innovantes",
        }
    
    def _generate_title_template(self, genre, ambiance, keywords_list=[]):
        """Template de titre"""
        prefixes = {
            'RPG': ['Les Chroniques de', 'L\'Héritage de'],
            'FPS': ['Opération', 'Code'],
            'METROIDVANIA': ['Les Ombres de'],
        }
        suffixes = ['Aetheria', 'Eclipse', 'Grimhaven']
        
        prefix = random.choice(prefixes.get(genre, prefixes['RPG']))
        suffix = random.choice(keywords_list) if keywords_list else random.choice(suffixes)
        
        return f"{prefix} {suffix.title()}"
    
    def _generate_characters_template(self, game):
        """Template personnages"""
        return [
            {
                'name': 'Aiden',
                'role': 'PROTAGONIST',
                'character_class': 'Guerrier',
                'background': "Un héros improbable.",
                'abilities': "Maîtrise du combat.",
                'motivations': "Sauver le monde.",
                'appearance': "Apparence de guerrier."
            }
        ]
    
    def _generate_locations_template(self, game):
        """Template lieux"""
        return [
            {
                'name': 'La Forêt Enchantée',
                'description': "Un lieu mystérieux.",
                'atmosphere': "Atmosphère magique.",
                'gameplay_significance': "Zone clé."
            }
        ]