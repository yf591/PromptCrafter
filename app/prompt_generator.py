# prompt_generator.py

from transformers import pipeline
from app.config import APP_SETTINGS
import torch

generator = None
if APP_SETTINGS.get("use_model_for_generation", False) and APP_SETTINGS.get("model_name", ""):
    try:
        generator = pipeline("text-generation", model=APP_SETTINGS["model_name"], device=0 if torch.cuda.is_available() else -1)
        print("Model Loaded Successfully:", APP_SETTINGS["model_name"])
    except Exception as e:
        print(f"Error loading model: {e}")

def generate_prompt(keyword, lora_name="", mode="both"):
    positive_prompt = ""
    negative_prompt = ""

    positive_template = APP_SETTINGS.get(APP_SETTINGS.get("selected_positive_template"), "")
    negative_template = APP_SETTINGS.get(APP_SETTINGS.get("selected_negative_template"), "")

    if APP_SETTINGS.get("use_model_for_generation", False) and generator:
        if mode == "positive_only" or mode == "both":
            positive_prompt = _generate_model_prompt(keyword, "positive")
        if mode == "negative_only" or mode == "both":
            negative_prompt = _generate_model_prompt(keyword, "negative")
    else:
        if mode == "positive_only" or mode == "both":
            positive_prompt = positive_template.format(keyword=keyword)
        if mode == "negative_only" or mode == "both":
            negative_prompt = negative_template.format(keyword=keyword)

    if lora_name and lora_name != "None":
        positive_prompt = f"<lora:{lora_name}:1>, {positive_prompt}"

    return positive_prompt, negative_prompt

def _generate_model_prompt(keyword, prompt_type):
    if prompt_type == "positive":
        prompt_start = f"Generate a high quality, masterpiece, best quality, extremely detailed CG, 8k, realistic, sharp focus, intricate details, professional art about"
        prompt_end = ""
        if APP_SETTINGS.get("auto_generate_areas"):
            prompt_end = ", ".join([f" related to {area}" for area in APP_SETTINGS.get("auto_generate_areas")])
        prompt = f"{prompt_start} {keyword}{prompt_end}:"
    elif prompt_type == "negative":
        prompt = f"Generate a negative prompt about {keyword}:"

    try:
        generated_text = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        
        if prompt_type == "positive":
            # Remove the prompt itself from the generated text
            generated_text = generated_text.replace(prompt, "").strip()
            # Remove unwanted characters
            unwanted_chars = ['"', ':', '*']
            for char in unwanted_chars:
                generated_text = generated_text.replace(char, "")
            return generated_text
        elif prompt_type == "negative":
            # Remove unwanted characters
            unwanted_chars = ['"', ':', '*']
            for char in unwanted_chars:
                generated_text = generated_text.replace(char, "")
            return generated_text
    except Exception as e:
        print(f"Error during model generation: {e}")
        return f"Error: Could not generate prompt for {keyword} - {prompt_type}"

def _generate_template_prompt(keyword, prompt_type):
    # この関数は使用されなくなったため、空の文字列を返すように変更
    return ""