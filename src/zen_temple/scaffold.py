"""zen-templeプロジェクトのスキャフォールドジェネレータ"""

import re
from pathlib import Path
from typing import Optional

import yaml


class ScaffoldGenerator:
    """
    zen-templeアプリケーション用のプロジェクトスキャフォールドを生成

    作成するもの:
    - プロジェクト構造
    - 設定ファイル
    - サンプルコンポーネント
    - ベーステンプレート
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        スキャフォールドジェネレータを初期化

        引数:
            project_root: プロジェクトのルートディレクトリ（デフォルトはcwd）
        """
        self.project_root = project_root or Path.cwd()

    def _to_class_name(self, component_name: str) -> str:
        """コンポーネント名をPascalCaseのクラス名に変換（例: my_widget → MyWidgetState）"""
        parts = [p for p in re.split(r"[-_]", component_name) if p]
        return "".join(part.capitalize() for part in parts) + "State"

    def generate_project(
        self, project_name: str, include_examples: bool = True, include_server: bool = False
    ) -> dict[str, Path]:
        """
        完全なプロジェクト構造を生成

        引数:
            project_name: プロジェクトの名前
            include_examples: サンプルコンポーネントを含めるか
            include_server: 基本的なFlaskサーバーを含めるか

        戻り値:
            構造名と作成されたパスをマッピングする辞書
        """
        project_path = self.project_root / project_name
        created_paths = {}

        # ディレクトリ構造を作成
        directories = [
            project_path / "templates",
            project_path / "templates/components",
            project_path / "templates/layouts",
            project_path / "static",
            project_path / "static/css",
            project_path / "static/js",
        ]

        if include_server:
            directories.extend(
                [
                    project_path / "app",
                    project_path / "app/routes",
                ]
            )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            created_paths[str(directory.relative_to(project_path))] = directory

        # 設定ファイルを生成
        config_file = self._create_config_file(project_path, project_name)
        created_paths["zen-temple.yaml"] = config_file

        # ベースレイアウトを生成
        base_layout = self._create_base_layout(project_path)
        created_paths["templates/layouts/base.html"] = base_layout

        # リクエストされた場合はサンプルコンポーネントを生成
        if include_examples:
            example_paths = self._create_example_components(project_path)
            created_paths.update(example_paths)

        # リクエストされた場合はサーバーファイルを生成
        if include_server:
            server_paths = self._create_server_files(project_path, project_name)
            created_paths.update(server_paths)

        # READMEを作成
        readme = self._create_readme(project_path, project_name, include_server)
        created_paths["README.md"] = readme

        return created_paths

    def generate_component(
        self, component_name: str, component_type: str = "basic", output_dir: Optional[Path] = None
    ) -> Path:
        """
        コンポーネントテンプレートを生成

        引数:
            component_name: コンポーネントの名前
            component_type: コンポーネントのタイプ（basic、form、list、card）
            output_dir: コンポーネントを作成するディレクトリ

        戻り値:
            作成されたコンポーネントファイルへのパス
        """
        if output_dir is None:
            output_dir = self.project_root / "templates/components"

        output_dir.mkdir(parents=True, exist_ok=True)
        component_path = output_dir / f"{component_name}.html"

        template_content = self._get_component_template(component_name, component_type)
        component_path.write_text(template_content)

        return component_path

    def _create_config_file(self, project_path: Path, project_name: str) -> Path:
        """zen-temple設定ファイルを作成"""
        config = {
            "project": {
                "name": project_name,
                "version": "0.1.0",
            },
            "templates": {
                "directories": ["templates", "templates/components", "templates/layouts"],
            },
            "cdn": {
                "htmx": "https://unpkg.com/htmx.org@1.9.10",
                "alpine": "https://unpkg.com/alpinejs@3.13.5/dist/cdn.min.js",
                "tailwind": "https://cdn.tailwindcss.com",
            },
            "zen_temple": {
                "philosophy": [
                    "No build step required",
                    "No hidden abstractions",
                    "Template-centered design",
                    "Logic in Alpine.js x-data only",
                    "Server returns JSON only",
                    "HTMX for communication and events only",
                ]
            },
        }

        config_path = project_path / "zen-temple.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return config_path

    def _create_base_layout(self, project_path: Path) -> Path:
        """HTMX、Alpine.js、Tailwindを含むベースHTMLレイアウトを作成"""
        layout_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}zen-temple App{% endblock %}</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.13.5/dist/cdn.min.js"></script>

    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Main container -->
    <div class="container mx-auto px-4 py-8">
        {% block content %}
        <!-- Page content goes here -->
        {% endblock %}
    </div>

    {% block extra_body %}{% endblock %}
