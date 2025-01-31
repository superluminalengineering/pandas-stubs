from typing import (
    Any,
    Protocol,
    Tuple,
)

from pandas import DataFrame

class OpsMixinProtocol(Protocol): ...

class OpsMixin:
    def __eq__(self: OpsMixinProtocol, other: object) -> DataFrame: ...  # type: ignore[override]
    def __ne__(self: OpsMixinProtocol, other: object) -> DataFrame: ...  # type: ignore[override]
    def __lt__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __le__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __gt__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __ge__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    # -------------------------------------------------------------
    # Logical Methods
    def __and__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rand__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __or__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __ror__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __xor__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rxor__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    # -------------------------------------------------------------
    # Arithmetic Methods
    def __add__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __radd__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __sub__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rsub__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __mul__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rmul__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __truediv__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rtruediv__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __floordiv__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rfloordiv__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __mod__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rmod__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __divmod__(
        self: OpsMixinProtocol, other: DataFrame
    ) -> Tuple[DataFrame, DataFrame]: ...
    def __rdivmod__(
        self: OpsMixinProtocol, other: DataFrame
    ) -> Tuple[DataFrame, DataFrame]: ...
    def __pow__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
    def __rpow__(self: OpsMixinProtocol, other: Any) -> DataFrame: ...
