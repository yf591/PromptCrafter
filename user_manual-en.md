# PromptCrafter User Manual


## Application Overview

PromptCrafter is a desktop application designed to help you generate prompts for Stable Diffusion image generation. This app utilizes AI models or templates to create high-quality prompts, assisting you in creating images effectively.


## How to Launch the Application

1.  Clone or download the repository and navigate to the PromptCrafter folder.
2.  To install the required libraries, run the following command in the command line or terminal:

```bash
pip install -r requirements.txt
```

3. Run the following command to launch the application:

```bash
python main.py
```


## Main Screen Operation

1.  **Keyword Input:**
    * In the text box labeled "Enter Keywords:" at the top of the screen, enter keywords you want to use for prompt generation. If you're entering multiple keywords, separate them with commas.
2.  **Prompt Display:**
    * The generated prompts will appear in the text boxes below, labeled "Positive Prompt:" and "Negative Prompt:".
3.  **LoRA Selection:**
    * Select the LoRA model you want to use from the drop-down menu labeled "Select LoRA:". If you do not want to use a LoRA model, leave the selection on "None".
4.  **Category Selection**
    * Click category buttons (e.g., "Nature," "People," "Prompts", "NSFW") in the lower left of the screen to display subcategory popup menus. 
    * Select a subcategory and choose items by clicking the check boxes to add them to the keywords input area.
5.  **Prompt Search:**
    * Enter a keyword in the text box labeled "Search Prompts:" and click the "Search" button.
    * The search results will appear in a popup window, and you can add prompts to the keywords input area by checking the checkboxes and clicking "Add Selected Prompts".
6.  **Prompt Generation:**
    * Click the "Generate Prompt" button to generate prompts based on the entered keywords and settings. The generated prompts will be displayed in the prompt display areas.
7.  **Copying Prompts**
    * Click the “Copy Positive Prompt” button to copy the positive prompt to the clipboard.
    * Click the “Copy Negative Prompt” button to copy the negative prompt to the clipboard.

## Settings Screen Operation

1.  **Launching the Settings Screen:**
    * Click the "Settings" button on the main screen to open the settings screen.
2.  **Editing Prompt Templates:**
    * In the text boxes labeled "Positive Template:" and "Negative Template:", edit the templates used for prompt generation. Use `{keyword}` to include the content from the keyword input.
3.  **Model Selection:**
    * In the text box labeled "Model Name:", enter the name of a text generation model downloadable from the Hugging Face Hub.
4.  **Enabling AI Generation:**
    * Check the "Use Model for Generation:" checkbox to enable prompt generation using an AI model. Uncheck it to generate prompts using templates.
5.  **AI Generation Mode Setting:**
    * You can choose the mode for AI prompt generation:  "positive_only(AI generates only positive prompt)", "negative_only(AI generates only negative prompt)", or "both(AI generates both)".
6.  **Specifying auto-generation areas:**
    * In the text box labeled "Auto Generate Areas:", enter the keyword categories that AI should automatically generate (separated by commas, e.g., `style, subject`).
7.  **Adding Prompts from CSV File:**
    * Click the "Add Prompts from CSV" button and select a CSV file containing additional prompts. The content of the CSV file will be added to the Prompts category and be available through the search function.
8.  **Saving Settings:**
    * Click the "OK" button to save the changed settings.

## Editing Configuration Files

1.  **`app_settings.json`:**
    * This file stores the application's settings.
    * Changes made through the GUI’s setting screen are saved to this file.
2.  **`categories.json`:**
    * This file describes the categories and keywords to generate the prompts.
    * You can change the categories and keywords that are displayed in GUI by editing this file.
3.  **`config.py`:**
    * This file contains the default settings of the application.
    * You can edit the default settings by changing `DEFAULT_APP_SETTINGS` in this file.

## Troubleshooting

*   **If the model cannot be loaded:**
    *   Check whether the model specified in `model_name` exists on the Hugging Face Hub.
    *   Downloading the model may take time when starting the application for the first time or after changing the model.
*   **If prompts are not being generated:**
    *   Make sure that the keywords for prompt generation are entered in the keyword input.
    *   When using the AI model, make sure that you have specified a text generation model in `model_name`.
    *   If you are using the AI model, make sure `auto_generate_areas` specifies the appropriate category.
*  **If the "Prompts" button does not appear in GUI:**
   *    After adding prompts from the CSV file, it will be automatically displayed in GUI.
   *    Or confirm that “Prompts” category exists in `categories.json`.

## Disclaimer

* When using the NSFW categories, please comply with the terms of service and laws.
* Some models may cause out-of-memory errors. If this happens, try using a lightweight model.