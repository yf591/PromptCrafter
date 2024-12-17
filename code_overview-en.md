# PromptCrafter Code Overview

## `app/__init__.py`
*   **Overview**
    * This file is a Python package initialization file. It is usually empty, but it can include package-level initialization code if needed.
*   **Code Explanation**
    *   This is an empty file used to indicate that the `app` directory should be recognized as a Python package.

## `app/gui.py`
*   **Overview**
    * This file defines the GUI (Graphical User Interface) of the application. It uses the Tkinter library to create UI elements such as windows, buttons, and text input fields and manages user interactions.
*   **Code Explanation**
    *   **`SettingsDialog` Class:** Defines the settings dialog box. It enables the modification of settings such as prompt templates, model names, AI generation mode, and LoRA models.
    *   **`PromptCrafterGUI` Class:** Defines the main window and its widgets. It manages the main UI elements of the application, including keyword input, prompt display, LoRA selection, category selection, search, and various buttons.
    *   **Event Handlers:** Defines the behavior when each button is clicked. For example, `generate_prompt_action()` generates and displays prompts, `copy_positive_prompt()` and `copy_negative_prompt()` copy prompts to the clipboard, and `open_settings()` opens the settings screen.
    *   **`create_gui()` Function:** Creates the main window of the application and starts the Tkinter main loop.

## `app/prompt_generator.py`
*   **Overview**
    * This file defines the logic for generating prompts using an AI model. It uses the Hugging Face `transformers` library to load a text generation model and generate prompts.
*   **Code Explanation**
    *   **Global Variable `generator`:** Stores the AI model used for prompt generation. The model is loaded during initialization based on the model name set in `config.py`.
    *   **`generate_prompt(keyword, lora_name)` Function:** Takes a keyword and a selected LoRA model name, and calls either the `_generate_model_prompt` or `_generate_template_prompt` function to generate both positive and negative prompts.
    *   **`_generate_model_prompt(keyword, prompt_type)` Function:** Handles prompt generation using the AI model. Returns an error message if the model could not be loaded.
    *   **`_generate_template_prompt(keyword, prompt_type)` Function:** Handles prompt generation based on a template. Uses the templates set in `config.py`.

## `app/config.py`
*   **Overview**
    * This file defines the application’s settings and manages the loading and saving of configuration files (`app_settings.json`, `categories.json`).
*   **Code Explanation**
    *   **`DEFAULT_APP_SETTINGS`:** Defines the default settings for the application. Includes the prompt templates, model name, AI generation mode, LoRA list, etc.
    *   **`APP_SETTINGS`:** A global variable that stores the settings used during the application’s runtime.
    *   **`SETTINGS_FILE` and `CATEGORIES_FILE`:** Defines the filenames for the settings file and the categories file, respectively.
    *   **`load_settings(file_path=None)` Function:** Loads application settings from the specified JSON file (or the default `app_settings.json`). If no file is found, it applies default settings and creates the file.
    *   **`save_settings(file_path=None)` Function:** Saves the current application settings to a JSON file.
    *   **`load_categories(file_path=None)` Function:** Loads the categories from the specified JSON file (or the default `categories.json`). If no file is found, it creates default categories and the file.
    *   **`save_categories(file_path=None)` Function:** Saves the current categories to a JSON file.
    *    **`add_prompts_from_csv(file_path)` Function:**  Reads the specified CSV file and adds categories and prompts.

## `app/favorites_manager.py`

*   **Overview**
    * This file defines the logic for adding and removing favorite prompts.
*   **Code Explanation**
    *   **`add_to_favorites(prompt, prompt_type, key)` Function:** Adds a prompt to favorites with the specified prompt, type, and key.
    *   **`remove_from_favorites(key, prompt_type)` Function:** Removes a favorite prompt that matches the specified key and type.

## `categories.json`
*   **Overview**
    * This file defines a hierarchical structure of keyword categories used for generating prompts. It consists of major, medium, and minor categories used in keyword selection and search functionalities in the GUI.
*   **Code Explanation**
    *   Categories such as `Nature`, `People`, `Buildings & Structures`, `Art`, `Concept`, `Fantasy`, `Cyberpunk`, `Steampunk`, `Retro`, `Pop Culture`, `NSFW`, and `Prompts` are defined. Each category has subcategories, which have a list of keywords.