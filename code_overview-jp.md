# **各ファイルのコードの概要**

## **`app/__init__.py`**
*  **概要**
    * このファイルはPythonのパッケージ初期化ファイルです。通常は空ですが、必要に応じてパッケージレベルの初期化コードを含めることができます。
*   **コードの解説**
    *   このファイルは、`app`ディレクトリをPythonのパッケージとして認識させるための空のファイルです。


## **`app/gui.py`**
*   **概要**
    * このファイルは、アプリケーションのGUI（グラフィカルユーザーインターフェース）を定義するファイルです。Tkinter ライブラリを使用して、ウィンドウ、ボタン、テキスト入力欄などのUI要素を作成し、ユーザーとのインタラクションを管理します。
*   **コードの解説**
    *   **`SettingsDialog` クラス:** 設定画面のダイアログを定義します。プロンプトテンプレート、モデル名、AI生成モード、LoRAモデルなどの設定を変更できます。
    *   **`PromptCrafterGUI` クラス:** メインウィンドウとそのウィジェットを定義します。キーワード入力、プロンプト表示、LoRA選択、カテゴリ選択、検索、各種ボタンなど、アプリケーションの主要なUI要素を管理します。
    *   **イベントハンドラ:** 各ボタンがクリックされた時の処理を定義します。例えば、`generate_prompt_action()` はプロンプトを生成し表示、`copy_positive_prompt()` や `copy_negative_prompt()` はクリップボードにコピー、`open_settings()` は設定画面を開くなどの処理を行います。
    *   **`create_gui()` 関数:** アプリケーションのメインウィンドウを生成し、Tkinterのmainloopを開始します。


## **`app/prompt_generator.py`**

*   **概要**
    * このファイルは、AIモデルを使用したプロンプト生成のロジックを定義します。Hugging Face の `transformers` ライブラリを利用して、テキスト生成モデルをロードし、プロンプトの生成を行います。
*   **コードの解説**
    *   **グローバル変数 `generator`:** プロンプト生成に使用するAIモデルを格納します。モデルは `config.py` で設定されたモデル名に基づき、初期化時にロードされます。
    *   **`generate_prompt(keyword, lora_name)` 関数:** キーワードと選択されたLoRAモデル名を受け取り、`_generate_model_prompt` または `_generate_template_prompt` 関数を呼び出して、ポジティブとネガティブの両方のプロンプトを生成します。
    *   **`_generate_model_prompt(keyword, prompt_type)` 関数:** AIモデルを利用してプロンプトを生成する処理を記述します。モデルがロードできていない場合は、エラーメッセージを返します。
    *   **`_generate_template_prompt(keyword, prompt_type)` 関数:** テンプレートベースでプロンプトを生成する処理を記述します。`config.py` で設定されたテンプレートを使用します。


## **`app/config.py`**

*   **概要**
    * このファイルは、アプリケーションの設定を定義し、設定ファイル (`app_settings.json`, `categories.json`) の読み込みと保存を管理します。
*   **コードの解説**
    *   **`DEFAULT_APP_SETTINGS`:** アプリケーションのデフォルト設定を定義します。プロンプトテンプレート、モデル名、AI生成モード、LoRAリストなどを含みます。
    *   **`APP_SETTINGS`:** アプリケーションの実行中に使用される設定を格納するグローバル変数です。
    *   **`SETTINGS_FILE` と `CATEGORIES_FILE`:** 設定ファイルとカテゴリファイルのファイル名を定義します。
    *   **`load_settings(file_path=None)` 関数:** 指定されたJSONファイル（またはデフォルトの `app_settings.json` ）からアプリケーションの設定を読み込みます。ファイルがない場合は、デフォルト設定を適用し、ファイルを作成します。
    *  **`save_settings(file_path=None)` 関数:** 現在のアプリケーション設定をJSONファイルに保存します。
    *   **`load_categories(file_path=None)` 関数:** 指定された JSON ファイル（またはデフォルトの `categories.json` ）からカテゴリ情報を読み込みます。ファイルがない場合は、デフォルトカテゴリを作成し、ファイルを作成します。
     * **`save_categories(file_path=None)` 関数**: 現在のカテゴリ情報をJSONファイルに保存します。
     * **`add_prompts_from_csv(file_path)` 関数:** 指定された CSV ファイルを読み込み、カテゴリとプロンプトを追加します。


## **`categories.json`**

*   **概要**
    * このファイルは、プロンプトを生成するためのキーワードカテゴリを階層構造で定義します。大分類、中分類、小分類で構成され、GUI上のキーワード選択や検索で使用されます。
*   **コードの解説**
    *   `Nature`, `People`, `Buildings & Structures`, `Art`, `Concept`, `Fantasy`, `Cyberpunk`, `Steampunk`, `Retro`, `Pop Culture`, `NSFW`, `Prompts` の各カテゴリが定義され、それぞれのカテゴリに紐づいたキーワードのリストが記述されます。