import json
import os
import csv

SETTINGS_FILE = "app_settings.json"
CATEGORIES_FILE = "categories.json"

DEFAULT_APP_SETTINGS = {
    "positive_prompt_template": "extremely detailed CG, 8k, masterpiece, best quality, hyperrealistic, sharp focus, intricate details, professional art, perfect lighting, ultra high res,  {keyword}, RAW photo, no artifacts, best quality",
    "negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, bad anatomy, disfigured, out of focus, bad proportions, cartoon, anime, 3d,  (worst quality:1.5), (low quality:1.5), (normal quality:1.5), lowres, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, low contrast, text, logo, watermark",
    "model_name": "Gustavosta/MagicPrompt-Stable-Diffusion",
    "use_model_for_generation": True, # AI自動生成を使用しない場合はFalseに設定する
    "auto_generate_areas": ["People", "NSFW", "Prompts"],
     "ai_generation_mode": "both",
    "loras": ["add-detail-xl", "epi_noiseoffset2", "lcm-lora-sdxl"]
}


APP_SETTINGS = {}
CATEGORIES = {}

def save_settings(file_path=None):
    global APP_SETTINGS
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(APP_SETTINGS, f, indent=4)
    else:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(APP_SETTINGS, f, indent=4)

def load_settings(file_path = None):
  global APP_SETTINGS
  try:
    if file_path:
      with open(file_path, 'r') as f:
        APP_SETTINGS = json.load(f)
    elif os.path.exists(SETTINGS_FILE):
      with open(SETTINGS_FILE, 'r') as f:
        APP_SETTINGS = json.load(f)
  except FileNotFoundError:
      APP_SETTINGS = DEFAULT_APP_SETTINGS.copy()
      save_settings()
  except json.JSONDecodeError:
    APP_SETTINGS = DEFAULT_APP_SETTINGS.copy()
    save_settings()
  
  if not APP_SETTINGS:
      APP_SETTINGS = DEFAULT_APP_SETTINGS.copy()
      save_settings()

