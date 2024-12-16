import json
import os
import csv

SETTINGS_FILE = "app_settings.json"
CATEGORIES_FILE = "categories.json"

DEFAULT_APP_SETTINGS = {
    "positive_prompt_template": "high quality, masterpiece, best quality, extremely detailed CG, 8k, {keyword}, realistic, sharp focus, intricate details, professional art",
    "negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, bad anatomy, disfigured, out of focus, bad proportions, cartoon, anime, 3d",
    "model_name": "Gustavosta/MagicPrompt-Stable-Diffusion",
    "use_model_for_generation": True,
    "auto_generate_areas": ["People", "Background", "NSFW"],
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
             CATEGORIES = json.dump(CATEGORIES, f, indent=4, ensure_ascii=False)
    except FileNotFoundError:
       print("Error: categories.json not found. Creating default one.")
       CATEGORIES = {}
       save_categories()
    except json.JSONDecodeError:
        print("Error: categories.json has invalid JSON format. Loading default values.")
        CATEGORIES = {}
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
                japanese_expression = row.get("Japanese_Expressions")

                if category and prompt and japanese_expression:
                  if "Prompts" not in CATEGORIES:
                    CATEGORIES["Prompts"] = {}
                  if category not in CATEGORIES["Prompts"]:
                    CATEGORIES["Prompts"][category] = {}
                  if japanese_expression not in CATEGORIES["Prompts"][category]:
                    CATEGORIES["Prompts"][category][japanese_expression] = prompt

        save_categories()
    except Exception as e:
        print(f"Error loading CSV file: {e}")

load_settings()
load_categories()