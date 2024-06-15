# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from django.core.serializers import serialize
from django.db.models.query import QuerySet
import simplejson as json
from django.template import Library
from django.utils.safestring import mark_safe
from datetime import datetime
from urllib.parse import urlparse
import re

register = Library()

def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(json.dumps(object))

register.filter('jsonify', jsonify)

def render_age_eligibility(age_req):
    s = ''
    if age_req['age_min'] and age_req['age_max']:
        s = f'{age_req["age_min"]}-{age_req["age_max"]} (until you turn {age_req["age_max"] + 1} years old)'
    elif age_req['age_min']:
        s = f'{age_req["age_min"]}+'
    elif age_req['age_max']:
        s = f'Under {age_req["age_max"]}'
    if age_req['population_served']:
        s += f" ({age_req['population_served']})"
    return s

register.filter('render_age_eligibility', render_age_eligibility)


def contains_all_ages_requirement(age_reqs):
    return bool([req for req in age_reqs if req['all_ages']])

register.filter('contains_all_ages_requirement', contains_all_ages_requirement)

def format_website_url(url):
    print(url)
    if not url:
        return None

    if not url.startswith('http://') and not url.startswith('https://'):
        return 'https://' + url
    return url

def format_website_url_view(url):
    if not url:
        return None

    try:
        url_object = urlparse(url)
        return url_object.netloc.replace('www.', '') + url_object.path
    except ValueError:
        return url.replace('www.', '')


def linebreaks_before_bullet(value):
    return value.replace('•', '<br>•') 

register.filter('format_website_url', format_website_url)
register.filter('linebreaks_before_bullet', linebreaks_before_bullet)
register.filter('format_website_url_view', format_website_url_view)



def render_schedule(s):
    schedule = convert_object_to_array(s)
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    if (
        len(schedule) == 7
        and all(
            day["opens_at"] == "00:00:00" and day["closes_at"] == "23:59:00"
            for day in schedule
        )
    ):
        return "Open 24/7"

    def day_number_to_name(weekday):
        return weekdays[weekday - 1]

    def format_hour(time):
        if re.search(r"(23:59:00|00:00:00)", time):
            return "midnight"
        return datetime.strptime(time, "%H:%M:%S").strftime("%-I %p").replace(":00 ", " ")

    def format_hours(opens, closes):
        return f"{format_hour(opens)} to {format_hour(closes)}"

    def format_range(day_range):
        start, end = day_range["start"], day_range["end"]
        if end == start:
            return day_number_to_name(start)
        if end == start + 1:
            return f"{day_number_to_name(start)} & {day_number_to_name(end)}"
        return f"{day_number_to_name(start)} to {day_number_to_name(end)}"

    ordered_schedule = sorted(schedule, key=lambda x: (x["weekday"], x["opens_at"]))

    days_grouped_by_hours = {}
    for day in ordered_schedule:
        hours_string = format_hours(day["opens_at"], day["closes_at"])
        days_grouped_by_hours[hours_string] = (
            days_grouped_by_hours.get(hours_string, []) + [day["weekday"]]
        )

    group_strings = []
    for hours_string, remaining_weekdays in days_grouped_by_hours.items():
        day_ranges = []
        while remaining_weekdays:
            current_day_range = day_ranges[-1] if day_ranges else None
            day = remaining_weekdays.pop(0)

            if day > 7:
                continue

            if current_day_range and current_day_range["end"] == day - 1:
                current_day_range["end"] = day
            else:
                day_ranges.append({"start": day, "end": day})

        group_strings.append(
            f"{', '.join(format_range(day_range) for day_range in day_ranges)} {hours_string}"
        )

    return f"Open {', '.join(group_strings)}"


def convert_object_to_array(input_object):
    output_array = []

    for key, opening_hours in input_object.items():
        weekday = int(key)

        def convert_time(time):
            # FIXME: this is truly awful code. should probably use datetime.strptime instead
            hour, minute = map(int, time.replace(" AM", "").replace(" PM", "").split(":"))
            formatted_hour = hour

            if "PM" in time and formatted_hour != 12:
                formatted_hour += 12

            return f"{formatted_hour:02d}:{minute:02d}:00"

        for hours in opening_hours:
            converted_opening_time = convert_time(hours["opens_at"])
            converted_closing_time = convert_time(hours["closes_at"])
            output_array.append({
                "opens_at": converted_opening_time,
                "closes_at": converted_closing_time,
                "weekday": weekday,
            })

    return output_array[::-1]

register.filter('render_schedule', render_schedule)
