"""Tests for ScaffoldGenerator."""

from pathlib import Path

from zen_temple.scaffold import ScaffoldGenerator


def test_scaffold_init(tmp_path: Path) -> None:
    """Test ScaffoldGenerator initialization."""
    generator = ScaffoldGenerator(project_root=tmp_path)
    assert generator.project_root == tmp_path


def test_generate_project(tmp_path: Path) -> None:
    """Test generating a complete project."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="test_project", include_examples=True, include_server=False
    )

    project_path = tmp_path / "test_project"

    # Check that directories were created
    assert (project_path / "templates").exists()
    assert (project_path / "templates/components").exists()
    assert (project_path / "templates/layouts").exists()
    assert (project_path / "static").exists()

    # Check that files were created
    assert (project_path / "zen-temple.yaml").exists()
    assert (project_path / "templates/layouts/base.html").exists()
    assert (project_path / "README.md").exists()

    # Check example components
    assert (project_path / "templates/components/counter.html").exists()
    assert (project_path / "templates/components/todo.html").exists()
    assert (project_path / "templates/index.html").exists()


def test_generate_project_with_server(tmp_path: Path) -> None:
    """Test generating a project with server files."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="server_project", include_examples=False, include_server=True
    )

    project_path = tmp_path / "server_project"

    # Check server files
    assert (project_path / "app").exists()
    assert (project_path / "app/main.py").exists()
    assert (project_path / ".env").exists()
    assert (project_path / "requirements.txt").exists()


def test_generate_project_no_examples(tmp_path: Path) -> None:
    """Test generating a project without examples."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="minimal_project", include_examples=False, include_server=False
    )

    project_path = tmp_path / "minimal_project"

    # Should have basic structure
    assert (project_path / "templates").exists()
    assert (project_path / "zen-temple.yaml").exists()

    # Should not have example components
    assert not (project_path / "templates/components/counter.html").exists()


def test_generate_component(tmp_path: Path) -> None:
    """Test generating a component."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"
    component_path = generator.generate_component(
        component_name="test_component", component_type="basic", output_dir=output_dir
    )

    assert component_path.exists()
    assert component_path.name == "test_component.html"

    content = component_path.read_text()
    assert "test_component" in content
    assert "x-data" in content


def test_generate_different_component_types(tmp_path: Path) -> None:
    """Test generating different component types."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"

    component_types = ["basic", "form", "list", "card"]

    for comp_type in component_types:
        component_path = generator.generate_component(
            component_name=f"{comp_type}_component", component_type=comp_type, output_dir=output_dir
        )

        assert component_path.exists()
        content = component_path.read_text()
        assert f"{comp_type}_component" in content


def test_create_base_layout(tmp_path: Path) -> None:
    """Test creating base layout."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    layout_path = generator._create_base_layout(tmp_path)

    assert layout_path.exists()
    content = layout_path.read_text()

    # Check for required CDN imports in generated template
    # Note: These are literal strings in our template, not user input
    assert "htmx.org" in content
    assert "alpinejs" in content
    assert "tailwindcss.com" in content

    # Check for Jinja2 blocks
    assert "{% block" in content


def test_create_config_file(tmp_path: Path) -> None:
    """Test creating configuration file."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    config_path = generator._create_config_file(tmp_path, "test_project")

    assert config_path.exists()
    assert config_path.name == "zen-temple.yaml"

    content = config_path.read_text()
    assert "test_project" in content
    assert "htmx" in content
    assert "alpine" in content


def test_generate_component_uses_macro(tmp_path: Path) -> None:
    """Test that generated components use the SFC macro wrapper."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"
    component_path = generator.generate_component(
        component_name="my_widget", component_type="basic", output_dir=output_dir
    )

    content = component_path.read_text()
    # SFCパターン: macroラッパー
    assert "macro my_widget" in content
    assert "{%- endmacro" in content or "{% endmacro" in content


def test_generate_component_uses_class_based_xdata(tmp_path: Path) -> None:
    """Test that generated components use new ClassName() pattern for x-data."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"
    component_path = generator.generate_component(
        component_name="my_widget", component_type="basic", output_dir=output_dir
    )

    content = component_path.read_text()
    # ZEN哲学: インラインオブジェクトではなくクラスベースの状態管理
    assert 'x-data="new MyWidgetState()"' in content
    assert "class MyWidgetState" in content


def test_generate_component_list_uses_api_fetch(tmp_path: Path) -> None:
    """Test that list components use fetch() for explicit API calls."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"
    component_path = generator.generate_component(
        component_name="user_list", component_type="list", output_dir=output_dir
    )

    content = component_path.read_text()
    # ZEN哲学【E】Explicit Flow: fetchで明示的にAPIを叩く
    assert "fetch(" in content
    assert "async" in content
    # サーバー状態の丸ごと再代入
    assert "this.items = " in content


def test_example_counter_uses_class_pattern(tmp_path: Path) -> None:
    """Test that generated counter example uses macro + class pattern."""
    generator = ScaffoldGenerator(project_root=tmp_path)
    generator.generate_project("test_project", include_examples=True, include_server=False)

    counter_path = tmp_path / "test_project/templates/components/counter.html"
    content = counter_path.read_text()

    assert "macro counter" in content
    assert "class CounterState" in content
    assert 'x-data="new CounterState(' in content


def test_example_todo_uses_api_pattern(tmp_path: Path) -> None:
    """Test that generated todo example uses backend-driven update pattern."""
    generator = ScaffoldGenerator(project_root=tmp_path)
    generator.generate_project("test_project", include_examples=True, include_server=False)

    todo_path = tmp_path / "test_project/templates/components/todo.html"
    content = todo_path.read_text()

    assert "macro todo" in content
    assert "class TodoState" in content
    # ZEN哲学: バックエンド主導の更新
    assert "fetch(" in content
    # サーバー状態とUI状態の分離
    assert "this.todos" in content
    assert "this.newTodoText" in content
    # 破壊的メソッドを使わない
    assert ".push(" not in content


def test_to_class_name(tmp_path: Path) -> None:
    """Test the component name to class name conversion."""
    generator = ScaffoldGenerator(project_root=tmp_path)
    assert generator._to_class_name("my_widget") == "MyWidgetState"
    assert generator._to_class_name("counter") == "CounterState"
    assert generator._to_class_name("data-fetch") == "DataFetchState"
    assert generator._to_class_name("user_list") == "UserListState"