</body>
</html>
"""
        layout_path = project_path / "templates/layouts/base.html"
        layout_path.parent.mkdir(parents=True, exist_ok=True)
        layout_path.write_text(layout_content)
        return layout_path

    def _create_example_components(self, project_path: Path) -> dict[str, Path]:
        """zen-temple哲学を示すサンプルコンポーネントを作成"""
        components = {}

        # カウンターコンポーネント（Alpine.jsクラスベース状態管理の例）
        counter_content = """{%- macro counter(initial_count=0) -%}
<!-- カウンターコンポーネント - クラスベース状態管理のデモ -->
<div
    x-data="new CounterState({{ initial_count }})"
    class="bg-white rounded-lg shadow-md p-6 max-w-md"
>
    <h3 class="text-xl font-semibold mb-4">カウンター</h3>

    <div class="flex items-center justify-between mb-4">
        <button
            @click="decrement()"
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
            -
        </button>

        <span class="text-3xl font-bold" x-text="count"></span>

        <button
            @click="increment()"
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
            +
        </button>
    </div>

    <p class="text-center text-gray-500">2倍: <span x-text="double"></span></p>
</div>

<script>
class CounterState {
    constructor(initialCount = 0) {
        this.count = initialCount;
    }

    increment() {
        this.count++;
    }

    decrement() {
        this.count--;
    }

    // 算出プロパティ: Alpine.jsで自動的にリアクティブになる
    get double() {
        return this.count * 2;
    }
}
</script>
{%- endmacro -%}
"""
        counter_path = project_path / "templates/components/counter.html"
        counter_path.write_text(counter_content)
        components["templates/components/counter.html"] = counter_path

        # Todoリストコンポーネント（バックエンド主導の更新パターンの例）
        todo_content = """{%- macro todo() -%}
<!-- Todoリストコンポーネント - バックエンド主導の単一方向データフローのデモ -->
<div
    x-data="new TodoState()"
    x-init="init()"
    class="bg-white rounded-lg shadow-md p-6 max-w-2xl"
>
    <h3 class="text-xl font-semibold mb-4">Todoリスト</h3>

    <!-- Todo追加フォーム（UI状態: newTodoText） -->
    <div class="flex gap-2 mb-4">
        <input
            type="text"
            x-model="newTodoText"
            @keyup.enter="addTodo()"
            placeholder="新しいTodoを追加..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded"
        />
        <button
            @click="addTodo()"
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
        >
            追加
        </button>
    </div>

    <!-- Todoリスト（サーバー状態: todos） -->
    <ul class="space-y-2">
        <template x-for="todo in todos" :key="todo.id">
            <li class="flex items-center gap-2 p-3 bg-gray-50 rounded">
                <input
                    type="checkbox"
                    :checked="todo.completed"
                    @change="toggleTodo(todo.id)"
                    class="w-5 h-5 text-blue-500"
                />
                <span
                    x-text="todo.text"
                    :class="{ 'line-through text-gray-400': todo.completed }"
                    class="flex-1"
                ></span>
                <button
                    @click="removeTodo(todo.id)"
                    class="text-red-500 hover:text-red-700"
                >
                    削除
                </button>
            </li>
        </template>
    </ul>

    <div x-show="todos.length === 0" class="text-center text-gray-400 py-8">
        まだTodoがありません。上で追加してください！
    </div>

    <p class="mt-4 text-sm text-gray-500">
        完了: <span x-text="completedCount"></span> / <span x-text="todos.length"></span>
    </p>
