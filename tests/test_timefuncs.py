# flake8: noqa: F841

import datetime as dt
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

import numpy as np
from numpy import typing as npt
import pandas as pd
import pytest
from pytz.tzinfo import BaseTzInfo
from typing_extensions import assert_type

from pandas._libs import NaTType

from tests import check

if TYPE_CHECKING:
    from pandas.core.series import (
        TimedeltaSeries,
        TimestampSeries,
    )

# Separately define here so pytest works
np_ndarray_bool = npt.NDArray[np.bool_]


def test_types_init() -> None:
    ts: pd.Timestamp = pd.Timestamp("2021-03-01T12")
    ts1: pd.Timestamp = pd.Timestamp(dt.date(2021, 3, 15))
    ts2: pd.Timestamp = pd.Timestamp(dt.datetime(2021, 3, 10, 12))
    ts3: pd.Timestamp = pd.Timestamp(pd.Timestamp("2021-03-01T12"))
    ts4: pd.Timestamp = pd.Timestamp(1515590000.1, unit="s")
    ts5: pd.Timestamp = pd.Timestamp(1515590000.1, unit="s", tz="US/Pacific")
    ts6: pd.Timestamp = pd.Timestamp(1515590000100000000)  # plain integer (nanosecond)
    ts7: pd.Timestamp = pd.Timestamp(2021, 3, 10, 12)
    ts8: pd.Timestamp = pd.Timestamp(year=2021, month=3, day=10, hour=12)
    ts9: pd.Timestamp = pd.Timestamp(
        year=2021, month=3, day=10, hour=12, tz="US/Pacific"
    )


def test_types_arithmetic() -> None:
    ts: pd.Timestamp = pd.to_datetime("2021-03-01")
    ts2: pd.Timestamp = pd.to_datetime("2021-01-01")
    delta: pd.Timedelta = pd.to_timedelta("1 day")

    tsr: pd.Timedelta = ts - ts2
    tsr2: pd.Timestamp = ts + delta
    tsr3: pd.Timestamp = ts - delta
    tsr4: pd.Timedelta = ts - dt.datetime(2021, 1, 3)


def test_types_comparison() -> None:
    ts: pd.Timestamp = pd.to_datetime("2021-03-01")
    ts2: pd.Timestamp = pd.to_datetime("2021-01-01")

    tsr: bool = ts < ts2
    tsr2: bool = ts > ts2


