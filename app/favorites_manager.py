# favorites_manager.py

import json
import os
from app.config import CATEGORIES_FILE, load_categories, save_categories

def add_to_favorites(prompt, prompt_type, key):
    categories = load_categories()
    if "Favorites" not in categories:
        categories["Favorites"] = {
            "Positive": {},
            "Negative": {}
        }

    if prompt_type == "Positive":
        categories["Favorites"]["Positive"][key] = prompt
        save_categories(CATEGORIES_FILE)
        return True
    elif prompt_type == "Negative":
        categories["Favorites"]["Negative"][key] = prompt
        save_categories(CATEGORIES_FILE)
        return True
    else:
        return False

def remove_from_favorites(key, prompt_type):
    categories = load_categories()
    if "Favorites" in categories and prompt_type in categories["Favorites"] and key in categories["Favorites"][prompt_type]:
        del categories["Favorites"][prompt_type][key]
        save_categories(CATEGORIES_FILE)
        return True
    else:
        return False