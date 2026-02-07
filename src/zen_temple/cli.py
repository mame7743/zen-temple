"""zen-temple のコマンドラインインターフェース"""

import sys
from pathlib import Path
from typing import Optional

import click

from zen_temple import __version__
from zen_temple.scaffold import ScaffoldGenerator
from zen_temple.template_manager import TemplateManager
from zen_temple.validator import ComponentValidator


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """
    zen-temple: ビルド不要、マジックなしのフロントエンドコンポーネントシステム

    HTMX、Alpine.js、Jinja2、Tailwind CSSを使用してリアクティブなWebUIを構築します。
    """
    pass


@main.command()
@click.argument("project_name")
@click.option(
    "--path",
    type=click.Path(),
    default=".",
    help="プロジェクトの親ディレクトリ（デフォルト: カレントディレクトリ）",
)
@click.option("--no-examples", is_flag=True, help="サンプルコンポーネントの作成をスキップ")
@click.option("--with-server", is_flag=True, help="基本的なFlask開発サーバーを含める")
def new(project_name: str, path: str, no_examples: bool, with_server: bool) -> None:
    """
    新しいzen-templeプロジェクトを作成します。

    以下を含む完全なプロジェクト構造を生成します:
    - ベーステンプレートとレイアウト
    - 設定ファイル
    - サンプルコンポーネント（--no-examplesが指定されていない場合）
    - オプションのFlaskサーバー（--with-serverを指定した場合）

    例:
        zen-temple new my-app
        zen-temple new my-app --with-server
    """
    click.echo(f"新しいzen-templeプロジェクトを作成中: {project_name}")

    generator = ScaffoldGenerator(project_root=Path(path))

    try:
        created = generator.generate_project(
            project_name=project_name, include_examples=not no_examples, include_server=with_server
        )

        click.echo("\n✓ プロジェクトが正常に作成されました！")
        click.echo("\n作成されたファイル:")
        for name in sorted(created.keys()):
            click.echo(f"  - {name}")

        click.echo("\n次のステップ:")
        click.echo(f"  cd {project_name}")

        if with_server:
            click.echo("  pip install -r requirements.txt")
            click.echo("  python app/main.py")
        else:
            click.echo("  # templates/ ディレクトリ内のテンプレートを編集")
            click.echo("  # 設定については zen-temple.yaml を参照")

        click.echo("\n楽しく開発しましょう！🎨")

    except Exception as e:
        click.echo(f"プロジェクト作成エラー: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("component_name")
@click.option(
    "--type",
    "component_type",
    type=click.Choice(["basic", "form", "list", "card"]),
    default="basic",
    help="生成するコンポーネントのタイプ",
)
@click.option(
    "--output", type=click.Path(), help="出力ディレクトリ（デフォルト: templates/components）"
)
def component(component_name: str, component_type: str, output: Optional[str]) -> None:
    """
    新しいコンポーネントテンプレートを生成します。

    コンポーネントは、状態管理にAlpine.jsを、サーバー通信にHTMXを使用した
    自己完結型で再利用可能なHTMLテンプレートです。

    コンポーネントタイプ:
        - basic: Alpine.js状態を持つシンプルなコンポーネント
        - form: バリデーション付きフォームコンポーネント
        - list: データ読み込み機能付きリストコンポーネント
        - card: カード/ウィジェットコンポーネント

    例:
        zen-temple component my-widget
        zen-temple component user-form --type form
    """
    click.echo(f"{component_type}コンポーネントを生成中: {component_name}")

    generator = ScaffoldGenerator()
    output_dir = Path(output) if output else None

    try:
        component_path = generator.generate_component(
            component_name=component_name, component_type=component_type, output_dir=output_dir
        )

        click.echo(f"✓ コンポーネントが作成されました: {component_path}")
        click.echo("\nこのコンポーネントを使用するには:")
        click.echo(f'  {{% include "components/{component_name}.html" %}}')

    except Exception as e:
        click.echo(f"コンポーネント作成エラー: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--project-name", prompt="プロジェクト名", help="プロジェクト名")
@click.option(
    "--template-dir", default="templates", help="テンプレートディレクトリ（デフォルト: templates）"
)
def init(project_name: str, template_dir: str) -> None:
    """
    既存のプロジェクトにzen-temple設定を初期化します。

    適切なデフォルト値でzen-temple.yaml設定ファイルを作成します。
    既存のプロジェクトにzen-templeを追加する場合に使用します。

    例:
        zen-temple init --project-name my-app
    """
    click.echo(f"zen-temple設定を初期化中: {project_name}")

    generator = ScaffoldGenerator()
    project_path = Path.cwd()

    try:
        config_file = generator._create_config_file(project_path, project_name)
        click.echo(f"✓ 設定ファイルが作成されました: {config_file}")

        # テンプレートディレクトリが存在しない場合は作成
        template_path = project_path / template_dir
        template_path.mkdir(exist_ok=True)
        (template_path / "components").mkdir(exist_ok=True)
        (template_path / "layouts").mkdir(exist_ok=True)

        click.echo(f"✓ テンプレートディレクトリが {template_dir}/ に作成されました")

    except Exception as e:
        click.echo(f"プロジェクト初期化エラー: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("component_path", type=click.Path(exists=True))
def validate(component_path: str) -> None:
    """
    コンポーネントテンプレートを検証します。

    コンポーネントがzen-templeの哲学に従っているかをチェックします:
    - インラインJavaScriptを使用していない（Alpine.jsを使用）
    - 適切なHTMXの使用
    - クリーンなテンプレート構造

    例:
        zen-temple validate templates/components/my-component.html
    """
    click.echo(f"コンポーネントを検証中: {component_path}")

    validator = ComponentValidator()
    path = Path(component_path)

    result = validator.validate_component(path)

    if result.is_valid:
        click.echo(click.style("✓ コンポーネントは有効です！", fg="green"))
    else:
        click.echo(click.style("✗ コンポーネントに問題があります:", fg="red"))

    if result.errors:
        click.echo("\nエラー:")
        for error in result.errors:
            click.echo(click.style(f"  - {error}", fg="red"))

    if result.warnings:
        click.echo("\n警告:")
        for warning in result.warnings:
            click.echo(click.style(f"  - {warning}", fg="yellow"))

    if not result.is_valid:
        sys.exit(1)


@main.command()
@click.option(
    "--template-dir",
    default="templates",
    type=click.Path(exists=True),
    help="一覧表示するテンプレートディレクトリ",
)
def list_components(template_dir: str) -> None:
    """
    プロジェクト内の利用可能な全コンポーネントを一覧表示します。

    例:
        zen-temple list-components
        zen-temple list-components --template-dir my-templates
    """
    manager = TemplateManager(template_dirs=[Path(template_dir)])
    components = manager.list_components()

    if components:
        click.echo(f"{len(components)}個のコンポーネントが見つかりました:")
        for component in components:
            click.echo(f"  - {component}")
    else:
        click.echo("コンポーネントが見つかりませんでした。")
        click.echo("\nコンポーネントを作成するには: zen-temple component <名前>")


@main.command()
def philosophy() -> None:
    """
    zen-templeの設計哲学を表示します。

    これらの原則を理解することで、zen-templeを使用して
    より良いアプリケーションを構築できます。
    """
    philosophy_text = """
╔════════════════════════════════════════════════════════════════╗
║                   zen-temple 哲学                               ║
║         (ゼロテンプレート - ゼロビルド - ゼロマジック)           ║
╚════════════════════════════════════════════════════════════════╝

1. ビルドステップ不要
   テンプレートを編集して即座に変更を確認。webpackもバンドラーも
   コンパイルも不要。ページをリロードするだけ。

2. 隠された抽象化なし
   書いたものがそのまま動く。マジック変換も隠された複雑さもなし。
   テンプレートはテンプレート。

3. テンプレート中心設計
   テンプレートが真実の源。すべてがHTMLから始まる。
   コンポーネントは単なるJinja2のインクルード。

4. ロジックはAlpine.js内
   状態管理はx-data関数に属する。HTMLは宣言的に保つ。
   全てのクライアントサイドのリアクティビティにAlpine.jsを使用。

5. サーバーはJSON/HTMLを返す
   APIエンドポイントはJSONデータまたはHTMLフラグメントを返す。
   クライアント側で処理方法を決定（Alpine.jsまたはHTMX）。

6. 通信にはHTMX
   全てのサーバー通信とイベントにHTMXを使用。細かい制御が必要な
   場合を除き、手動でfetch()を呼び出さない。

7. ゼロマジック
   全てのコード行が可視化され編集可能。コード生成もビルド成果物も
   隠しファイルもなし。

技術スタック:
  • HTMX      - サーバー通信と動的更新
  • Alpine.js - リアクティブな状態とクライアントサイドロジック
  • Jinja2    - テンプレートレンダリングと構成
  • Tailwind  - CDN経由のスタイリング（ビルド不要）

詳細はこちら: https://github.com/mame7743/zen-temple
"""
    click.echo(philosophy_text)


if __name__ == "__main__":
    main()
