# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from datetime import datetime
from dateutil.parser import isoparse
from v1.models import Taxonomies, Locations
import pytz
import requests
import time
from os import environ
from operator import itemgetter
from itertools import groupby
import json

def format_datetime_to_days_ago(input_datetime):

    tzinfo = input_datetime.tzinfo

    time_difference = datetime.now(tzinfo) - input_datetime

    # Extract the number of days from the time difference
    days_ago = time_difference.days

    # Handle different cases based on the number of days
    if days_ago < 1:
        return 'within the last 24 hours'
    if days_ago == 1:
        return '1 day ago'
    elif days_ago >= 1 and days_ago < 7:
        return f'{days_ago} days ago'
    elif days_ago >= 7 and days_ago < 30:
        weeks_ago = days_ago // 7
        return f'{weeks_ago} week{"s" if weeks_ago > 1 else ""} ago'
    elif days_ago >= 30 and days_ago < 365:
        months_ago = days_ago // 30
        return f'{months_ago} month{"s" if months_ago > 1 else ""} ago'
    elif time_difference.days >= 365:
        return 'More than 1 year ago'

def get_today_integer():
    # start with monday being 1
    # end with sunday being 7
    # get the current day of the week
    now = datetime.now()
    day = now.strftime("%A")
    if day == "Monday":
        return 1
    elif day == "Tuesday":
        return 2
    elif day == "Wednesday":
        return 3
    elif day == "Thursday":
        return 4
    elif day == "Friday":
        return 5
    elif day == "Saturday":
        return 6
    elif day == "Sunday":
        return 7
    else:
        return 0
    

TAXONOMIES_BASE_SQL = "select id from taxonomies t where 1=1 "

def get_open_now_where():
    todays_integer = get_today_integer()
    est = pytz.timezone('US/Eastern')
    current_time_in_EST = datetime.now(est)
    return f" and (hs.weekday = {todays_integer} and hs.opens_at <= '{current_time_in_EST.strftime('%H:%M:%S')}' and hs.closes_at >= '{current_time_in_EST.strftime('%H:%M:%S')}')"

def convert_time(time):
    if time:
        hour, minute = time.split(':')[:-1]
        hour = int(hour)
        if hour > 12:
            hour -= 12
            suffix = 'PM'  
        else: 
            suffix = 'AM'  
        return f"{hour:02d}:{minute} {suffix}"

def filter_services_by_name(d, is_location_detail, category_name=None):
    return {
        "services": [
            {
                "name": service['name'],
                "description": service['description'],
                "category": service['Taxonomies'][0]['parent_name'],
                "subcategory": service['Taxonomies'][0]['name'],
                "info": [x['information'] for x in service["EventRelatedInfos"]]  if "EventRelatedInfos" in service else [],
                "closed": all([x['closed'] for x in service['HolidaySchedules']]),
                "schedule": {
                    weekday: list(map(lambda schedule: {
                            "opens_at": convert_time(schedule['opens_at']),
                            "closes_at": convert_time(schedule['closes_at']),
                        }, schedules)) \
                        for weekday, schedules in groupby(
                            sorted(
                                filter(
                                    lambda schedule: schedule['opens_at'] and schedule['closes_at'],
                                    service['HolidaySchedules']
                                ), 
                                key=itemgetter('weekday')), 
                            key=itemgetter('weekday')
                        )
                },
                "docs" : [doc['document'] for doc in service['RequiredDocuments'] if doc['document'] != 'None'] if is_location_detail else None,
                "referral_letter" : any(["referral letter" in doc['document'].lower() for doc in service['RequiredDocuments']]) if is_location_detail else None,
                "eligibility": [elig['description'] for elig in service['Eligibilities'] if elig['description']] if is_location_detail else None,
                "membership": any(["membership" in elig['EligibilityParameter']['name'].lower() and elig['eligible_values'] and not "false" in [str(elig_value).lower() for elig_value in elig['eligible_values']] for elig in service['Eligibilities']]) if is_location_detail else None,
            } for service in d['Services'] if ( category_name in (service['Taxonomies'][0]['parent_name'], service['Taxonomies'][0]['name']) if category_name else True)
        ]
    }