def load_categories(file_path=None):
    global CATEGORIES
    try:
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                CATEGORIES = json.load(f)
        elif os.path.exists(CATEGORIES_FILE):
            with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
                CATEGORIES = json.load(f)
        else:
          with open(os.path.join(os.path.dirname(__file__), "categories.json"), 'r', encoding='utf-8') as f:
             CATEGORIES = json.load(f)

    except FileNotFoundError:
        print("Error: categories.json not found. Creating default one.")
        CATEGORIES = {
            "Nature": {
                "Landscape": ["mountain", "river", "lake", "sea", "forest", "grassland", "desert", "polar"],
                "Living Things": ["animal", "plant", "insect", "bird", "fish", "microorganism"],
                "Celestial": ["star", "planet", "galaxy", "space"],
                "Weather": ["sunny", "rainy", "snowy", "rainbow", "stormy"]
            },
            "People": {
                "Occupation": ["doctor", "teacher", "painter", "engineer", "chef", "athlete"],
                "Age": ["child", "teenager", "middle-aged", "elderly"],
                "Emotion": ["joy", "anger", "sadness", "pleasure", "surprise", "fear", "excitement"],
                "Condition": ["sleeping", "eating", "exercising", "working", "playing"]
            },
            "Buildings & Structures": {
                "Type": ["house", "office building", "factory", "school", "hospital", "station", "bridge", "tower"],
                "Style": ["ancient", "medieval", "modern", "futuristic", "Japanese", "Western"],
                "Material": ["wood", "stone", "iron", "glass", "concrete"]
            },
            "Art": {
                "Painting": ["oil painting", "watercolor", "Japanese painting", "abstract painting", "portrait painting"],
                "Sculpture": ["plaster", "bronze", "wood carving"],
                "Music": ["instrument", "performance", "composition"],
                "Literature": ["novel", "poem", "drama"]
            },
            "Concept": {
                "Abstract": ["love", "peace", "freedom", "justice", "time", "space"],
                "Philosophical": ["existence", "consciousness", "truth", "beauty"],
                "Religious": ["god", "buddha", "angel", "demon"]
            },
            "Fantasy": {
                "Race": ["elf", "fairy", "dragon", "vampire", "werewolf"],
                "World": ["medieval fantasy", "sci-fi", "magic world", "other world"],
                "Item": ["magic wand", "sword", "potion", "ring"]
            },
            "Cyberpunk": {
                "City": ["neon city", "skyscraper", "slum"],
                "Technology": ["robot", "AI", "virtual reality", "cyberspace"],
                "People": ["hacker", "cyborg", "mercenary"]
            },
            "Steampunk": {
                "Machine": ["steam engine", "gear", "clock"],
                "City": ["chimney", "factory", "airship"],
                "Fashion": ["corset", "goggle"]
            },
            "Retro": {
                "Era": ["1950s", "1960s", "1970s"],
                "Style": ["vintage", "retro-futuristic"]
            },
            "Pop Culture": {
                "Anime": ["Japanese anime", "Western anime"],
                "Manga": ["Japanese manga", "Western manga"],
                "Game": ["RPG", "action game", "adventure game"],
                "Movie": ["sci-fi movie", "fantasy movie", "horror movie"]
            },
             "NSFW": {
                "General": ["nude", "explicit", "hentai", "erotic", "adult", "bdsm"],
                "Acts": ["oral sex", "anal sex", "masturbation", "group sex", "non-consensual sex"],
                "Fetishes": ["uniform fetish", "foot fetish", "hand fetish", "breast fetish", "butt fetish", "thigh fetish", "leg fetish", "arm fetish", "back fetish", "neck fetish", "hair fetish", "eye fetish", "mouth fetish", "ear fetish", "belly fetish", "navel fetish", "latex fetish", "leather fetish", "rubber fetish", "lace fetish", "silk fetish", "nylon fetish", "stocking fetish", "garter fetish", "black net tights fetish", "corset fetish"],
                "Body Parts": ["penis", "vagina", "nipples", "areola", "genitals", "pubic hair", "butt", "chest", "thighs", "legs", "arms", "Sperm", "clitoris"],
                "Positions": ["69", "Cowgirl", "Doggy Style", "Missionary", "Spoon", "Standing Sex", "Bending over", "On all fours", "Spreading legs", "Arching back", "Tining head back", "Prone", "Lying on one's back"],
                "Situations": ["bondage", "Voyeur", "Exhibitionism", "Strip", "Pole Dance", "Lap Dance", "Private Dance", "Strip Club", "Massage Parlour", "Sex Toys", "Fetish Equipment", "Handcuffs", "Blindfold", "Spanking", "Teasing", "Denial", "Watersports", "Bukkake", "Creampie", "Gangbang", "Orgy", "many girls one lucky guy", "harem play", "Age play", "Cuckold", "Female domination", "Male domination"],
                "Paraphilia": ["voyeurism", "exhibitionism"],
                 "BDSM": ["domination", "submission", "sadomasochism"],
                "Fluids": ["sweat", "orgasm", "ejaculation", "semen", "vaginal fluids", "oral fluids", "anal fluids", "erection", "Pee", "piss", "feces", "shit", "vomit", "blood", "mucus", "saliva", "after cum", "before cum", "during cum"]
            }
        }
        save_categories()

    return CATEGORIES

def save_categories(file_path=None):
    global CATEGORIES
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(CATEGORIES, f, indent=4, ensure_ascii=False)
    else:
        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(CATEGORIES, f, indent=4, ensure_ascii=False)

def add_prompts_from_csv(file_path):
    global CATEGORIES
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category = row.get("Item")
                prompt = row.get("Prompt")
                if category and prompt:
                  if "Prompts" not in CATEGORIES:
                    CATEGORIES["Prompts"] = {}
                  if category not in CATEGORIES["Prompts"]:
                      CATEGORIES["Prompts"][category] = []
                  if prompt not in CATEGORIES["Prompts"][category]:
                      CATEGORIES["Prompts"][category].append(prompt)

        save_categories()
    except Exception as e:
        print(f"Error loading CSV file: {e}")


load_settings()
load_categories()