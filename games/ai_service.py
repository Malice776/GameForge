import json
import re
import traceback
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Game, Character, Location
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from io import BytesIO
from PIL import Image
from huggingface_hub import InferenceClient

class AIGameGenerator:
    """Générateur IA simplifié pour GameForge"""

    def __init__(self):
        api_key = settings.AI_API_KEY
        if api_key:
            self.llm = ChatGroq(
                api_key=api_key,
                model_name="llama-3.1-8b-instant",
                temperature=0.8,
                max_tokens=1500,
            )
        else:
            self.llm = None

    # --------------------
    # Méthode utilitaire LangChain
    # --------------------
    def _generate_with_chain(self, template, variables):
        if not self.llm:
            return None
        try:
            prompt = PromptTemplate(input_variables=list(variables.keys()), template=template)
            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = chain.invoke(variables)
            if isinstance(result, dict):
                return result.get("text", "").strip()
            return str(result).strip()
        except Exception as e:
            print(f"[IA ERROR] {e}")
            return None

    # --------------------
    # Génération principale du jeu
    # --------------------
    def generate_game(self, genre, ambiance, keywords, cultural_references=""):
        if self.llm:
            game_data = self._generate_game_with_ai(genre, ambiance, keywords, cultural_references)
            if game_data:
                return game_data
        return self._generate_game_with_templates(genre, ambiance, keywords, cultural_references)

    def _generate_game_with_ai(self, genre, ambiance, keywords, cultural_references):
        template = """
Tu es un expert en game design. Crée un concept complet de jeu vidéo.

Genre: {genre}
Ambiance: {ambiance}
Mots-clés: {keywords}
{cultural_ref}

Fournis les éléments suivants:

TITRE:
DESCRIPTION:
UNIVERS:
HISTOIRE:
MECANIQUES:
"""
        cultural_ref = f"Références culturelles: {cultural_references}" if cultural_references else ""
        result = self._generate_with_chain(template, {
            "genre": genre,
            "ambiance": ambiance,
            "keywords": keywords,
            "cultural_ref": cultural_ref
        })
        if not result:
            return None

        # Regex pour extraire les sections
        pattern = r'\**\s*(TITRE|DESCRIPTION|UNIVERS|HISTOIRE|MECANIQUES)\s*:*\**\s*(.*?)(?=(\**\s*(TITRE|DESCRIPTION|UNIVERS|HISTOIRE|MECANIQUES)\s*:)|\Z)'
        matches = re.findall(pattern, result, flags=re.DOTALL | re.IGNORECASE)
        sections = {match[0].strip().lower(): match[1].strip() for match in matches}

        key_map = {
            "titre": "title",
            "description": "description",
            "univers": "universe_description",
            "histoire": "main_story",
            "mecaniques": "gameplay_mechanics"
        }

        parsed_data = {model_field: sections.get(section_name, "") for section_name, model_field in key_map.items()}

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

    # --------------------
    # Génération de personnages
    # --------------------
    def create_characters_for_game(self, game):
        if self.llm:
            characters_data = self._generate_characters_with_ai(game)
        else:
            characters_data = self._generate_characters_template(game)
        characters = [Character.objects.create(game=game, **c) for c in characters_data]
        return characters

    def _generate_characters_with_ai(self, game):
        template = """
Crée 3 personnages pour le jeu "{title}".
Genre: {genre}
Ambiance: {ambiance}

Format JSON strict:
[
  {{
    "name": "Nom",
    "role": "PROTAGONIST ou ALLY ou ANTAGONIST",
    "character_class": "Classe",
    "background": "Background en 2 phrases",
    "abilities": "Capacités",
    "motivations": "Motivations",
    "appearance": "Apparence"
  }}
]
"""
        result = self._generate_with_chain(template, {
            "title": game.title,
            "genre": game.genre,
            "ambiance": game.ambiance
        })
        if result:
            try:
                start, end = result.find("["), result.rfind("]") + 1
                return json.loads(result[start:end])[:3]
            except:
                pass
        return self._generate_characters_template(game)

    def _generate_characters_template(self, game):
        return [{
            'name': 'Aiden',
            'role': 'PROTAGONIST',
            'character_class': 'Guerrier',
            'background': "Un héros improbable.",
            'abilities': "Maîtrise du combat.",
            'motivations': "Sauver le monde.",
            'appearance': "Apparence de guerrier."
        }]

    # --------------------
    # Génération de lieux
    # --------------------
    def create_locations_for_game(self, game):
        if self.llm:
            locations_data = self._generate_locations_with_ai(game)
        else:
            locations_data = self._generate_locations_template(game)
        locations = [Location.objects.create(game=game, **l) for l in locations_data]
        return locations

    def _generate_locations_with_ai(self, game):
        template = """
Crée 3 lieux pour le jeu "{title}".
Genre: {genre}
Ambiance: {ambiance}

Format JSON strict:
[
  {{
    "name": "Nom du lieu",
    "description": "Description en 2-3 phrases",
    "atmosphere": "Atmosphère en 2 phrases",
    "gameplay_significance": "Importance gameplay"
  }}
]
"""
        result = self._generate_with_chain(template, {
            "title": game.title,
            "genre": game.genre,
            "ambiance": game.ambiance
        })
        if result:
            try:
                start, end = result.find("["), result.rfind("]") + 1
                return json.loads(result[start:end])[:3]
            except:
                pass
        return self._generate_locations_template(game)

    def _generate_locations_template(self, game):
        return [{
            'name': 'La Forêt Enchantée',
            'description': "Un lieu mystérieux.",
            'atmosphere': "Atmosphère magique.",
            'gameplay_significance': "Zone clé."
        }]

    # --------------------
    # Génération des prompts d'images
    # --------------------
    
    def create_concept_art_for_game(self, game):
        if not self.llm:
            character_prompt = f"Illustration d'un héros {game.genre} en {game.ambiance.lower()}"
            environment_prompt = f"Paysage {game.ambiance.lower()} pour un jeu {game.genre}"
        else:
            template = """
    Crée deux prompts textuels courts pour générer du concept art IA pour le jeu "{title}":
    1. Un personnage principal
    2. Un environnement clé

    Retourne un JSON strict :
    [{"type": "CHARACTER", "prompt": "..."}, {"type": "ENVIRONMENT", "prompt": "..."}]
    """
            result = self._generate_with_chain(template, {"title": game.title})
            import json
            try:
                start = result.find('[')
                end = result.rfind(']') + 1
                prompts = json.loads(result[start:end])
                character_prompt = next(p['prompt'] for p in prompts if p['type'] == "CHARACTER")
                environment_prompt = next(p['prompt'] for p in prompts if p['type'] == "ENVIRONMENT")
            except Exception:
                character_prompt = f"Illustration d'un héros {game.genre} en {game.ambiance.lower()}"
                environment_prompt = f"Paysage {game.ambiance.lower()} pour un jeu {game.genre}"

        # 🔹 Affichage des prompts pour debug
        print("=== Prompts pour génération d'images ===")
        print(f"Prompt personnage : {character_prompt}")
        print(f"Prompt environnement : {environment_prompt}")
        print("========================================")
        
        hf_token = settings.HUGGINGFACE_API_KEY
        # ✅ CORRECTION : Ne pas spécifier de provider
        client = InferenceClient(token=hf_token)

        for prompt, field_name, filename in [
            (character_prompt, "concept_art_character", "character.png"),
            (environment_prompt, "concept_art_environment", "environment.png")
        ]:
            try:
                print(f"⏳ Génération de {field_name} en cours...")
                
                # ✅ CORRECTION : Sans spécifier de modèle (utilise le modèle par défaut)
                # text_to_image retourne directement un objet PIL Image
                image = client.text_to_image(prompt)
                
                # ✅ Plus besoin de decoder - on a directement l'image PIL
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)
                
                getattr(game, field_name).save(
                    filename,
                    ContentFile(buffer.getvalue()),
                    save=False
                )
                print(f"✅ Génération {field_name} réussie !")
                
            except Exception as e:
                print(f"❌ Erreur génération image {field_name}: {e}")
                traceback.print_exc()

        game.save()
        return game