def map_gogetta_to_yourpeer(d, is_location_detail):
    org_name = d["Organization"]['name']
    address = d['PhysicalAddresses'][0] if 'PhysicalAddresses' in d else d['address']
    postal_code = address['postal_code'] if 'postal_code' in address else address['postalCode']
    city = address['city']
    area = address['neighborhood']
    address_1 = address['address_1'] if 'address_1' in address else address['street']
    updated_at = d["last_validated_at"]
    location_id = d['id']
    return {
        "id": location_id,
        'location_name': d['name'],
        'address': address_1,
        'city': city,
        'region': address['region'],
        'state': address['state_province'] if 'state_province' in address else address['state'],
        'zip': postal_code,
        'lat': d['position']['coordinates'][1],
        'lng': d['position']['coordinates'][0],
        "area": area,
        "info": [x['information'] for x in d['EventRelatedInfos']], 
        "slug": f'/locations/{d["slug"]}',
        "last_updated": format_datetime_to_days_ago(isoparse(updated_at)),
        "last_updated_date": updated_at,
        "name": org_name,
        "phone": d["Phones"] and d["Phones"][0]['number'],
        "url": d["Organization"]['url'],
        "accommodation_services": filter_services_by_name(d, is_location_detail, 'Shelter'),
        "food_services": filter_services_by_name(d, is_location_detail, 'Food'),
        "clothing_services": filter_services_by_name(d, is_location_detail, 'Clothing'),
        "personal_care_services": filter_services_by_name(d, is_location_detail, 'Personal Care'),
        "health_services": filter_services_by_name(d, is_location_detail, 'Health'),
        "other_services": { "services": [ service for service in filter_services_by_name(d, is_location_detail)['services'] if not ({service["category"], service["subcategory"]} & {'Shelter', 'Food', 'Clothing', 'Personal Care', 'Health'}) ] },
        "closed": d['closed'],
    }

def map_gogetta_to_yourpeer_location_fields_only(d):
    print('d', d)
    location_id = d['id']
    coordinates = d['position']['coordinates']
    slug = Locations.objects.filter(id=location_id).first().slug
    return {
      "position": {
        "lat": coordinates[1],
        "lng": coordinates[0],
      },
     "lat": coordinates[1],
     "lng": coordinates[0],
      "closed": d['closed'],
      "slug": slug,
      "id": location_id,
      "title": d['name'],
    }

GO_GETTA_PROD_URL = environ.get('GO_GETTA_PROD_URL','https://w6pkliozjh.execute-api.us-east-1.amazonaws.com/prod')


def get_redirect_by_slug_from_gogetta_backend(slug):
    query_url = f"{GO_GETTA_PROD_URL}/location-slug-redirects/{slug}"
    print(query_url)
    response = requests.get(query_url)
    response.raise_for_status()
    return requests.get(query_url).json()

def get_location_by_slug_from_gogetta_backend(slug):
    query_url = f"{GO_GETTA_PROD_URL}/locations-by-slug/{slug}"
    print(query_url)
    response = requests.get(query_url)
    response.raise_for_status()
    yourpeer_response = map_gogetta_to_yourpeer(response.json(), True)
    print('yourpeer_response', json.dumps(yourpeer_response,indent=4)) 
    return yourpeer_response  

def get_location_from_gogetta_backend(location_id):
    query_url = f"{GO_GETTA_PROD_URL}/locations/{location_id}"
    print(query_url)
    response = requests.get(query_url)
    response.raise_for_status()
    return map_gogetta_to_yourpeer(response.json(), True)

def get_locations_from_gogetta_backend(page_num=None, page_size=None, taxonomies=None, taxonomy_specific_attributes = None, no_requirement = None, referral_required = None, membership = None, open_now = False, search = None, location_fields_only = False):
    # FIXME: we include COVID19 as query param here, in orde to make results match GoGetta's. But i's not technically correct, so we probably should remov eit at some point. 
    query_url = f"{GO_GETTA_PROD_URL}/locations?occasion=COVID19"

    if page_num is not None and page_size is not None:
        query_url += f"&pageNumber={page_num}&pageSize={page_size}"
    if location_fields_only:
        query_url += f'&locationFieldsOnly=true'
    if taxonomies:
        query_url += f"&taxonomyId={','.join([str(t.id) for t in taxonomies])}"
    if taxonomy_specific_attributes:
        query_url += '&' + '&'.join([f'taxonomySpecificAttribute[{i}]={a}' for i, a in enumerate(taxonomy_specific_attributes)])

    if no_requirement:
        if not referral_required:
            query_url += f'&referralRequired=false'
        if not membership:
            query_url += f'&membership=false'
    else:
        if referral_required is not None:
            query_url += f'&referralRequired={str(referral_required).lower()}'
        if membership is not None:
            query_url += f'&membership={str(membership).lower()}'

    if search:
        query_url += f'&searchString={search}'

    if open_now:
        query_url += f'&openAt={datetime.now().isoformat()}'

    print(query_url) 
    tic = time.perf_counter_ns()
    gogetta_response = requests.get(query_url)
    #import pdb
    #pdb.set_trace()
    number_of_pages = int(gogetta_response.headers.get('Pagination-Count','0'))
    result_count = int(gogetta_response.headers.get('Total-Count','0'))
    gogetta_response_json = gogetta_response.json()
    print('fetched in %d ms' % ((time.perf_counter_ns() - tic)/1000000))
    return number_of_pages, result_count, [ map_gogetta_to_yourpeer_location_fields_only(d) if location_fields_only else map_gogetta_to_yourpeer(d, False) for d in gogetta_response_json ]


