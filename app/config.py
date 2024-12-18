# config.py

import json
import os
import csv

SETTINGS_FILE = "app_settings.json"
CATEGORIES_FILE = "categories.json"

DEFAULT_APP_SETTINGS = {
    "realistic_positive_prompt_template": "high quality, masterpiece, best quality, extremely detailed CG, 8k, {keyword}, realistic, sharp focus, intricate details, professional art, highly detailed, aesthetic, hyperrealistic, cinematic lighting",
    "realistic_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, nsfw, "
                                         "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), cartoon, anime, 3d, "
                                         "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                         "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                         "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                         "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "2d_positive_prompt_template": "masterpiece, best quality, high quality, {keyword}, highly detailed, aesthetic, vibrant, colorful, anime style, official art, sharp focus, character design, professional art",
    "2d_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, nsfw, "
                                     "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), realistic, 3d, "
                                     "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                     "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                     "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                     "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "2.5d_positive_prompt_template": "masterpiece, best quality, high quality, {keyword}, highly detailed, aesthetic, semi-realistic, 2.5d, detailed shading, professional art, volumetric lighting, artistic, octane render, cinematic",
    "2.5d_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, nsfw, "
                                       "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), realistic, anime, 3d, "
                                       "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                       "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                       "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                       "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "nsfw_realistic_positive_prompt_template": "nsfw, high quality, masterpiece, best quality, extremely detailed CG, 8k, {keyword}, realistic, sharp focus, intricate details, professional art, highly detailed, aesthetic, hyperrealistic, cinematic lighting, explicit, mature",
    "nsfw_realistic_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, sfw, "
                                              "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), cartoon, anime, 3d, "
                                              "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                              "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                              "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                              "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "nsfw_2d_positive_prompt_template": "nsfw, masterpiece, best quality, high quality, {keyword}, highly detailed, aesthetic, vibrant, colorful, anime style, official art, sharp focus, character design, professional art, explicit, mature",
    "nsfw_2d_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, sfw, "
                                          "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), realistic, 3d, "
                                          "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                          "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                          "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                          "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "nsfw_2.5d_positive_prompt_template": "nsfw, masterpiece, best quality, high quality, {keyword}, highly detailed, aesthetic, semi-realistic, 2.5d, detailed shading, professional art, volumetric lighting, artistic, octane render, cinematic, explicit, mature",
    "nsfw_2.5d_negative_prompt_template": "low quality, worst quality, normal quality, blurry, pixelated, distortion, sfw, "
                                          "(bad anatomy:1.3), (disfigured:1.3), (bad proportions:1.3), (ugly:1.2), (mutation:1.2), (long neck:1.3), realistic, anime, 3d, "
                                          "(((extra limbs:1.5))), ((extra arms:1.5)), ((extra legs:1.5)), ((extra hands:1.5)), ((extra feet:1.5)), ((extra fingers:1.5)), ((extra toes:1.5)), "
                                          "((missing limbs:1.5)), ((missing arms:1.5)), ((missing legs:1.5)), ((missing hands:1.5)), ((missing feet:1.5)), "
                                          "(((mutated hands:1.5))), (((bad hands:1.5))), ((poorly drawn hands:1.5)), ((fused fingers:1.5)), ((too many fingers:1.5)), ((bad fingers:1.5)), "
                                          "(((poorly drawn face:1.4))), ((bad face:1.4))",
    "use_model_for_generation": True,
    "auto_generate_areas": ["People", "Background", "NSFW"],
    "ai_generation_mode": "both",
    "loras": ["add-detail-xl", "epi_noiseoffset2", "lcm-lora-sdxl"],
    "selected_positive_template": "realistic_positive_prompt_template",
    "selected_negative_template": "realistic_negative_prompt_template"
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