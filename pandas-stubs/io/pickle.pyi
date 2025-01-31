from typing import (
    Literal,
    Optional,
    Union,
)

from pandas._typing import FilePathOrBuffer

def to_pickle(
    obj,
    filepath_or_buffer: FilePathOrBuffer,
    compression: Optional[str] = ...,
    protocol: int = ...,
): ...
def read_pickle(
    filepath_or_buffer_or_reader: FilePathOrBuffer,
    compression: Optional[
        Union[str, Literal["infer", "gzip", "bz2", "zip", "xz"]]
    ] = ...,
): ...