def test_types_timestamp_series_comparisons() -> None:
    # GH 27
    df = pd.DataFrame(["2020-01-01", "2019-01-01"])
    tss = pd.to_datetime(df[0], format="%Y-%m-%d")
    ts = pd.to_datetime("2019-02-01", format="%Y-%m-%d")
    tssr = tss <= ts
    tssr2 = tss >= ts
    tssr3 = tss == ts
    check(assert_type(tssr, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(tssr2, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(tssr3, "pd.Series[bool]"), pd.Series, bool)


def test_types_pydatetime() -> None:
    ts: pd.Timestamp = pd.Timestamp("2021-03-01T12")

    datet: dt.datetime = ts.to_pydatetime()
    datet2: dt.datetime = ts.to_pydatetime(False)
    datet3: dt.datetime = ts.to_pydatetime(warn=True)


def test_to_timedelta() -> None:
    td: pd.Timedelta = pd.to_timedelta(3, "days")
    tds: pd.TimedeltaIndex = pd.to_timedelta([2, 3], "minutes")


def test_timedelta_arithmetic() -> None:
    td1: pd.Timedelta = pd.to_timedelta(3, "days")
    td2: pd.Timedelta = pd.to_timedelta(4, "hours")
    td3: pd.Timedelta = td1 + td2
    td4: pd.Timedelta = td1 - td2
    td5: pd.Timedelta = td1 * 4.3
    td6: pd.Timedelta = td3 / 10.2


def test_timedelta_series_arithmetic() -> None:
    tds1: pd.TimedeltaIndex = pd.to_timedelta([2, 3], "minutes")
    td1: pd.Timedelta = pd.Timedelta("2 days")
    r1: pd.TimedeltaIndex = tds1 + td1
    r2: pd.TimedeltaIndex = tds1 - td1
    r3: pd.TimedeltaIndex = tds1 * 4.3
    r4: pd.TimedeltaIndex = tds1 / 10.2


def test_timestamp_timedelta_series_arithmetic() -> None:
    ts = pd.Timestamp("2022-03-05")
    s1 = pd.Series(["2022-03-05", "2022-03-06"])
    ts1 = pd.to_datetime(pd.Series(["2022-03-05", "2022-03-06"]))
    assert isinstance(ts1.iloc[0], pd.Timestamp)
    td1 = pd.to_timedelta([2, 3], "seconds")
    ts2 = pd.to_datetime(pd.Series(["2022-03-08", "2022-03-10"]))
    r1 = ts1 - ts2
    check(assert_type(r1, "TimedeltaSeries"), pd.Series, pd.Timedelta)
    r2 = r1 / td1
    check(assert_type(r2, "pd.Series[float]"), pd.Series, float)
    r3 = r1 - td1
    check(assert_type(r3, "TimedeltaSeries"), pd.Series, pd.Timedelta)
    r4 = pd.Timedelta(5, "days") / r1
    check(assert_type(r4, "pd.Series[float]"), pd.Series, float)
    sb = pd.Series([1, 2]) == pd.Series([1, 3])
    check(assert_type(sb, "pd.Series[bool]"), pd.Series, bool)
    r5 = sb * r1
    check(assert_type(r5, "TimedeltaSeries"), pd.Series, pd.Timedelta)
    r6 = r1 * 4
    check(assert_type(r6, "TimedeltaSeries"), pd.Series, pd.Timedelta)


def test_timestamp_dateoffset_arithmetic() -> None:
    ts = pd.Timestamp("2022-03-18")
    do = pd.DateOffset(days=366)
    r1: pd.Timestamp = ts + do


def test_datetimeindex_plus_timedelta() -> None:
    tscheck = pd.Series([pd.Timestamp("2022-03-05"), pd.Timestamp("2022-03-06")])
    dti = pd.to_datetime(["2022-03-08", "2022-03-15"])
    td_s = pd.to_timedelta(pd.Series([10, 20]), "minutes")
    dti_td_s = dti + td_s
    check(
        assert_type(dti_td_s, "TimestampSeries"),
        pd.Series,
        pd.Timestamp,
    )
    td_dti_s = td_s + dti
    check(
        assert_type(td_dti_s, "TimestampSeries"),
        pd.Series,
        pd.Timestamp,
    )
    tdi = pd.to_timedelta([10, 20], "minutes")
    dti_tdi_dti = dti + tdi
    check(assert_type(dti_tdi_dti, "pd.DatetimeIndex"), pd.DatetimeIndex)
    tdi_dti_dti = tdi + dti
    check(assert_type(tdi_dti_dti, "pd.DatetimeIndex"), pd.DatetimeIndex)
    dti_td_dti = dti + pd.Timedelta(10, "minutes")
    check(assert_type(dti_td_dti, "pd.DatetimeIndex"), pd.DatetimeIndex)


def test_timestamp_plus_timedelta_series() -> None:
    tscheck = pd.Series([pd.Timestamp("2022-03-05"), pd.Timestamp("2022-03-06")])
    ts = pd.Timestamp("2022-03-05")
    td = pd.to_timedelta(pd.Series([10, 20]), "minutes")
    r3 = td + ts
    check(assert_type(r3, "TimestampSeries"), pd.Series, pd.Timestamp)


def test_timedelta_series_mult() -> None:
    df = pd.DataFrame({"x": [1, 3, 5], "y": [2, 2, 6]})
    std = (df["x"] < df["y"]) * pd.Timedelta(10, "minutes")
    check(
        assert_type(std, "TimedeltaSeries"),
        pd.Series,
        pd.Timedelta,
    )


def test_timedelta_series_sum() -> None:
    s = pd.Series(pd.to_datetime(["04/05/2022 11:00", "04/03/2022 10:00"])) - pd.Series(
        pd.to_datetime(["04/05/2022 08:00", "04/03/2022 09:00"])
    )
    ssum = s.sum()
    ires: int = ssum.days

    sf = pd.Series([1.0, 2.2, 3.3])
    sfsum: float = sf.sum()


def test_iso_calendar() -> None:
    # GH 31
    dates = pd.date_range(start="2012-01-01", end="2019-12-31", freq="W-MON")
    dates.isocalendar()


def fail_on_adding_two_timestamps() -> None:
    s1 = pd.Series(pd.to_datetime(["2022-05-01", "2022-06-01"]))
    s2 = pd.Series(pd.to_datetime(["2022-05-15", "2022-06-15"]))
    if TYPE_CHECKING:
        ssum: pd.Series = s1 + s2  # type: ignore[operator]
        ts = pd.Timestamp("2022-06-30")
        tsum: pd.Series = s1 + ts  # type: ignore[operator]


def test_dtindex_tzinfo() -> None:
    # GH 71
    dti = pd.date_range("2000-1-1", periods=10)
    assert assert_type(dti.tzinfo, Optional[dt.tzinfo]) is None


def test_todatetime_fromnumpy() -> None:
    # GH 72
    t1 = np.datetime64("2022-07-04 02:30")
    check(assert_type(pd.to_datetime(t1), pd.Timestamp), pd.Timestamp)


def test_comparisons_datetimeindex() -> None:
    # GH 74
    dti = pd.date_range("2000-01-01", "2000-01-10")
    ts = pd.Timestamp("2000-01-05")
    check(assert_type((dti < ts), np_ndarray_bool), np.ndarray)
    check(assert_type((dti > ts), np_ndarray_bool), np.ndarray)
    check(assert_type((dti >= ts), np_ndarray_bool), np.ndarray)
    check(assert_type((dti <= ts), np_ndarray_bool), np.ndarray)
    check(assert_type((dti == ts), np_ndarray_bool), np.ndarray)
    check(assert_type((dti != ts), np_ndarray_bool), np.ndarray)


def test_to_datetime_nat() -> None:
    # GH 88
    check(
        assert_type(pd.to_datetime("2021-03-01", errors="ignore"), pd.Timestamp),
        pd.Timestamp,
    )
    check(
        assert_type(pd.to_datetime("2021-03-01", errors="raise"), pd.Timestamp),
        pd.Timestamp,
    )
    check(
        assert_type(
            pd.to_datetime("2021-03-01", errors="coerce"),
            "Union[pd.Timestamp, NaTType]",
        ),
        pd.Timestamp,
    )
    check(
        assert_type(
            pd.to_datetime("not a date", errors="coerce"),
            "Union[pd.Timestamp, NaTType]",
        ),
        NaTType,
    )


def test_dt_accessors() -> None:
    # GH 131
    i0 = pd.date_range(start="2022-06-01", periods=10)
    check(assert_type(i0, pd.DatetimeIndex), pd.DatetimeIndex, pd.Timestamp)

    check(assert_type(i0.to_series(), "TimestampSeries"), pd.Series, pd.Timestamp)

    s0 = pd.Series(i0)

    check(assert_type(s0.dt.date, "pd.Series[dt.date]"), pd.Series, dt.date)
    check(assert_type(s0.dt.time, "pd.Series[dt.time]"), pd.Series, dt.time)
    check(assert_type(s0.dt.timetz, "pd.Series[dt.time]"), pd.Series, dt.time)
    check(assert_type(s0.dt.year, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.month, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.day, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.hour, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.minute, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.second, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.microsecond, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.nanosecond, "pd.Series[int]"), pd.Series, int)
    with pytest.warns(
        FutureWarning,
        match="Series.dt.weekofyear and Series.dt.week have been deprecated",
    ):
        check(assert_type(s0.dt.week, "pd.Series[int]"), pd.Series, int)
    with pytest.warns(
        FutureWarning,
        match="Series.dt.weekofyear and Series.dt.week have been deprecated",
    ):
        check(assert_type(s0.dt.weekofyear, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.dayofweek, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.day_of_week, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.weekday, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.dayofyear, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.day_of_year, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.quarter, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.is_month_start, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_month_end, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_quarter_start, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_quarter_end, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_year_start, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_year_end, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.is_leap_year, "pd.Series[bool]"), pd.Series, bool)
    check(assert_type(s0.dt.daysinmonth, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s0.dt.days_in_month, "pd.Series[int]"), pd.Series, int)
    assert assert_type(s0.dt.tz, Optional[Union[dt.tzinfo, BaseTzInfo]]) is None
    check(assert_type(s0.dt.freq, Optional[str]), str)
    check(assert_type(s0.dt.isocalendar(), pd.DataFrame), pd.DataFrame)
    check(
        assert_type(s0.dt.to_period("D"), "pd.Series[pd.Period]"), pd.Series, pd.Period
    )
    check(assert_type(s0.dt.to_pydatetime(), np.ndarray), np.ndarray, dt.datetime)
    local_dtarray = s0.dt.tz_localize("UTC")
    slocal = pd.Series(local_dtarray)
    check(
        assert_type(slocal.dt.tz_convert("EST"), "TimestampSeries"),
        pd.Series,
        pd.Timestamp,
    )
    check(assert_type(slocal.dt.tz, Optional[Union[dt.tzinfo, BaseTzInfo]]), BaseTzInfo)
    check(assert_type(s0.dt.normalize(), "TimestampSeries"), pd.Series, pd.Timestamp)
    check(assert_type(s0.dt.strftime("%Y"), "pd.Series[str]"), pd.Series, str)
    check(assert_type(s0.dt.round("D"), pd.Series), pd.Series, pd.Timestamp)
    check(assert_type(s0.dt.floor("D"), pd.Series), pd.Series, pd.Timestamp)
    check(assert_type(s0.dt.ceil("D"), pd.Series), pd.Series, pd.Timestamp)
    check(assert_type(s0.dt.month_name(), "pd.Series[str]"), pd.Series, str)
    check(assert_type(s0.dt.day_name(), "pd.Series[str]"), pd.Series, str)

    i1 = pd.period_range(start="2022-06-01", periods=10)

    check(assert_type(i1, pd.PeriodIndex), pd.PeriodIndex)

    check(assert_type(i1.to_series(), pd.Series), pd.Series, pd.Period)

    s1 = pd.Series(i1)

    check(assert_type(s1.dt.qyear, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s1.dt.start_time, "TimestampSeries"), pd.Series, pd.Timestamp)
    check(assert_type(s1.dt.end_time, "TimestampSeries"), pd.Series, pd.Timestamp)

    i2 = pd.timedelta_range(start="1 day", periods=10)
    check(assert_type(i2, pd.TimedeltaIndex), pd.TimedeltaIndex)

    check(assert_type(i2.to_series(), "TimedeltaSeries"), pd.Series, pd.Timedelta)

    s2 = pd.Series(i2)

    check(assert_type(s2.dt.days, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s2.dt.seconds, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s2.dt.microseconds, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s2.dt.nanoseconds, "pd.Series[int]"), pd.Series, int)
    check(assert_type(s2.dt.components, pd.DataFrame), pd.DataFrame)
    check(assert_type(s2.dt.to_pytimedelta(), np.ndarray), np.ndarray)
    check(assert_type(s2.dt.total_seconds(), "pd.Series[float]"), pd.Series, float)
