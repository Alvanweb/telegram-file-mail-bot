from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from database.settings import get_setting

DEFAULT_TIMEZONE = 'Asia/Tehran'

# Common IANA timezones exposed in the panel. The stored value is the standard
# IANA name, so DST rules are handled automatically by Python zoneinfo.
TIMEZONES = [
    ('UTC', 'UTC (GMT+00:00)'),
    ('Europe/London', 'London (GMT/BST)'),
    ('Europe/Berlin', 'Berlin (CET/CEST)'),
    ('Europe/Paris', 'Paris (CET/CEST)'),
    ('Europe/Istanbul', 'Istanbul (GMT+03:00)'),
    ('Asia/Tehran', 'Tehran (GMT+03:30)'),
    ('Asia/Dubai', 'Dubai (GMT+04:00)'),
    ('Asia/Riyadh', 'Riyadh (GMT+03:00)'),
    ('Asia/Kolkata', 'India (GMT+05:30)'),
    ('Asia/Tokyo', 'Tokyo (GMT+09:00)'),
    ('Asia/Shanghai', 'Shanghai (GMT+08:00)'),
    ('Asia/Singapore', 'Singapore (GMT+08:00)'),
    ('Australia/Sydney', 'Sydney (GMT+10/+11)'),
    ('America/New_York', 'New York (GMT-05/-04)'),
    ('America/Chicago', 'Chicago (GMT-06/-05)'),
    ('America/Denver', 'Denver (GMT-07/-06)'),
    ('America/Los_Angeles', 'Los Angeles (GMT-08/-07)'),
    ('America/Toronto', 'Toronto (GMT-05/-04)'),
]


def get_timezone_name():
    value = get_setting('timezone', DEFAULT_TIMEZONE) or DEFAULT_TIMEZONE
    try:
        ZoneInfo(value)
        return value
    except ZoneInfoNotFoundError:
        return DEFAULT_TIMEZONE


def get_zoneinfo():
    return ZoneInfo(get_timezone_name())


def local_datetime(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(get_zoneinfo())


def format_timestamp(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(get_zoneinfo()).strftime(fmt)