</div>

<script>
class TodoState {
    constructor() {
        // サーバー状態（APIから取得、直接書き換え禁止）
        this.todos = [];
        // UI状態（入力フォーム用）
        this.newTodoText = '';
    }

    async init() {
        await this.fetchTodos();
    }

    // バックエンドから最新データを取得して丸ごと再代入
    async fetchTodos() {
        const response = await fetch('/api/todos');
        const data = await response.json();
        this.todos = data.todos;
    }

    async addTodo() {
        if (!this.newTodoText.trim()) return;
        await fetch('/api/todos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: this.newTodoText }),
        });
        this.newTodoText = '';
        // 成功後はバックエンドから最新データを再取得
        await this.fetchTodos();
    }

    async toggleTodo(id) {
        await fetch(`/api/todos/${id}/toggle`, { method: 'POST' });
        await this.fetchTodos();
    }

    async removeTodo(id) {
        await fetch(`/api/todos/${id}`, { method: 'DELETE' });
        await this.fetchTodos();
    }

    // 算出プロパティ
    get completedCount() {
        return this.todos.filter(t => t.completed).length;
    }
}
</script>
{%- endmacro -%}
"""
        todo_path = project_path / "templates/components/todo.html"
        todo_path.write_text(todo_content)
        components["templates/components/todo.html"] = todo_path

        # データフェッチコンポーネント（明示的なfetchフローの例）
        fetch_content = """{%- macro data_fetch() -%}
<!-- データフェッチコンポーネント - 明示的なAPI通信フローのデモ -->
<div
    x-data="new DataFetchState()"
    class="bg-white rounded-lg shadow-md p-6 max-w-2xl"
>
    <h3 class="text-xl font-semibold mb-4">データフェッチャー</h3>

    <button
        @click="loadData()"
        :disabled="isLoading"
        class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-6 py-2 rounded mb-4"
    >
        <span x-show="!isLoading">データを読み込む</span>
        <span x-show="isLoading">読み込み中...</span>
    </button>

    <ul class="space-y-2">
        <template x-for="item in items" :key="item.id">
            <li class="p-3 bg-gray-50 rounded border">
                <strong x-text="item.title"></strong>: <span x-text="item.description"></span>
            </li>
        </template>
    </ul>

    <div x-show="items.length === 0 && !isLoading" class="text-center text-gray-400 py-8">
        ボタンをクリックしてサーバーからデータを読み込みます。
    </div>
</div>

<script>
class DataFetchState {
    constructor() {
        // サーバー状態（APIから取得、直接書き換え禁止）
        this.items = [];
        // UI状態
        this.isLoading = false;
    }

    // 明示的なfetchフロー: APIを叩き、成功したらバックエンドから最新データで上書き
    async loadData() {
        this.isLoading = true;
        const response = await fetch('/api/data');
        const data = await response.json();
        this.items = data.items;
        this.isLoading = false;
    }
}
</script>
{%- endmacro -%}
"""
        fetch_path = project_path / "templates/components/data_fetch.html"
        fetch_path.write_text(fetch_content)
        components["templates/components/data_fetch.html"] = fetch_path

        # サンプルインデックスページ
        index_content = """{% extends "layouts/base.html" %}
{% from "components/counter.html" import counter %}
{% from "components/todo.html" import todo %}
{% from "components/data_fetch.html" import data_fetch %}

{% block title %}zen-temple サンプル{% endblock %}