def get_food_sql(page_num, page_size, food_type, search, open_now, location_fields_only):
    print("get_food_sql", food_type, search, open_now)
    food_pantry = food_type and "pantry" in food_type.lower()
    soup_kitchen = food_type and "kitchen" in food_type.lower()

    query = TAXONOMIES_BASE_SQL
    
    if food_pantry:
        query += "and t.name='Food Pantry'"
    elif soup_kitchen:
        query += "and t.name='Soup Kitchen'"
    else: 
        query += "and t.name='Food'"
    
    taxonomies = Taxonomies.objects.raw(query)
    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        search = search, 
        open_now = open_now,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )



def get_shelter_sql(page_num, page_size, is_single, is_family, search, open_now, location_fields_only):
    print("get_shelter_sql", search, open_now)
    query = TAXONOMIES_BASE_SQL

    if is_single:
        query += " and t.name = 'Single Adult' and t.parent_name = 'Shelter'"
    elif is_family:
        query += " and t.name = 'Families' and t.parent_name = 'Shelter'"
    else:
        query += " and t.name = 'Shelter'"

    taxonomies = Taxonomies.objects.raw(query)
    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        search = search, 
        open_now = open_now,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )


def get_clothing_sql(page_num, page_size, is_casual, is_professional, requires_referral, requires_registered_client, no_requirement, search, open_now, location_fields_only):
    print("get_clothing_sql", is_casual, is_professional, requires_referral, requires_registered_client, search, open_now)
    query = TAXONOMIES_BASE_SQL + " and t.name = 'Clothing'"

    taxonomies = Taxonomies.objects.raw(query)
    taxonomy_specific_attributes = []

    if is_casual:
        taxonomy_specific_attributes.append('clothingOccasion') 
        taxonomy_specific_attributes.append('everyday') 
    elif is_professional:
        taxonomy_specific_attributes.append('clothingOccasion') 
        taxonomy_specific_attributes.append('interview') 

    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        taxonomy_specific_attributes = taxonomy_specific_attributes,
        no_requirement = no_requirement,
        referral_required = requires_referral,
        membership = requires_registered_client,
        open_now = open_now,
        search = search,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )


def get_personal_care_sql(page_num, page_size, is_toiletries, is_shower, is_laundry, is_haircut, is_restrooms, requires_referral, requires_registered_client, no_requirement,  search, open_now, location_fields_only):
    print("get_personal_care_sql", is_toiletries, is_shower, is_laundry, is_haircut, is_restrooms, requires_referral, requires_registered_client, no_requirement, search, open_now)

    has_care_type = is_toiletries or is_shower or is_laundry or is_haircut or is_restrooms

    query = TAXONOMIES_BASE_SQL 
    if not has_care_type:
        query += " and t.name = 'Personal Care'"
    else:
        conditions = []
        if is_toiletries:
            conditions.append('Toiletries')
        if is_shower:
            conditions.append('Shower')
        if is_laundry:
            conditions.append('Laundry')
        if is_haircut:
            conditions.append('Haircut')
        if is_restrooms:
            conditions.append('Restrooms')

        conditions_in_quotes = [f"'{c}'" for c in conditions]
        query += f" and t.parent_name = 'Personal Care' and t.name in ({','.join(conditions_in_quotes) })"

    print('taxonomy sql query', query)
    taxonomies = Taxonomies.objects.raw(query)
    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        no_requirement = no_requirement,
        referral_required = requires_referral,
        membership = requires_registered_client,
        open_now = open_now,
        search = search,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )


def get_health_sql(page_num, page_size, search, open_now, location_fields_only):
    print("get_health_sql", search, open_now)
    query = TAXONOMIES_BASE_SQL + " and (t.name='Health' or t.parent_name = 'Health')"
    taxonomies = Taxonomies.objects.raw(query)
    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        open_now = open_now,
        search = search,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )


def get_other_sql(page_num, page_size, search, open_now, location_fields_only):
    print("get_other_sql", search, open_now)
    query = TAXONOMIES_BASE_SQL + " and (t.name = 'Other service' or t.parent_name = 'Other service')"
    taxonomies = Taxonomies.objects.raw(query)
    return get_locations_from_gogetta_backend(
        taxonomies = taxonomies,
        open_now = open_now,
        search = search,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )

def get_all_sql(page_num, page_size, search, open_now, location_fields_only):
    return get_locations_from_gogetta_backend(
        open_now = open_now,
        search = search,
        location_fields_only = location_fields_only,
        page_num=page_num,
        page_size=page_size,
    )
 
