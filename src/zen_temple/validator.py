"""zen-templeのコンポーネントバリデータ"""

import re
from pathlib import Path

from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """コンポーネント検証の結果"""

    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    component_name: str

    def add_error(self, message: str) -> None:
        """エラーメッセージを追加"""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """警告メッセージを追加"""
        self.warnings.append(message)


class ComponentValidator:
    """
    zen-templeコンポーネントの構造と設計哲学への準拠を検証

    検証項目:
    - HTML内のインラインJavaScriptなし（代わりにAlpine.js x-dataを使用）
    - HTMX属性の適切な使用
    - Alpine.jsリアクティブパターン
    - テンプレート構造
    """

    def __init__(self):
        """バリデータを初期化"""
        self.rules = [
            self._check_inline_scripts,
            self._check_htmx_usage,
            self._check_alpine_usage,
            self._check_template_structure,
            self._check_macro_wrapper,
            self._check_server_state_mutation,
        ]

    def validate_component(self, component_path: Path) -> ValidationResult:
        """
        コンポーネントファイルを検証

        引数:
            component_path: コンポーネントHTMLファイルへのパス

        戻り値:
            エラーと警告を含むValidationResult
        """
        result = ValidationResult(is_valid=True, component_name=component_path.stem)

        if not component_path.exists():
            result.add_error(f"コンポーネントファイルが見つかりません: {component_path}")
            return result

        content = component_path.read_text()

        # 全ての検証ルールを実行
        for rule in self.rules:
            rule(content, result)

        return result

    def validate_string(self, content: str, component_name: str = "inline") -> ValidationResult:
        """
        文字列からコンポーネント内容を検証

        引数:
            content: 検証するHTML内容
            component_name: コンポーネントの名前（エラーメッセージ用）

        戻り値:
            エラーと警告を含むValidationResult
        """
        result = ValidationResult(is_valid=True, component_name=component_name)

        for rule in self.rules:
            rule(content, result)

        return result

    def _check_inline_scripts(self, content: str, result: ValidationResult) -> None:
        """インラインスクリプトをチェック（zen-temple哲学に違反）"""
        # CDNインクルードではない<script>タグを探す
        # ホワイトスペースと閉じタグの属性を処理するより堅牢な正規表現を使用
        # パターンの説明:
        # - <script(?![^>]*src=) : src=属性がない<scriptにマッチ
        # - [^>]*> : >まで任意の属性にマッチ
        # - [\s\S]*? : 内容にマッチ（改行を含む）非貪欲
        # - </\s*script[^>]*> : オプションのホワイトスペースと属性を持つ閉じタグにマッチ
        script_pattern = r"<script(?![^>]*src=)[^>]*>[\s\S]*?</\s*script[^>]*>"
        matches = re.finditer(script_pattern, content, re.IGNORECASE)

        for match in matches:
            script_content = match.group(0)
            # Alpine.jsのインライン初期化、HTMX拡張、またはSFCスタイルのクラス定義を許可
            if (
                "x-data" not in script_content
                and "htmx" not in script_content.lower()
                and "class " not in script_content
            ):
                result.add_error(
                    "インラインスクリプトが検出されました。ロジックをAlpine.js x-data関数に移動してください。"
                )

        # インラインイベントハンドラーをチェック
        inline_handlers = [
            r"onclick\s*=",
            r"onload\s*=",
            r"onchange\s*=",
            r"onsubmit\s*=",
        ]
        for pattern in inline_handlers:
            if re.search(pattern, content, re.IGNORECASE):
                result.add_error(
                    f"インラインイベントハンドラーが検出されました（{pattern}）。Alpine.jsの@click、@changeなどを使用してください。"
                )

    def _check_htmx_usage(self, content: str, result: ValidationResult) -> None:
        """HTMXの適切な使用をチェック"""
        # HTMX属性を探す
        htmx_attrs = [
            "hx-get",
            "hx-post",
            "hx-put",
            "hx-delete",
            "hx-patch",
            "hx-trigger",
            "hx-target",
            "hx-swap",
            "hx-select",
        ]

        has_htmx = any(attr in content for attr in htmx_attrs)

        if has_htmx:
            # レスポンスがJSON/HTMLフラグメントであることを期待し、フルページではないことをチェック
            if "hx-swap" in content:
                # フルドキュメントを置き換える可能性がある場合に警告
                if re.search(r'hx-swap\s*=\s*["\']outerHTML["\']', content):
                    result.add_warning(
                        "フルドキュメントでhx-swap='outerHTML'を使用しています。"
                        "サーバーがHTMLフラグメントを返すことを確認してください、フルページではありません。"
                    )

    def _check_alpine_usage(self, content: str, result: ValidationResult) -> None:
        """Alpine.jsの適切な使用をチェック"""
        # x-data（状態管理）をチェック
        if "x-data" in content:
            # x-dataが適切に使用されていることを確認
            x_data_pattern = r'x-data\s*=\s*["\']([^"\']*)["\']'
            matches = re.finditer(x_data_pattern, content)

            for match in matches:
                data_content = match.group(1)
                # 関数呼び出しまたはオブジェクトのように見えるかチェック
                if data_content and not ("{" in data_content or "(" in data_content):
                    result.add_warning(
                        f"x-data='{data_content}'は関数呼び出しまたはオブジェクトリテラルである必要があります"
                    )
                # ZEN哲学: インラインオブジェクトではなくクラスベースの状態管理を推奨
                if data_content and data_content.strip().startswith("{") and "new " not in data_content:
                    result.add_warning(
                        "x-dataにインラインオブジェクトが使用されています。"
                        "'new ClassName()' 形式のクラスベースの状態管理を使用してください。"
                        "例: x-data=\"new ComponentState()\""
                    )

        # Alpineディレクティブをチェック
        alpine_directives = ["x-show", "x-if", "x-for", "x-model", "x-text", "x-html"]
        has_alpine = any(directive in content for directive in alpine_directives)

        if not has_alpine and "x-data" not in content:
            result.add_warning(
                "Alpine.jsディレクティブが見つかりませんでした。リアクティブな動作にAlpine.jsの使用を検討してください。"
            )

    def _check_template_structure(self, content: str, result: ValidationResult) -> None:
        """基本的なテンプレート構造をチェック"""
        # Jinja2ブロックまたはインクルードをチェック
        if "{% block" in content or "{% extends" in content or "{% include" in content:
            # これは良い - Jinja2テンプレート継承を使用
            pass
        else:
            # スタンドアロンコンポーネント - 何らかの構造を持つべき
            if "<html" in content.lower() and "</html>" in content.lower():
                result.add_warning(
                    "コンポーネントがフルHTMLドキュメントを含んでいます。"
                    "再利用可能なコンポーネントフラグメントに分割することを検討してください。"
                )

    def _check_macro_wrapper(self, content: str, result: ValidationResult) -> None:
        """SFCパターンに従ったJinja2マクロラッパーをチェック"""
        if "{% macro" not in content and "{%- macro" not in content:
            result.add_warning(
                "コンポーネントに {% macro %} ラッパーがありません。"
                "SFCパターンに従い、{% macro component_name(args) %} で囲んでください。"
            )

    def _check_server_state_mutation(self, content: str, result: ValidationResult) -> None:
        """サーバー状態への破壊的操作をチェック（ZEN哲学: サーバー状態の直接書き換え禁止）"""
        mutation_patterns = [
            r"this\.\w+\.push\s*\(",
            r"this\.\w+\.splice\s*\(",
            r"this\.\w+\.pop\s*\(",
        ]
        for pattern in mutation_patterns:
            if re.search(pattern, content):
                result.add_warning(
                    "サーバー状態への破壊的操作（push/splice/pop）が検出されました。"
                    "APIを通じてデータを更新し、バックエンドから受け取った最新データで丸ごと再代入してください。"
                )
                break