{% block content %}
<div class="space-y-8">
    <header class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">zen-temple</h1>
        <p class="text-lg text-gray-600">ゼロビルド、マジックなしのフロントエンドコンポーネント</p>
    </header>

    <section class="space-y-6">
        <h2 class="text-2xl font-semibold text-gray-700">サンプルコンポーネント</h2>

        <div class="grid md:grid-cols-2 gap-6">
            <div>
                {{ counter(initial_count=0) }}
            </div>

            <div>
                {{ data_fetch() }}
            </div>
        </div>

        <div>
            {{ todo() }}
        </div>
    </section>

    <footer class="text-center text-gray-500 mt-12 pt-8 border-t">
        <p>Alpine.js、Jinja2、Tailwind CSSで構築</p>
        <p class="text-sm mt-2">ビルドステップなし • 隠されたマジックなし • テンプレート中心</p>
    </footer>
</div>
{% endblock %}
"""
        index_path = project_path / "templates/index.html"
        index_path.write_text(index_content)
        components["templates/index.html"] = index_path

        return components

    def _create_server_files(self, project_path: Path, project_name: str) -> dict[str, Path]:
        """基本的なFlaskサーバーファイルを作成"""
        files = {}

        # メインアプリファイル
        app_content = f'''"""
{project_name}のメインアプリケーションエントリーポイント
"""

from flask import Flask, render_template, jsonify
from pathlib import Path

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


@app.route('/')
def index():
    """メインページをレンダリング"""
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    """
    JSONデータを返すサンプルAPIエンドポイント

    ZEN哲学【N】Neutral Backend に従う:
    - サーバーは純粋なJSON APIとして機能
    - UIに依存しない汎用的なデータを返す
    - Alpine.jsクラスがJSONを受け取り状態を更新
    """
    items = [
        {{'id': 1, 'title': '項目1', 'description': 'サーバーから読み込まれたデータ'}},
        {{'id': 2, 'title': '項目2', 'description': 'Alpine.jsクラスがJSONを処理'}},
        {{'id': 3, 'title': '項目3', 'description': 'バックエンドはUIに依存しない'}},
    ]
    return jsonify({{'items': items}})


@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Todoリストを返す"""
    todos = [
        {{'id': 1, 'text': 'zen-templeを学ぶ', 'completed': False}},
        {{'id': 2, 'text': 'アプリを作る', 'completed': False}},
    ]
    return jsonify({{'todos': todos}})


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """新しいTodoを作成して最新リストを返す"""
    from flask import request
    data = request.get_json()
    # TODO: データベースに保存
    return jsonify({{'status': 'created', 'text': data.get('text')}})


@app.route('/api/todos/<int:todo_id>/toggle', methods=['POST'])
def toggle_todo(todo_id: int):
    """Todoの完了状態をトグル"""
    # TODO: データベースで更新
    return jsonify({{'status': 'toggled', 'id': todo_id}})


