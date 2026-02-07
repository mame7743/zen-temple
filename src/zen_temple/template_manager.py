"""zen-templeコンポーネントのテンプレートマネージャー"""

from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from zen_temple.logic_layer import LogicBridge, PureLogic, create_macro_helpers


class TemplateManager:
    """
    zen-templeコンポーネントのためのJinja2テンプレート管理

    zen-temple哲学に従います:
    - テンプレートが真実の源
    - ビルドステップ不要
    - クリアで透明なレンダリング
    - ロジックは純粋、ブリッジは最小限（LogicBridge経由）
    """

    def __init__(
        self, template_dirs: Optional[list[Path]] = None, logic_bridge: Optional[LogicBridge] = None
    ):
        """
        テンプレートマネージャーを初期化

        引数:
            template_dirs: テンプレートを検索するディレクトリのリスト
            logic_bridge: 純粋ロジックをテンプレートに接続するためのオプションロジックブリッジ
        """
        if template_dirs is None:
            template_dirs = [Path.cwd() / "templates"]

        self.template_dirs = [Path(d) for d in template_dirs]
        self.logic_bridge = logic_bridge or LogicBridge()
        self._setup_environment()

    def _setup_environment(self) -> None:
        """適切な設定でJinja2環境をセットアップ"""
        loader = FileSystemLoader([str(d) for d in self.template_dirs])
        self.env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # zen-temple用のカスタムフィルターを追加
        self.env.filters["json_encode"] = self._json_encode_filter

        # グローバルにマクロヘルパーを追加（ロジックとテンプレート間のブリッジ）
        macro_helpers = create_macro_helpers()
        self.env.globals.update(macro_helpers)

    @staticmethod
    def _json_encode_filter(value: Any) -> str:
        """Alpine.js用に値を安全にJSONとしてエンコードするフィルター"""
        import json

        from markupsafe import Markup

        return Markup(json.dumps(value))

    def render_component(
        self,
        component_name: str,
        context: Optional[dict[str, Any]] = None,
        logic: Optional[PureLogic] = None,
        **kwargs: Any,
    ) -> str:
        """
        コンポーネントテンプレートをレンダリング

        引数:
            component_name: コンポーネントテンプレートの名前
            context: レンダリング用のコンテキスト辞書
            logic: オプションの純粋ロジックインスタンス（「ロジックは純粋」原則に従う）
            **kwargs: 追加のコンテキスト変数

        戻り値:
            レンダリングされたHTML文字列
        """
        if context is None:
            context = {}

        # ロジックが提供されている場合、それからコンテキストを準備（最小限のブリッジ）
        if logic is not None:
            logic_context = self.logic_bridge.prepare_context(logic, extra_context=context)
            context = logic_context

        context.update(kwargs)

        template = self.env.get_template(f"{component_name}.html")
        return template.render(**context)

    def render_string(self, template_string: str, context: Optional[dict[str, Any]] = None) -> str:
        """
        文字列からテンプレートをレンダリング

        引数:
            template_string: レンダリングするテンプレート文字列
            context: レンダリング用のコンテキスト辞書

        戻り値:
            レンダリングされたHTML文字列
        """
        if context is None:
            context = {}
        template = self.env.from_string(template_string)
        return template.render(**context)

    def add_template_dir(self, template_dir: Path) -> None:
        """
        新しいテンプレートディレクトリを検索パスに追加

        引数:
            template_dir: テンプレートディレクトリへのパス
        """
        if template_dir not in self.template_dirs:
            self.template_dirs.append(Path(template_dir))
            self._setup_environment()

    def list_components(self) -> list[str]:
        """
        利用可能な全コンポーネントテンプレートを一覧表示

        戻り値:
            コンポーネント名のリスト（.html拡張子なし）
        """
        components = []
        for template_dir in self.template_dirs:
            if template_dir.exists():
                for file in template_dir.glob("*.html"):
                    component_name = file.stem
                    if component_name not in components:
                        components.append(component_name)
        return sorted(components)

    def component_exists(self, component_name: str) -> bool:
        """
        コンポーネントテンプレートが存在するかチェック

        引数:
            component_name: コンポーネントの名前

        戻り値:
            コンポーネントが存在する場合はTrue、そうでない場合はFalse
        """
        try:
            self.env.get_template(f"{component_name}.html")
            return True
        except Exception:
            return False
