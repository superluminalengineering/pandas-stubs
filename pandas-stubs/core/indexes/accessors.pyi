import datetime as dt
from datetime import tzinfo
from typing import (
    Literal,
    Optional,
    Union,
)

import numpy as np
import numpy.typing as npt
from pandas import (
    Period,
    Timedelta,
)
from pandas.core.accessor import PandasDelegate
from pandas.core.arrays import (
    DatetimeArray,
    PeriodArray,
)
from pandas.core.base import (
    NoNewAttributesMixin,
    PandasObject,
)
from pandas.core.frame import DataFrame
from pandas.core.series import (
    Series,
    TimestampSeries,
)
from pytz.tzinfo import BaseTzInfo

from pandas._libs.tslibs import BaseOffset
from pandas._libs.tslibs.offsets import DateOffset
from pandas._typing import np_ndarray_bool

class Properties(PandasDelegate, PandasObject, NoNewAttributesMixin):
    def __init__(self, data: Series, orig) -> None: ...

class DatetimeAndPeriodProperties(Properties):
    # Common ones are here
    @property
    def year(self) -> Series[int]: ...
    @property
    def month(self) -> Series[int]: ...
    @property
    def day(self) -> Series[int]: ...
    @property
    def hour(self) -> Series[int]: ...
    @property
    def minute(self) -> Series[int]: ...
    @property
    def second(self) -> Series[int]: ...
    @property
    def weekday(self) -> Series[int]: ...
    @property
    def dayofweek(self) -> Series[int]: ...
    @property
    def day_of_week(self) -> Series[int]: ...
    @property
    def dayofyear(self) -> Series[int]: ...
    @property
    def day_of_year(self) -> Series[int]: ...
    @property
    def quarter(self) -> Series[int]: ...
    @property
    def days_in_month(self) -> Series[int]: ...
    @property
    def daysinmonth(self) -> Series[int]: ...
    @property
    def microsecond(self) -> Series[int]: ...
    @property
    def nanosecond(self) -> Series[int]: ...
    @property
    def is_leap_year(self) -> Series[bool]: ...
    @property
    def freq(self) -> Optional[str]: ...

class DatetimeProperties(DatetimeAndPeriodProperties):
    def to_pydatetime(self) -> np.ndarray: ...
    def isocalendar(self) -> DataFrame: ...
    @property
    def weekofyear(self) -> Series[int]: ...
    @property
    def week(self) -> Series[int]: ...
    @property
    def is_month_start(self) -> Series[bool]: ...
    @property
    def is_month_end(self) -> Series[bool]: ...
    @property
    def is_quarter_start(self) -> Series[bool]: ...
    @property
    def is_quarter_end(self) -> Series[bool]: ...
    @property
    def is_year_start(self) -> Series[bool]: ...
    @property
    def is_year_end(self) -> Series[bool]: ...
    @property
    def tz(self) -> Optional[Union[tzinfo, BaseTzInfo]]: ...
    @property
    def date(self) -> Series[dt.date]: ...
    @property
    def time(self) -> Series[dt.time]: ...
    @property
    def timetz(self) -> Series[dt.time]: ...
    def to_period(
        self, freq: Optional[Union[str, BaseOffset]] = ...
    ) -> Series[Period]: ...
    def tz_localize(
        self,
        tz: Optional[str],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> DatetimeArray: ...
    def tz_convert(self, tz: Optional[str]) -> TimestampSeries: ...
    def normalize(self) -> TimestampSeries: ...
    def strftime(self, date_format: str) -> Series[str]: ...
    # Ideally, the next 3 methods would return TimestampSeries, but because of
    # how Series.dt is hooked in, we don't know which kind of series was passed
    # in to the dt accessor
    def round(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...
    def floor(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...
    def ceil(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...
    def month_name(self, locale: Optional[str] = ...) -> Series[str]: ...
    def day_name(self, locale: Optional[str] = ...) -> Series[str]: ...

class TimedeltaProperties(Properties):
    def to_pytimedelta(self) -> np.ndarray: ...
    @property
    def components(self) -> DataFrame: ...
    @property
    def days(self) -> Series[int]: ...
    @property
    def seconds(self) -> Series[int]: ...
    @property
    def microseconds(self) -> Series[int]: ...
    @property
    def nanoseconds(self) -> Series[int]: ...
    def total_seconds(self) -> Series[float]: ...
    # Ideally, the next 3 methods would return TimedeltaSeries, but because of
    # how Series.dt is hooked in, we don't know which kind of series was passed
    # in to the dt accessor
    def round(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...
    def floor(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...
    def ceil(
        self,
        freq: Optional[Union[str, BaseOffset]],
        ambiguous: Union[Literal["raise", "infer", "NaT"], np_ndarray_bool] = ...,
        nonexistent: Union[
            Literal["shift_forward", "shift_backward", "NaT", "raise"], Timedelta
        ] = ...,
    ) -> Series: ...

class PeriodProperties(DatetimeAndPeriodProperties):
    @property
    def start_time(self) -> TimestampSeries: ...
    @property
    def end_time(self) -> TimestampSeries: ...
    @property
    def qyear(self) -> Series[int]: ...
    def strftime(self, date_format: str) -> Series[str]: ...
    def to_timestamp(
        self,
        freq: Optional[Union[str, DateOffset]] = ...,
        how: Literal["s", "e", "start", "end"] = ...,
    ) -> DatetimeArray: ...
    def asfreq(
        self,
        freq: Optional[Union[str, DateOffset]] = ...,
        how: Literal["E", "END", "FINISH", "S", "START", "BEGIN"] = ...,
    ) -> PeriodArray: ...

class CombinedDatetimelikeProperties(
    DatetimeProperties, TimedeltaProperties, PeriodProperties
):
    def __new__(cls, data: Series): ...
