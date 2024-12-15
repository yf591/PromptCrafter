# app/gui.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, simpledialog, filedialog, Toplevel
import pyperclip
import json
from app.prompt_generator import generate_prompt
from app.config import APP_SETTINGS, load_settings, save_settings, load_categories, DEFAULT_APP_SETTINGS, add_prompts_from_csv


class SettingsDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Positive Template:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.positive_template = scrolledtext.ScrolledText(master, width=60, height=5)
        self.positive_template.insert(tk.END, APP_SETTINGS.get("positive_prompt_template", ""))
        self.positive_template.grid(row=0, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="Negative Template:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.negative_template = scrolledtext.ScrolledText(master, width=60, height=5)
        self.negative_template.insert(tk.END, APP_SETTINGS.get("negative_prompt_template", ""))
        self.negative_template.grid(row=1, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="Model Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.model_name_entry = tk.Entry(master, width=60)
        self.model_name_entry.insert(0, APP_SETTINGS.get("model_name", ""))
        self.model_name_entry.grid(row=2, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="Use Model for Generation:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.use_model_var = tk.BooleanVar(value=APP_SETTINGS.get("use_model_for_generation", False))
        self.use_model_checkbox = tk.Checkbutton(master, variable=self.use_model_var)
        self.use_model_checkbox.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        tk.Label(master, text="Auto Generate Areas:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.auto_generate_areas_entry = tk.Entry(master, width=60)
        self.auto_generate_areas_entry.insert(0, ', '.join(APP_SETTINGS.get("auto_generate_areas", [])))
        self.auto_generate_areas_entry.grid(row=4, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="AI Generation Mode:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.ai_mode_var = tk.StringVar(value=APP_SETTINGS.get("ai_generation_mode", "both"))
        modes = ["positive_only", "negative_only", "both"]
        for i, mode in enumerate(modes):
            rb = tk.Radiobutton(master, text=mode, variable=self.ai_mode_var, value=mode)
            rb.grid(row=5, column=i + 1, sticky="w", padx=5, pady=5)

        add_prompts_button = tk.Button(master, text="Add Prompts from CSV", command=self.add_prompts_from_csv_action, bg="#4CAF50", fg="white")
        add_prompts_button.grid(row=6, column=0, columnspan=3, pady=10)

        return self.positive_template  # initial focus

    def add_prompts_from_csv_action(self):
         file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
         if file_path:
             add_prompts_from_csv(file_path)
             messagebox.showinfo("Success", "Prompts added to categories.json.")

    def apply(self):
        global DEFAULT_APP_SETTINGS
        APP_SETTINGS["positive_prompt_template"] = self.positive_template.get("1.0", tk.END).strip()
        APP_SETTINGS["negative_prompt_template"] = self.negative_template.get("1.0", tk.END).strip()
        APP_SETTINGS["model_name"] = self.model_name_entry.get()
        APP_SETTINGS["use_model_for_generation"] = self.use_model_var.get()
        auto_gen_areas = [area.strip() for area in self.auto_generate_areas_entry.get().split(',')]
        APP_SETTINGS["auto_generate_areas"] = [area for area in auto_gen_areas if area]
        APP_SETTINGS["ai_generation_mode"] = self.ai_mode_var.get()

        DEFAULT_APP_SETTINGS["positive_prompt_template"] = APP_SETTINGS["positive_prompt_template"]
        DEFAULT_APP_SETTINGS["negative_prompt_template"] = APP_SETTINGS["negative_prompt_template"]
        DEFAULT_APP_SETTINGS["model_name"] = APP_SETTINGS["model_name"]
        DEFAULT_APP_SETTINGS["use_model_for_generation"] = APP_SETTINGS["use_model_for_generation"]
        DEFAULT_APP_SETTINGS["auto_generate_areas"] = APP_SETTINGS["auto_generate_areas"]
        DEFAULT_APP_SETTINGS["ai_generation_mode"] = APP_SETTINGS["ai_generation_mode"]

        save_settings()
class PromptCrafterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PromptCrafter")
        self.root.geometry("1200x800")
        self.center_window(self.root)
        
        self.setup_ui()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Keywords entry
        tk.Label(self.root, text="Enter Keywords:").pack(pady=5, anchor="w")
        self.keyword_entry = scrolledtext.ScrolledText(self.root, width=80, height=6)
        self.keyword_entry.pack(pady=5, anchor="w")

        # Prompts display
        tk.Label(self.root, text="Positive Prompt:").pack(pady=5, anchor="w")
        self.positive_prompt_text = scrolledtext.ScrolledText(self.root, width=120, height=8)
        self.positive_prompt_text.pack(pady=5, anchor="w")

        tk.Label(self.root, text="Negative Prompt:").pack(pady=5, anchor="w")
        self.negative_prompt_text = scrolledtext.ScrolledText(self.root, width=120, height=8)
        self.negative_prompt_text.pack(pady=5, anchor="w")


        # LoRA dropdown
        tk.Label(self.root, text="Select LoRA:").pack(pady=5, anchor="w")
        self.lora_var = tk.StringVar(self.root)
        self.lora_var.set("None")  # Set initial value
        self.lora_dropdown = ttk.Combobox(self.root, textvariable=self.lora_var, values=["None"] + APP_SETTINGS.get("loras", []))
        self.lora_dropdown.pack(pady=5, anchor="w")

        # Prompt search
        tk.Label(self.root, text="Search Prompts:").pack(pady=5, anchor="w")
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5, anchor="w")

        search_button = tk.Button(self.root, text="Search", command=self.search_prompts_action, bg="#2196F3", fg="white")
        search_button.pack(pady=5, anchor="w")

        # Categories and words frame
        self.categories_frame = tk.Frame(self.root)
        self.categories_frame.pack(pady=10, anchor="w")
        self.category_buttons = {}
        self.create_category_buttons()


        # Buttons
        generate_button = tk.Button(self.root, text="Generate Prompt", command=self.generate_prompt_action, bg="#4CAF50", fg="white")
        generate_button.pack(pady=10, anchor="w")
        
        copy_positive_button = tk.Button(self.root, text="Copy Positive Prompt", command=self.copy_positive_prompt, bg="#2196F3", fg="white")
        copy_positive_button.pack(pady=5, anchor="w")
        
        copy_negative_button = tk.Button(self.root, text="Copy Negative Prompt", command=self.copy_negative_prompt, bg="#2196F3", fg="white")
        copy_negative_button.pack(pady=5, anchor="w")
        
        settings_button = tk.Button(self.root, text="Settings", command=self.open_settings, bg="#9E9E9E", fg="white")
        settings_button.pack(pady=5, anchor="w")

        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load Settings", command=self.load_settings_from_file)
        filemenu.add_command(label="Save Settings", command=self.save_settings_to_file)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def load_settings_from_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            load_settings(file_path)
            self.update_ui_elements()

    def save_settings_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            save_settings(file_path)
            self.update_config_file()
    
    def update_config_file(self):
        # config.pyのDEFAULT_APP_SETTINGSを更新する
        from app.config import DEFAULT_APP_SETTINGS
        DEFAULT_APP_SETTINGS["positive_prompt_template"] = APP_SETTINGS["positive_prompt_template"]
        DEFAULT_APP_SETTINGS["negative_prompt_template"] = APP_SETTINGS["negative_prompt_template"]
        DEFAULT_APP_SETTINGS["model_name"] = APP_SETTINGS["model_name"]
        DEFAULT_APP_SETTINGS["use_model_for_generation"] = APP_SETTINGS["use_model_for_generation"]
        DEFAULT_APP_SETTINGS["auto_generate_areas"] = APP_SETTINGS["auto_generate_areas"]
        DEFAULT_APP_SETTINGS["ai_generation_mode"] = APP_SETTINGS["ai_generation_mode"]
        # config.pyに上書き保存する処理を追加（ここでは仮実装）
        with open('app/config.py', 'r') as f:
            lines = f.readlines()
        with open('app/config.py', 'w') as f:
            for line in lines:
                if line.strip().startswith("DEFAULT_APP_SETTINGS = {"):
                    f.write(f'DEFAULT_APP_SETTINGS = {json.dumps(DEFAULT_APP_SETTINGS, indent=4)}\n')
                else:
                    f.write(line)

    def update_ui_elements(self):
        self.lora_dropdown.config(values=["None"] + APP_SETTINGS.get("loras", []))
        self.create_category_buttons()

    def create_category_buttons(self):
        # Clear previous buttons
        for button in self.category_buttons.values():
            button.destroy()

        self.category_buttons = {}
        categories = load_categories()

        for i, (category, subcategories) in enumerate(categories.items()):
          button_color = "#673AB7"
          if category == "NSFW":
              button_color = "red"
          elif category == "Prompts":
              button_color = "red"
          category_button = tk.Button(self.categories_frame, text=category, 
                                          command=lambda cat=category: self.show_subcategories(cat),
                                          bg=button_color, fg="white")
          category_button.grid(row=0, column=i, padx=5, pady=5)
          self.category_buttons[category] = category_button

    def show_subcategories(self, category):
        categories = load_categories()
        subcategories = categories.get(category, {})
        popup = Toplevel(self.root)
        popup.title(category)
        popup.geometry("300x400")
        self.center_window(popup)
        
        item_frame = scrolledtext.ScrolledText(popup, width=40, height=15)
        item_frame.pack(pady=5, padx=5, fill="both", expand=True)
        item_frame.configure(state="normal")

        if category == "Prompts":
          for i, (subcategory, items) in enumerate(subcategories.items()):
              subcategory_button = tk.Button(item_frame, text=subcategory, 
                                                  command=lambda items=items, subcategory=subcategory: self.show_items("Prompts", items, popup),
                                                bg="#9C27B0", fg="white")
              item_frame.window_create("end", window=subcategory_button)
              item_frame.insert("end", "\n")
              
        else:
          for i, (subcategory, items) in enumerate(subcategories.items()):
            subcategory_button = tk.Button(item_frame, text=subcategory, 
                                                command=lambda cat=subcategory, items=items: self.show_items(cat, items, popup),
                                                bg="#9C27B0", fg="white")
            item_frame.window_create("end", window=subcategory_button)
            item_frame.insert("end", "\n")
        item_frame.configure(state="disabled")
        # Add scroll to top functionality to the text box
        item_frame.bind("<MouseWheel>", lambda event: self.scroll_text(event, item_frame))


    def show_items(self, subcategory, items, popup):
        item_popup = Toplevel(self.root)
        item_popup.title(subcategory)
        item_popup.geometry("300x400")
        self.center_window(item_popup)
        item_popup.config(cursor="arrow")
        
        item_frame = scrolledtext.ScrolledText(item_popup, width=40, height=15)
        item_frame.pack(pady=5, padx=5, fill="both", expand=True)
        item_frame.configure(state="normal")
        self.item_vars = {}
        for item in items:
            var = tk.BooleanVar()
            self.item_vars[item] = var
            check_button = tk.Checkbutton(item_frame, text=item, variable=var, bg="white", fg="black",
                                          selectcolor="white", activebackground="white", activeforeground="white",
                                          borderwidth=1, relief="solid", highlightthickness=0)

            item_frame.window_create("end", window=check_button)
            item_frame.insert("end", "\n")
        item_frame.configure(state="disabled")
        # Add scroll to top functionality to the text box
        item_frame.bind("<MouseWheel>", lambda event: self.scroll_text(event, item_frame))
        add_button = tk.Button(item_popup, text="Add Selected Items", command=lambda: self.add_selected_items_to_prompt(popup, item_popup), bg="#4CAF50", fg="white")
        add_button.pack(pady=10, anchor="w")

    def scroll_text(self, event, text_widget):
        text_widget.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_selected_items_to_prompt(self, popup, item_popup):
        selected_items = [item for item, var in self.item_vars.items() if var.get()]
        current_text = self.keyword_entry.get("1.0", tk.END).strip()
        if current_text:
            self.keyword_entry.delete("1.0", tk.END)
            self.keyword_entry.insert("1.0", f"{current_text}, {', '.join(selected_items)}")
        else:
          self.keyword_entry.insert("1.0", ', '.join(selected_items))
        popup.destroy()
        item_popup.destroy()

    def search_prompts_action(self):
      search_term = self.search_entry.get().strip()
      if not search_term:
          messagebox.showwarning("Input Error", "Please enter a search term.")
          return

      search_results = self.search_prompts(search_term)
      self.show_search_results(search_results)

    def search_prompts(self, search_term):
        all_categories = load_categories()
        results = []
        for main_cat, sub_cats in all_categories.items():
            if main_cat == "Prompts":
              for sub_cat, items in sub_cats.items():
                for item in items:
                  if search_term.lower() in item.lower():
                    results.append(f"{main_cat} > {sub_cat} > {item}")
            else:
              for sub_cat, items in sub_cats.items():
                  for item in items:
                      if search_term.lower() in item.lower():
                          results.append(f"{main_cat} > {sub_cat} > {item}")

        return results

    def show_search_results(self, search_results):
      search_popup = Toplevel(self.root)
      search_popup.title("Search Results")
      search_popup.geometry("400x300")
      self.center_window(search_popup)
      
      result_frame = scrolledtext.ScrolledText(search_popup, width=50, height=10)
      result_frame.pack(pady=5, padx=5, fill="both", expand=True)
      result_frame.configure(state="normal")
      self.search_vars = {}

      if not search_results:
          result_frame.insert("end", "No results found.")
      else:
          for result in search_results:
            var = tk.BooleanVar()
            self.search_vars[result] = var
            check_button = tk.Checkbutton(result_frame, text=result, variable=var, bg="white", fg="black",
                                          selectcolor="white", activebackground="white", activeforeground="white",
                                          borderwidth=1, relief="solid", highlightthickness=0)

            result_frame.window_create("end", window=check_button)
            result_frame.insert("end", "\n")

      result_frame.configure(state="disabled")

      add_button = tk.Button(search_popup, text="Add Selected Prompts", command=lambda: self.add_selected_search_results_to_prompt(search_popup), bg="#4CAF50", fg="white")
      add_button.pack(pady=10, anchor="w")


    def add_selected_search_results_to_prompt(self, popup):
       selected_items = [item for item, var in self.search_vars.items() if var.get()]
       current_text = self.keyword_entry.get("1.0", tk.END).strip()
       if current_text:
           self.keyword_entry.delete("1.0", tk.END)
           self.keyword_entry.insert("1.0", f"{current_text}, {', '.join(selected_items)}")
       else:
           self.keyword_entry.insert("1.0", ', '.join(selected_items))
       popup.destroy()

    def generate_prompt_action(self):
        keyword = self.keyword_entry.get("1.0", tk.END).strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return
        
        selected_lora = self.lora_var.get() if self.lora_var.get() != "None" else ""
        positive_prompt, negative_prompt = generate_prompt(keyword, selected_lora)
        
        self.positive_prompt_text.delete("1.0", tk.END)
        self.positive_prompt_text.insert(tk.END, positive_prompt)
        self.negative_prompt_text.delete("1.0", tk.END)
        self.negative_prompt_text.insert(tk.END, negative_prompt)
        
    def copy_positive_prompt(self):
        pyperclip.copy(self.positive_prompt_text.get("1.0", tk.END))
        messagebox.showinfo("Copied", "Positive prompt copied to clipboard!")
    
    def copy_negative_prompt(self):
        pyperclip.copy(self.negative_prompt_text.get("1.0", tk.END))
        messagebox.showinfo("Copied", "Negative prompt copied to clipboard!")

    def open_settings(self):
        SettingsDialog(self.root)
        self.update_ui_elements()


def create_gui():
    root = tk.Tk()
    gui = PromptCrafterGUI(root)
    root.mainloop()