import datetime, pytz, calendar


def utc_now() -> datetime:
    """
    :return: Same as datetime.datetime.utcnow() but includes utc timezone; also same as
    django.utils.timezone.now() with settings.USE_TZ = True.
    """
    return pytz.utc.localize(datetime.datetime.utcnow())


def utc_timestamp(dt: datetime) -> int:
    """
    :param dt: datetime. If it has no timezone, it assumes that is UTC
    :return: the corresponding Unix timestamp, i.e., seconds since January 1, 1970 00:00:00 UTC
    """
    if dt.tzinfo is None:
        pytz.utc.localize(dt)
    return int(dt.timestamp())


def utc_datetime(ts: int) -> datetime:
    """
    :param ts: Unix timestamp in seconds
    :return: the corresponding UTC datetime
    """
    return pytz.utc.localize(datetime.datetime.utcfromtimestamp(ts))

