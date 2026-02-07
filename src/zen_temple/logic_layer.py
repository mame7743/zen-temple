"""
zen-templeコンポーネントのための純粋ロジックレイヤー

このモジュールは「ロジックは純粋、ブリッジは最小限」の設計原則を実装します。
全てのビジネスロジックはバニラPythonクラスに記述し、Jinjaマクロが
テンプレートへの最小限のブリッジとして機能します。

設計原則:
1. バニラクラス分離: ロジックは純粋なPythonで、フレームワーク依存なし
2. 最小限のブリッジ: Jinjaマクロがロジックとテンプレートを接続
3. ゼロレガシー: ロジックとプレゼンテーションのクリーンな分離
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Optional


class PureLogic(ABC):
    """
    純粋ビジネスロジックのための基底クラス

    全てのビジネスロジックはこのクラスを継承し、フレームワーク非依存を保つべきです。
    ロジッククラスは、Webフレームワーク、テンプレートエンジン、UIライブラリへの依存なしの
    純粋なPythonコードのみを含むべきです。

    例:
        class CounterLogic(PureLogic):
            def __init__(self, initial_value: int = 0):
                self.value = initial_value

            def increment(self) -> int:
                self.value += 1
                return self.value

            def decrement(self) -> int:
                self.value -= 1
                return self.value

            def to_context(self) -> Dict[str, Any]:
                return {"count": self.value}
    """

    @abstractmethod
    def to_context(self) -> dict[str, Any]:
        """
        ロジック状態をテンプレートコンテキストに変換

        戻り値:
            テンプレートに渡す変数の辞書
        """
        pass


@dataclass
class ComponentState:
    """
    コンポーネントのためのイミュータブル状態コンテナ

    型安全性と自動シリアライゼーションのためにdataclassを使用します。
    全ての状態はAlpine.js互換性のためにJSONシリアライズ可能である必要があります。

    例:
        @dataclass
        class TodoState(ComponentState):
            todos: List[Dict[str, Any]]
            new_todo: str = ""
    """

    def to_dict(self) -> dict[str, Any]:
        """状態を辞書に変換"""
        return asdict(self)


class LogicBridge:
    """
    純粋ロジックとテンプレート間の最小限のブリッジ

    このクラスは、バニラPythonロジッククラスをJinja2テンプレートと接続するための
    ユーティリティを提供し、マクロをインターフェースレイヤーとして使用します。

    例:
        bridge = LogicBridge()
        counter_logic = CounterLogic(initial_value=0)
        context = bridge.prepare_context(counter_logic)
        # テンプレートレンダリングでコンテキストを使用
    """

    def __init__(self):
        """ロジックブリッジを初期化"""
        self._logic_registry: dict[str, type] = {}

    def register_logic(self, name: str, logic_class: type) -> None:
        """
        ロジッククラスを登録

        引数:
            name: ロジッククラスを登録する名前
            logic_class: 登録するロジッククラス
        """
        self._logic_registry[name] = logic_class

    def prepare_context(
        self, logic: PureLogic, extra_context: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """
        ロジックインスタンスからテンプレートコンテキストを準備

        引数:
            logic: 純粋ロジックインスタンス
            extra_context: 追加のコンテキスト変数

        戻り値:
            テンプレートレンダリング用の完全なコンテキスト辞書
        """
        context = logic.to_context()

        if extra_context:
            context.update(extra_context)

        return context

    def create_logic(self, name: str, **kwargs: Any) -> Optional[PureLogic]:
        """
        名前でロジックインスタンスを作成

        引数:
            name: ロジッククラスの登録名
            **kwargs: ロジックコンストラクタに渡す引数

        戻り値:
            ロジックインスタンス、または見つからない場合はNone
        """
        logic_class = self._logic_registry.get(name)
        if logic_class is None:
            return None

        return logic_class(**kwargs)


class ComponentLogic(PureLogic):
    """
    コンポーネントビジネスロジックの基底クラス

    コンポーネントレベルのロジックのための共通機能を提供します。
    再利用可能なロジックパターンのために、コンポーネントはこのクラスを継承すべきです。
    """

    def __init__(self, component_id: Optional[str] = None):
        """
        コンポーネントロジックを初期化

        引数:
            component_id: コンポーネントのオプション一意識別子
        """
        self.component_id = component_id or self._generate_id()

    def _generate_id(self) -> str:
        """一意のコンポーネントIDを生成"""
        import uuid

        return f"component-{uuid.uuid4().hex[:8]}"

    def to_context(self) -> dict[str, Any]:
        """
        デフォルトコンテキストにはコンポーネントIDが含まれます

        より多くのコンテキストを追加するには、このメソッドをオーバーライドします。
        """
        return {"component_id": self.component_id}


def create_macro_helpers() -> dict[str, Any]:
    """
    Jinjaマクロで使用するヘルパー関数を作成

    これらのヘルパーは、Pythonロジックとテンプレートマクロ間の
    最小限のブリッジとして機能します。

    戻り値:
        Jinja環境用のヘルパー関数の辞書
    """

    def prepare_alpine_data(logic: PureLogic) -> dict[str, Any]:
        """Alpine.js x-data用のロジックコンテキストを準備"""
        return logic.to_context()

    def serialize_state(state: ComponentState) -> dict[str, Any]:
        """テンプレート用にコンポーネント状態をシリアライズ"""
        return state.to_dict()

    return {
        "prepare_alpine_data": prepare_alpine_data,
        "serialize_state": serialize_state,
    }