@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id: int):
    """Todoを削除"""
    # TODO: データベースから削除
    return jsonify({{'status': 'deleted', 'id': todo_id}})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

        app_path = project_path / "app/main.py"
        app_path.write_text(app_content)
        files["app/main.py"] = app_path

        # .envファイル
        env_content = """# Flask設定
FLASK_APP=app/main.py
FLASK_ENV=development
FLASK_DEBUG=1
"""
        env_path = project_path / ".env"
        env_path.write_text(env_content)
        files[".env"] = env_path

        # requirementsファイル
        requirements_content = """flask>=3.0.0
python-dotenv>=1.0.0
jinja2>=3.1.0
"""
        req_path = project_path / "requirements.txt"
        req_path.write_text(requirements_content)
        files["requirements.txt"] = req_path

        return files

    def _create_readme(self, project_path: Path, project_name: str, include_server: bool) -> Path:
        """プロジェクトREADMEを作成"""
        server_section = ""
        if include_server:
            server_section = """
## 開発サーバーの起動

```bash
# 依存関係をインストール
pip install -r requirements.txt

# サーバーを起動
python app/main.py
```

その後、ブラウザで http://localhost:5000 を開きます。
"""

        readme_content = f"""# {project_name}

zen-templeプロジェクト - ゼロビルド、マジックなしのフロントエンドコンポーネント

## 哲学

このプロジェクトはzen-temple哲学に従います:

- **ビルドステップ不要**: テンプレートを編集して即座に変更を確認
- **隠された抽象化なし**: 見たものがそのまま得られる
- **テンプレート中心設計**: テンプレートが真実の源
- **Alpine.jsでのロジック**: x-data関数での状態管理
- **サーバーはJSON/HTMLを返す**: 関心の明確な分離
- **通信にはHTMX**: シンプルで宣言的なAPI呼び出し

## プロジェクト構造

```
{project_name}/
├── templates/
│   ├── layouts/
│   │   └── base.html          # CDNインポート付きベースレイアウト
│   ├── components/
│   │   ├── counter.html       # 例: Alpine.jsリアクティビティ
│   │   ├── todo.html          # 例: 状態管理
│   │   └── data_fetch.html    # 例: HTMX通信
│   └── index.html             # メインページ
├── static/
│   ├── css/                   # カスタムスタイル（必要に応じて）
│   └── js/                    # カスタムAlpine.jsストア（必要に応じて）
{"├── app/" if include_server else ""}
{"│   └── main.py               # Flaskアプリケーション" if include_server else ""}
└── zen-temple.yaml            # プロジェクト設定
```
{server_section}
## 技術スタック

- **HTMX**: AJAX、WebSocket、Server-Sent Events用
- **Alpine.js**: リアクティブで宣言的なJavaScript
- **Jinja2**: テンプレートレンダリング
- **Tailwind CSS**: スタイリング（CDN経由）

## コンポーネントの作成

コンポーネントはインタラクティビティ用のAlpine.jsを使用したシンプルなHTMLファイルです:

```html
<div x-data="{{ count: 0 }}">
    <button @click="count++">インクリメント</button>
    <span x-text="count"></span>
</div>
```

## HTMX統合

サーバー通信にHTMXを使用:

```html
<button
    hx-get="/api/data"
    hx-target="#result"
    hx-swap="innerHTML"
>
    データを読み込む
</button>
<div id="result"></div>
```

## 詳細情報

- [HTMXドキュメント](https://htmx.org/)
- [Alpine.jsドキュメント](https://alpinejs.dev/)
- [Jinja2ドキュメント](https://jinja.palletsprojects.com/)
- [Tailwind CSSドキュメント](https://tailwindcss.com/)
"""
        readme_path = project_path / "README.md"
        readme_path.write_text(readme_content)
        return readme_path

    def _get_component_template(self, component_name: str, component_type: str) -> str:
        """コンポーネントタイプ用のテンプレート内容を取得"""
        class_name = self._to_class_name(component_name)
        templates = {
            "basic": (
                "{%- macro __NAME__() -%}\n"
                "<!-- __NAME__コンポーネント -->\n"
                "<div\n"
                '    x-data="new __CLSNAME__()"\n'
                '    class="bg-white rounded-lg shadow-md p-6"\n'
                ">\n"
                '    <h3 class="text-xl font-semibold mb-4">__NAME__</h3>\n'
                "    <p x-text=\"message\"></p>\n"
                "</div>\n"
                "\n"
                "<script>\n"
                "class __CLSNAME__ {\n"
                "    constructor() {\n"
                "        this.message = '__NAME__からこんにちは！';\n"
                "    }\n"
                "}\n"
                "</script>\n"
                "{%- endmacro -%}\n"
            ),
            "form": (
                "{%- macro __NAME__() -%}\n"
                "<!-- __NAME__フォームコンポーネント -->\n"
                "<div\n"
                '    x-data="new __CLSNAME__()"\n'
                '    class="bg-white rounded-lg shadow-md p-6"\n'
                ">\n"
                '    <h3 class="text-xl font-semibold mb-4">__NAME__</h3>\n'
                "\n"
                '    <form @submit.prevent="submit()" class="space-y-4">\n'
                "        <div>\n"
                '            <label class="block text-sm font-medium text-gray-700 mb-2">\n'
                "                フィールド名\n"
                "            </label>\n"
                "            <input\n"
                '                type="text"\n'
                '                x-model="fieldValue"\n'
                '                class="w-full px-4 py-2 border border-gray-300 rounded'
                ' focus:outline-none focus:ring-2 focus:ring-blue-500"\n'
                "            />\n"
                "        </div>\n"
                "\n"
                "        <button\n"
                '            type="submit"\n'
                '            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"\n'
                "        >\n"
                "            送信\n"
                "        </button>\n"
                "    </form>\n"
                "</div>\n"
                "\n"
                "<script>\n"
                "class __CLSNAME__ {\n"
                "    constructor() {\n"
                "        // UI状態（入力フォーム用）\n"
                "        this.fieldValue = '';\n"
                "    }\n"
                "\n"
                "    async submit() {\n"
                "        const response = await fetch('/api/__NAME__', {\n"
                "            method: 'POST',\n"
                "            headers: { 'Content-Type': 'application/json' },\n"
                "            body: JSON.stringify({ field: this.fieldValue }),\n"
                "        });\n"
                "        const data = await response.json();\n"
                "        // 成功後の処理\n"
                "        this.fieldValue = '';\n"
                "    }\n"
                "}\n"
                "</script>\n"
                "{%- endmacro -%}\n"
            ),
            "list": (
                "{%- macro __NAME__() -%}\n"
                "<!-- __NAME__リストコンポーネント -->\n"
                "<div\n"
                '    x-data="new __CLSNAME__()"\n'
                '    x-init="init()"\n'
                '    class="bg-white rounded-lg shadow-md p-6"\n'
                ">\n"
                '    <h3 class="text-xl font-semibold mb-4">__NAME__</h3>\n'
                "\n"
                '    <ul class="space-y-2">\n'
                '        <template x-for="item in items" :key="item.id">\n'
                '            <li class="p-3 bg-gray-50 rounded">\n'
                '                <span x-text="item.name"></span>\n'
                "            </li>\n"
                "        </template>\n"
                "    </ul>\n"
                "\n"
                '    <div x-show="items.length === 0" class="text-center text-gray-400 py-8">\n'
                "        項目が見つかりませんでした。\n"
                "    </div>\n"
                "</div>\n"
                "\n"
                "<script>\n"
                "class __CLSNAME__ {\n"
                "    constructor() {\n"
                "        // サーバー状態（APIから取得、直接書き換え禁止）\n"
                "        this.items = [];\n"
                "    }\n"
                "\n"
                "    async init() {\n"
                "        await this.fetchItems();\n"
                "    }\n"
                "\n"
                "    // バックエンドから最新データを取得して丸ごと再代入\n"
                "    async fetchItems() {\n"
                "        const response = await fetch('/api/__NAME__');\n"
                "        const data = await response.json();\n"
                "        this.items = data.items;\n"
                "    }\n"
                "}\n"
                "</script>\n"
                "{%- endmacro -%}\n"
            ),
            "card": (
                '{%- macro __NAME__(title="__NAME__", description="") -%}\n'
                "<!-- __NAME__カードコンポーネント -->\n"
                '<div class="bg-white rounded-lg shadow-md overflow-hidden">\n'
                '    <div class="p-6">\n'
                '        <h3 class="text-xl font-semibold mb-2">{{ title }}</h3>\n'
                '        <p class="text-gray-600 mb-4">\n'
                "            {{ description or '__NAME__の説明をここに記述します。' }}\n"
                "        </p>\n"
                "\n"
                '        <button class="bg-blue-500 hover:bg-blue-600'
                ' text-white px-4 py-2 rounded">\n'
                "            アクション\n"
                "        </button>\n"
                "    </div>\n"
                "</div>\n"
                "{%- endmacro -%}\n"
            ),
        }

        template = templates.get(component_type, templates["basic"])
        return template.replace("__NAME__", component_name).replace("__CLSNAME__", class_name)
