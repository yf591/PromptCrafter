import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, simpledialog, filedialog, Toplevel
import platform
import pyperclip
import json
from app.prompt_generator import generate_prompt
from app.config import APP_SETTINGS, load_settings, save_settings, load_categories, DEFAULT_APP_SETTINGS, add_prompts_from_csv
from app.favorites_manager import add_to_favorites, remove_from_favorites

class SettingsDialog(simpledialog.Dialog):
    def body(self, master):
        # テンプレート選択用のドロップダウンリスト        
        tk.Label(master, text="Selected Positive Template:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.selected_positive_template_var = tk.StringVar(value=APP_SETTINGS.get("selected_positive_template", "realistic_positive_prompt_template"))
        self.selected_positive_template_dropdown = ttk.Combobox(master, textvariable=self.selected_positive_template_var, values=list(self.get_positive_template_keys()), font=("Arial", 11), state="readonly")
        self.selected_positive_template_dropdown.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        self.selected_positive_template_dropdown.bind("<<ComboboxSelected>>", self.update_positive_template_text)

        tk.Label(master, text="Positive Template:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.positive_template = scrolledtext.ScrolledText(master, width=60, height=5, font=("Arial", 11))
        self.positive_template.insert(tk.END, APP_SETTINGS.get(self.selected_positive_template_var.get(), ""))
        self.positive_template.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        self.positive_template.config(state="disabled")  # スクロールはできるが編集はできなくする

        tk.Label(master, text="Selected Negative Template:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.selected_negative_template_var = tk.StringVar(value=APP_SETTINGS.get("selected_negative_template", "realistic_negative_prompt_template"))
        self.selected_negative_template_dropdown = ttk.Combobox(master, textvariable=self.selected_negative_template_var, values=list(self.get_negative_template_keys()), font=("Arial", 11), state="readonly")
        self.selected_negative_template_dropdown.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        self.selected_negative_template_dropdown.bind("<<ComboboxSelected>>", self.update_negative_template_text)

        tk.Label(master, text="Negative Template:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.negative_template = scrolledtext.ScrolledText(master, width=60, height=5, font=("Arial", 11))
        self.negative_template.insert(tk.END, APP_SETTINGS.get(self.selected_negative_template_var.get(), ""))
        self.negative_template.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        self.negative_template.config(state="disabled")

        tk.Label(master, text="Model Name:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.model_name_entry = tk.Entry(master, width=60, font=("Arial", 11))
        self.model_name_entry.insert(0, APP_SETTINGS.get("model_name", ""))
        self.model_name_entry.grid(row=4, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="Use Model for Generation:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.use_model_var = tk.BooleanVar(value=APP_SETTINGS.get("use_model_for_generation", False))
        self.use_model_checkbox = tk.Checkbutton(master, variable=self.use_model_var, font=("Arial", 11))
        self.use_model_checkbox.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        tk.Label(master, text="Auto Generate Areas:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.auto_generate_areas_entry = tk.Entry(master, width=60, font=("Arial", 11))
        self.auto_generate_areas_entry.insert(0, ', '.join(APP_SETTINGS.get("auto_generate_areas", [])))
        self.auto_generate_areas_entry.grid(row=6, column=1, sticky="we", padx=5, pady=5)

        tk.Label(master, text="AI Generation Mode:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.ai_mode_var = tk.StringVar(value=APP_SETTINGS.get("ai_generation_mode", "both"))
        modes = ["positive_only", "negative_only", "both"]
        for i, mode in enumerate(modes):
            rb = tk.Radiobutton(master, text=mode, variable=self.ai_mode_var, value=mode, font=("Arial", 11))
            rb.grid(row=7, column=i + 1, sticky="w", padx=5, pady=5)

        # Add Prompts from CSVボタンを移動
        add_prompts_button = tk.Button(master, text="Add Prompts from CSV", command=self.add_prompts_from_csv_action, bg="#4CAF50", fg="white", font=("Arial", 11))
        add_prompts_button.grid(row=8, column=0, columnspan=3, pady=10)

        return self.model_name_entry
    

    def add_prompts_from_csv_action(self):
         file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
         if file_path:
             add_prompts_from_csv(file_path)
             messagebox.showinfo("Success", "Prompts added to categories.json.")

    def apply(self):
        global DEFAULT_APP_SETTINGS
        APP_SETTINGS["model_name"] = self.model_name_entry.get()
        APP_SETTINGS["use_model_for_generation"] = self.use_model_var.get()
        auto_gen_areas = [area.strip() for area in self.auto_generate_areas_entry.get().split(',')]
        APP_SETTINGS["auto_generate_areas"] = [area for area in auto_gen_areas if area]
        APP_SETTINGS["ai_generation_mode"] = self.ai_mode_var.get()
        APP_SETTINGS["selected_positive_template"] = self.selected_positive_template_var.get()
        APP_SETTINGS["selected_negative_template"] = self.selected_negative_template_var.get()

        DEFAULT_APP_SETTINGS["model_name"] = APP_SETTINGS["model_name"]
        DEFAULT_APP_SETTINGS["use_model_for_generation"] = APP_SETTINGS["use_model_for_generation"]
        DEFAULT_APP_SETTINGS["auto_generate_areas"] = APP_SETTINGS["auto_generate_areas"]
        DEFAULT_APP_SETTINGS["ai_generation_mode"] = APP_SETTINGS["ai_generation_mode"]
        DEFAULT_APP_SETTINGS["selected_positive_template"] = APP_SETTINGS["selected_positive_template"]
        DEFAULT_APP_SETTINGS["selected_negative_template"] = APP_SETTINGS["selected_negative_template"]

        save_settings()

    def get_positive_template_keys(self):
        # APP_SETTINGSからポジティブテンプレートのキーだけを取得する関数(ただし、"positive_prompt_template"は除く)
        return {key: value for key, value in APP_SETTINGS.items() if "positive_prompt_template" in key and key != "positive_prompt_template"}

    def get_negative_template_keys(self):
        # APP_SETTINGSからネガティブテンプレートのキーだけを取得する関数(ただし、"negative_prompt_template"は除く)
        return {key: value for key, value in APP_SETTINGS.items() if "negative_prompt_template" in key and key != "negative_prompt_template"}
    
    def update_positive_template_text(self, event=None):
        # 選択されているテンプレートキーを取得
        selected_template_key = self.selected_positive_template_var.get()
        # 選択されているテンプレートの内容をテキストボックスに設定
        self.positive_template.config(state="normal")  # テキストボックスを通常状態（編集可能）にする
        self.positive_template.delete("1.0", tk.END)
        self.positive_template.insert("1.0", APP_SETTINGS.get(selected_template_key, ""))
        self.positive_template.config(state="disabled")  # テキストボックスを無効状態（編集不可）にする

    def update_negative_template_text(self, event=None):
        # 選択されているテンプレートキーを取得
        selected_template_key = self.selected_negative_template_var.get()
        # 選択されているテンプレートの内容をテキストボックスに設定
        self.negative_template.config(state="normal")  # テキストボックスを通常状態（編集可能）にする
        self.negative_template.delete("1.0", tk.END)
        self.negative_template.insert("1.0", APP_SETTINGS.get(selected_template_key, ""))
        self.negative_template.config(state="disabled")  # テキストボックスを無効状態（編集不可）にする

class PromptCrafterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PromptCrafter")
        # self.root.geometry("1200x800")  # 初期サイズを削除
        self.center_window(self.root)
        
        self.setup_ui()
        self.bind_scroll_events() 
        self.root.update_idletasks()
        self.adjust_window_size() # ウィンドウサイズ調整

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def position_window_relative_to_parent(self, window, position):
        window.update_idletasks()  # ウィンドウのサイズを確定
        width = window.winfo_width()
        height = window.winfo_height()
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()

        if position == "top_right":
            x = parent_x + parent_width - width
            y = parent_y
        elif position == "bottom_right":
            x = parent_x + parent_width - width
            y = parent_y + parent_height - height
        else:  # center (デフォルト)
            x = parent_x + (parent_width - width) // 2
            y = parent_y + (parent_height - height) // 2

        window.geometry(f"+{x}+{y}")

    def setup_ui(self):
        # スクロールバー設定のために、CanvasとFrameを使用
        self.main_canvas = tk.Canvas(self.root)
        self.main_canvas.pack(side="left", fill="both", expand=True)

        # スクロールバーの追加
        yscrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        yscrollbar.pack(side="right", fill="y")
        xscrollbar = tk.Scrollbar(self.main_canvas, orient="horizontal", command=self.main_canvas.xview)
        xscrollbar.pack(side="bottom", fill="x")

        self.main_canvas.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        self.main_canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        # メインフレーム
        self.main_frame = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Search Prompts
        tk.Label(self.main_frame, text="Search Prompts:", font=("Arial", 14, "bold")).pack(pady=5, anchor="w")
        self.search_entry = tk.Entry(self.main_frame, width=50, font=("Arial", 12))
        self.search_entry.pack(pady=5, anchor="w")

        search_button = tk.Button(self.main_frame, text="Search", command=self.search_prompts_action, bg="#f0f0f0", fg="black", font=("Arial", 12))
        search_button.pack(pady=5, anchor="w")

        # カテゴリボタン用のフレーム
        self.categories_frame = tk.Frame(self.main_frame)
        self.categories_frame.pack(pady=10, anchor="w", fill="x") # fill="x"を追加
        self.category_buttons = {}
        self.create_category_buttons()

        # Keywords entry
        tk.Label(self.main_frame, text="Enter Keywords:", font=("Arial", 14, "bold")).pack(pady=5, anchor="w")
        self.keyword_entry = scrolledtext.ScrolledText(self.main_frame, width=100, height=6, font=("Arial", 12))
        self.keyword_entry.pack(pady=5, anchor="w")

        # Create a frame for Generate Prompt and Clear buttons
        keyword_buttons_frame = tk.Frame(self.main_frame)
        keyword_buttons_frame.pack(pady=5, anchor="w")
        # Generate Prompt button
        generate_button = tk.Button(keyword_buttons_frame, text="Generate Prompt", command=self.generate_prompt_action, bg="#4CAF50", fg="white", font=("Arial", 12))
        generate_button.pack(side="left", padx=(0, 5))

        # Generate Prompt (Positive Only) button
        generate_positive_button = tk.Button(keyword_buttons_frame, text="Generate Prompt (Positive only)", command=lambda: self.generate_prompt_action("positive_only"), bg="#4CAF50", fg="white", font=("Arial", 12))
        generate_positive_button.pack(side="left", padx=(0, 5))

        # Generate Prompt (Negative Only) button
        generate_negative_button = tk.Button(keyword_buttons_frame, text="Generate Prompt (Negative only)", command=lambda: self.generate_prompt_action("negative_only"), bg="#4CAF50", fg="white", font=("Arial", 12))
        generate_negative_button.pack(side="left", padx=(0, 5))

        # Clear button for keyword entry
        clear_keyword_button = tk.Button(keyword_buttons_frame, text="Clear", command=lambda: self.keyword_entry.delete("1.0", tk.END), bg="#f0f0f0", font=("Arial", 12))
        clear_keyword_button.pack(side="left")

        # Positive Prompt
        tk.Label(self.main_frame, text="Positive Prompt:", font=("Arial", 14, "bold")).pack(pady=5, anchor="w")
        self.positive_prompt_text = scrolledtext.ScrolledText(self.main_frame, width=120, height=6, font=("Arial", 12))
        self.positive_prompt_text.pack(pady=5, anchor="w")

        # Create a frame for Positive Prompt buttons
        positive_buttons_frame = tk.Frame(self.main_frame)
        positive_buttons_frame.pack(pady=5, anchor="w")

        # Copy Positive Prompt button
        copy_positive_button = tk.Button(positive_buttons_frame, text="Copy Positive Prompt", command=self.copy_positive_prompt, bg="white", fg="black", font=("Arial", 12))
        copy_positive_button.pack(side="left", padx=(0, 5))

        # Add to Favorites button for positive prompt
        positive_add_button = tk.Button(positive_buttons_frame, text="Add to Favorites", command=lambda: self.add_to_favorites("Positive", self.positive_prompt_text), bg="#f0f0f0", font=("Arial", 12))
        positive_add_button.pack(side="left", padx=(0, 5))

        # Clear button for positive prompt
        positive_clear_button = tk.Button(positive_buttons_frame, text="Clear", command=lambda: self.positive_prompt_text.delete("1.0", tk.END), bg="#f0f0f0", font=("Arial", 12))
        positive_clear_button.pack(side="left")

        # Negative Prompt
        tk.Label(self.main_frame, text="Negative Prompt:", font=("Arial", 14, "bold")).pack(pady=5, anchor="w")
        self.negative_prompt_text = scrolledtext.ScrolledText(self.main_frame, width=120, height=6, font=("Arial", 12))
        self.negative_prompt_text.pack(pady=5, anchor="w")

        # Create a frame for Negative Prompt buttons
        negative_buttons_frame = tk.Frame(self.main_frame)
        negative_buttons_frame.pack(pady=5, anchor="w")

        # Copy Negative Prompt button
        copy_negative_button = tk.Button(negative_buttons_frame, text="Copy Negative Prompt", command=self.copy_negative_prompt, bg="white", fg="black", font=("Arial", 12))
        copy_negative_button.pack(side="left", padx=(0, 5))

        # Add to Favorites button for negative prompt
        negative_add_button = tk.Button(negative_buttons_frame, text="Add to Favorites", command=lambda: self.add_to_favorites("Negative", self.negative_prompt_text), bg="#f0f0f0", font=("Arial", 12))
        negative_add_button.pack(side="left", padx=(0, 5))

        # Clear button for negative prompt
        negative_clear_button = tk.Button(negative_buttons_frame, text="Clear", command=lambda: self.negative_prompt_text.delete("1.0", tk.END), bg="#f0f0f0", font=("Arial", 12))
        negative_clear_button.pack(side="left")

        # LoRA dropdown
        tk.Label(self.main_frame, text="Select LoRA:", font=("Arial", 12)).pack(pady=5, anchor="w")
        self.lora_var = tk.StringVar(self.main_frame)
        self.lora_var.set("None")
        self.lora_dropdown = ttk.Combobox(self.main_frame, textvariable=self.lora_var, values=["None"] + APP_SETTINGS.get("loras", []), font=("Arial", 12))
        self.lora_dropdown.pack(pady=5, anchor="w")

        # Buttons
        settings_button = tk.Button(self.main_frame, text="Settings", command=self.open_settings, bg="#f0f0f0", fg="black", font=("Arial", 12))
        settings_button.pack(pady=5, anchor="w")

        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load Settings", command=self.load_settings_from_file, font=("Arial", 12))
        filemenu.add_command(label="Save Settings", command=self.save_settings_to_file, font=("Arial", 12))
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        self.main_frame.update_idletasks()  # フレームのサイズを更新
        # self.main_canvas.config(scrollregion=self.main_canvas.bbox("all")) # コメントアウト
        self.main_canvas.bind('<Configure>', self.on_canvas_configure) # スクロール領域の更新

    def generate_prompt_action(self, mode="both"):
        keyword = self.keyword_entry.get("1.0", tk.END).strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return

        selected_lora = self.lora_var.get() if self.lora_var.get() != "None" else ""

        # 修正: modeの値で条件分岐
        if mode == "positive_only":
            positive_prompt, _ = generate_prompt(keyword, selected_lora, "positive_only")
            self.positive_prompt_text.delete("1.0", tk.END)
            self.positive_prompt_text.insert(tk.END, positive_prompt)
            self.negative_prompt_text.delete("1.0", tk.END) #ネガティブプロンプト欄をクリア
        elif mode == "negative_only":
            _, negative_prompt = generate_prompt(keyword, selected_lora, "negative_only")
            self.positive_prompt_text.delete("1.0", tk.END) #ポジティブプロンプト欄をクリア
            self.negative_prompt_text.delete("1.0", tk.END)
            self.negative_prompt_text.insert(tk.END, negative_prompt)
        else:
            positive_prompt, negative_prompt = generate_prompt(keyword, selected_lora, "both")
            self.positive_prompt_text.delete("1.0", tk.END)
            self.positive_prompt_text.insert(tk.END, positive_prompt)
            self.negative_prompt_text.delete("1.0", tk.END)
            self.negative_prompt_text.insert(tk.END, negative_prompt)

    def bind_scroll_events(self):
        # スクロールバーのイベントをバインド
        self.main_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.main_canvas.bind_all("<Shift-MouseWheel>", self.on_shift_mousewheel)

        # OSごとにバインディングを変更
        os_name = platform.system()
        if os_name == "Linux":
            self.main_canvas.bind_all("<Button-4>", self.on_mousewheel)
            self.main_canvas.bind_all("<Button-5>", self.on_mousewheel)
            self.main_canvas.bind_all("<Shift-Button-4>", self.on_shift_mousewheel)
            self.main_canvas.bind_all("<Shift-Button-5>", self.on_shift_mousewheel)
        elif os_name == "Darwin":
            self.main_canvas.bind_all("<Command-MouseWheel>", self.on_shift_mousewheel)

    def on_mousewheel(self, event):
        # 垂直方向のスクロール処理
        os_name = platform.system()
        if os_name == "Windows":
            delta = int(-1 * (event.delta / 120))
        elif os_name == "Darwin":
            delta = int(-1 * event.delta)
        else:  # Linux
            delta = int(-1 * event.delta)
        
        self.main_canvas.yview_scroll(delta, "units")

    def on_shift_mousewheel(self, event):
        # 水平方向のスクロール処理
        os_name = platform.system()
        if os_name == "Windows":
            delta = int(-1 * (event.delta / 120))
        elif os_name == "Darwin":
            delta = int(-1 * event.delta)
        else:  # Linux
            delta = int(-1 * event.delta)

        self.main_canvas.xview_scroll(delta, "units")

    def on_canvas_configure(self, event):
        # Canvasのサイズ変更時にスクロール領域を更新
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    def adjust_window_size(self):
        # ウィジェットのサイズを取得
        self.main_frame.update_idletasks()
        width = self.main_frame.winfo_width()
        height = self.main_frame.winfo_height()

        # 画面サイズを取得
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # ウィジェットが画面に収まるようにサイズを調整
        if width > screen_width:
            width = screen_width
        if height > screen_height:
            height = screen_height

        # ウィンドウサイズを設定
        self.root.geometry(f"{width}x{height}")

        # ウィンドウを中央に配置
        self.center_window(self.root)

    def create_clear_button(self, text_widget, target_widget, clear_area, button_text, position):
        clear_button = tk.Button(self.main_frame, text=button_text, command=lambda widget=target_widget, area=clear_area: widget.delete(area, tk.END), bg="#f0f0f0", font=("Arial", 12))
        clear_button.pack(in_=text_widget, side="right", anchor=position, padx=5)

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
        
        row = 0
        col = 0
        for i, (category, subcategories) in enumerate(categories.items()):
            button_color = "white"
            if category == "NSFW":
                button_color = "white"
            elif category == "Prompts" or category == "Favorites":
                button_color = "white"
            category_button = tk.Button(self.categories_frame, text=category, 
                                            command=lambda cat=category: self.show_subcategories(cat),
                                            bg=button_color, fg="black", font=("Arial", 12))
            category_button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew") # gridを使用
            self.category_buttons[category] = category_button
            col += 1
            if (i + 1) % 10 == 0: # 10個ごとに改行
                row += 1
                col = 0

        # すべての列が同じ幅になるように設定
        for i in range(10):
            self.categories_frame.columnconfigure(i, weight=1)

    def show_subcategories(self, category):
        # 選択された大項目を記憶
        self.current_category = category

        categories = load_categories()
        subcategories = categories.get(category, {})
        popup = Toplevel(self.root)
        popup.title(category)
        popup.geometry("600x400")
        # self.center_window(popup)
        self.position_window_relative_to_parent(popup, "bottom_right") # 修正
        
        item_frame = scrolledtext.ScrolledText(popup, width=60, height=15, font=("Arial", 11))
        item_frame.pack(pady=5, padx=5, fill="both", expand=True)
        item_frame.configure(state="normal")

        if category == "Prompts":
            for i, (subcategory, items) in enumerate(subcategories.items()):
                subcategory_button = tk.Button(item_frame, text=subcategory, 
                                                    command=lambda items=items, subcategory=subcategory: self.show_items(subcategory, items, popup),
                                                    bg="#9C27B0", fg="white", font=("Arial", 11))
                item_frame.window_create("end", window=subcategory_button)
                item_frame.insert("end", "\n")
        elif category == "Favorites":
            for i, (subcategory, items) in enumerate(subcategories.items()):
                subcategory_button = tk.Button(item_frame, text=subcategory, 
                                                    command=lambda items=items, subcategory=subcategory: self.show_items(subcategory, items, popup),
                                                    bg="#9C27B0", fg="white", font=("Arial", 11))
                item_frame.window_create("end", window=subcategory_button)
                item_frame.insert("end", "\n")
        else:
            for i, (subcategory, items) in enumerate(subcategories.items()):
                subcategory_button = tk.Button(item_frame, text=subcategory, 
                                                    command=lambda cat=subcategory, items=items: self.show_items(subcategory, items, popup),
                                                    bg="#9C27B0", fg="white", font=("Arial", 11))
                item_frame.window_create("end", window=subcategory_button)
                item_frame.insert("end", "\n")
        
        item_frame.configure(state="disabled")
        item_frame.bind("<MouseWheel>", lambda event: self.scroll_text(event, item_frame))

    def show_items(self, subcategory, items, popup):
        item_popup = Toplevel(self.root)
        item_popup.title(subcategory)
        item_popup.geometry("600x400")
        # self.center_window(item_popup) #削除
        self.position_window_relative_to_parent(item_popup, "bottom_right") # 修正
        item_popup.config(cursor="arrow")

        item_frame = scrolledtext.ScrolledText(item_popup, width=60, height=15, font=("Arial", 11))
        item_frame.pack(pady=5, padx=5, fill="both", expand=True)
        item_frame.configure(state="normal")
        self.item_vars = {}

        # 大項目が "Favorites" かどうかを判定
        is_favorites = self.current_category == "Favorites"

        for key, value in items.items():
            var = tk.BooleanVar()
            self.item_vars[key] = var
            if is_favorites:
                # Favoritesの場合は、キーとサブカテゴリーを使って関数を呼び出す
                check_button = tk.Checkbutton(item_frame, text=key, variable=var, bg="white", fg="black",
                                             selectcolor="white", activebackground="white", activeforeground="black",
                                             borderwidth=1, relief="solid", highlightthickness=0, font=("Arial", 11),
                                             command=lambda k=key, v=value, s=subcategory: self.add_favorite_item_to_prompt(k, v, s))
                item_frame.window_create("end", window=check_button)
                item_frame.insert("end", "\n")
            else:
                # 通常の場合は、add_item_to_prompt関数を呼び出す
                check_button = tk.Checkbutton(item_frame, text=key, variable=var, bg="white", fg="black",
                                             selectcolor="white", activebackground="white", activeforeground="black",
                                             borderwidth=1, relief="solid", highlightthickness=0, font=("Arial", 11),
                                             command=lambda en=value: self.add_item_to_prompt(en))
                item_frame.window_create("end", window=check_button)
                item_frame.insert("end", "\n")

        item_frame.configure(state="disabled")
        item_frame.bind("<MouseWheel>", lambda event: self.scroll_text(event, item_frame))

    def add_item_to_prompt(self, item_en):
        current_text = self.keyword_entry.get("1.0", tk.END).strip()
        if current_text:
            self.keyword_entry.delete("1.0", tk.END)
            self.keyword_entry.insert("1.0", f"{current_text}, {item_en}")
        else:
            self.keyword_entry.insert("1.0", item_en)

    def add_favorite_item_to_prompt(self, key, value, subcategory):
        # "Favorites" の場合、選択されたプロンプトを対応するテキストエリアに追加
        if subcategory == "Positive":
            target_text_widget = self.positive_prompt_text
        elif subcategory == "Negative":
            target_text_widget = self.negative_prompt_text
        else:
            return

        current_text = target_text_widget.get("1.0", tk.END).strip()
        prompt_text = value  # value を使用するように修正

        if current_text:
            target_text_widget.delete("1.0", tk.END)
            target_text_widget.insert("1.0", f"{current_text}\n{prompt_text}")
        else:
            target_text_widget.insert("1.0", prompt_text)


    def scroll_text(self, event, text_widget):
        text_widget.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_item_to_prompt(self, item_en):
        current_text = self.keyword_entry.get("1.0", tk.END).strip()
        if current_text:
            self.keyword_entry.delete("1.0", tk.END)
            self.keyword_entry.insert("1.0", f"{current_text}, {item_en}")
        else:
            self.keyword_entry.insert("1.0", item_en)

    def add_selected_items_to_prompt(self, popup, item_popup):
        selected_items = [item_en for item_jp, item_en in self.item_vars.items() if self.item_vars[item_en].get()]
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
        search_lower = search_term.lower()  # 検索語を小文字に変換

        for main_cat, sub_cats in all_categories.items():
            if main_cat == "Prompts":
                for sub_cat, items in sub_cats.items():
                    for item_jp, item_en in items.items():
                        if search_lower in item_jp.lower() or search_lower in item_en.lower():
                            results.append(f"{main_cat} > {sub_cat} > {item_jp}")
            elif main_cat == "Favorites":
                for sub_cat, items in sub_cats.items():
                    for key, value in items.items():  # キーと値の両方を対象に変更
                        if search_lower in key.lower() or search_lower in value.lower():
                            results.append(f"{main_cat} > {sub_cat} > {key}")
            else:
                for sub_cat, items in sub_cats.items():
                    for item_jp, item_en in items.items():
                        if search_lower in item_jp.lower() or search_lower in item_en.lower():
                            results.append(f"{main_cat} > {sub_cat} > {item_jp}")

        return results

    def show_search_results(self, search_results):
        search_popup = Toplevel(self.root)
        search_popup.title("Search Results")
        search_popup.geometry("700x300")
        # self.center_window(search_popup)
        self.position_window_relative_to_parent(search_popup, "top_right") # 修正


        item_frame = scrolledtext.ScrolledText(search_popup, width=50, height=10, font=("Arial", 11))
        item_frame.pack(pady=5, padx=5, fill="both", expand=True)
        item_frame.configure(state="normal")
        self.search_vars = {}

        if not search_results:
            item_frame.insert("end", "No results found.")
        else:
            for result in search_results:
                parts = result.split(" > ")
                if len(parts) == 3:
                    main_cat, sub_cat, item_jp = parts
                    all_categories = load_categories()
                    if main_cat in all_categories and sub_cat in all_categories[main_cat]:
                        item_en = all_categories[main_cat][sub_cat].get(item_jp)
                        if item_en:
                            var = tk.BooleanVar()
                            self.search_vars[item_en] = var
                            check_button = tk.Checkbutton(item_frame, text=result, variable=var, bg="white", fg="black",
                                                          selectcolor="white", activebackground="white", activeforeground="black",
                                                          borderwidth=1, relief="solid", highlightthickness=0, font=("Arial", 11),
                                                          command=lambda en=item_en: self.add_item_to_prompt(en))
                            item_frame.window_create("end", window=check_button)
                            item_frame.insert("end", "\n")
                        else:
                            item_frame.insert("end", f"Error: English equivalent not found for '{item_jp}'\n")
                else:
                    item_frame.insert("end", f"Invalid result format: '{result}'\n")

        item_frame.configure(state="disabled")


    def add_selected_search_results_to_prompt(self, popup):
        selected_items = [item_en for item_en, var in self.search_vars.items() if var.get()]
        current_text = self.keyword_entry.get("1.0", tk.END).strip()
        if current_text:
            new_text = f"{current_text}, {', '.join(selected_items)}"
        else:
            new_text = ', '.join(selected_items)
        self.keyword_entry.delete("1.0", tk.END)
        self.keyword_entry.insert("1.0", new_text)
        popup.destroy()

    def generate_prompt_action(self, mode="both"):
        keyword = self.keyword_entry.get("1.0", tk.END).strip()
        if not keyword:
            messagebox.showwarning("Input Error", "Please enter a keyword.")
            return

        selected_lora = self.lora_var.get() if self.lora_var.get() != "None" else ""

        if mode == "positive_only":
            # 修正: positive_prompt のみを取得し、Positive Prompt 欄にのみ追加
            positive_prompt, _ = generate_prompt(keyword, selected_lora, mode)
            self.positive_prompt_text.delete("1.0", tk.END)
            self.positive_prompt_text.insert(tk.END, positive_prompt)
        elif mode == "negative_only":
            # 修正: negative_prompt のみを取得し、Negative Prompt 欄にのみ追加
            _, negative_prompt = generate_prompt(keyword, selected_lora, mode)
            self.negative_prompt_text.delete("1.0", tk.END)
            self.negative_prompt_text.insert(tk.END, negative_prompt)
        else:
            positive_prompt, negative_prompt = generate_prompt(keyword, selected_lora, mode)
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

    def add_to_favorites(self, prompt_type, text_widget):
        prompt = text_widget.get("1.0", tk.END).strip()
        if prompt:
            key = simpledialog.askstring("Input", "Enter a key for this favorite:", parent=self.root)
            if key:
                if add_to_favorites(prompt, prompt_type, key):
                    messagebox.showinfo("Success", f"{prompt_type} prompt saved to favorites with key: {key}")
                    self.create_category_buttons()
                    
                else:
                    messagebox.showwarning("Error", f"Failed to save {prompt_type} prompt to favorites.")
        else:
            messagebox.showwarning("Input Error", f"{prompt_type} prompt is empty.")

    def remove_favorite(self, key, prompt_type):
        if remove_from_favorites(key, prompt_type):
            messagebox.showinfo("Success", f"Favorite with key '{key}' removed successfully.")
            self.create_category_buttons()
        else:
            messagebox.showerror("Error", f"Failed to remove favorite with key '{key}'.")

    def open_settings(self):
        SettingsDialog(self.root)
        self.update_ui_elements()

def create_gui():
    root = tk.Tk()
    gui = PromptCrafterGUI(root)
    root.mainloop()