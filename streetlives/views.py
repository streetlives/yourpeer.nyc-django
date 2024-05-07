# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from datetime import datetime, timedelta
import json
import os
import pytz
import requests
import csv
import math
from django.http import HttpResponse, JsonResponse, HttpResponsePermanentRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.template import Template, Context
from django.core.paginator import Paginator
from v1.models import Locations 
from v1.models import VwOrgsFood
from v1.models import VwOrgsAccommodations
from v1.models import VwOrgsClothing
from v1.models import VwOrgsHealth
from v1.models import VwOrgsOtherServices
from v1.models import VwOrgsPersonalCare
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sitemaps import Sitemap
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from streetlives.sql import *
from django.db.models.query import RawQuerySet
from django.views.decorators.cache import cache_page
import requests 

DEFAULT_PAGE_SIZE=20


logger = logging.getLogger(__name__)

def health_check(request):
    return HttpResponse("OK")

# homepage view
def home(request):
    return render(request, "home/home.html")


# About us view
def about_us(request):
    return render(request, "about_us.html")


# privacy policy view
def privacy_policy(request):
    return render(request, "privacy_policy.html")


# terms of use view
def terms_of_use(request):
    return render(request, "terms_of_use.html")


# Contact us view
def contact_us(request):
    return render(request, "contact_us.html")


# Contact us view
def donate(request):
    return render(request, "donate.html")

def sign_up(request):
    response = redirect('https://forms.gle/iDeQigu5GpNf9A286')
    return response



def concat_service_list(list):
    final = ""
    counter = 0
    for item in list:
        if counter != 0:
            final += " • "
        final += item.name


def mixin_search_and_open_now(query, search, open_now):
    if search:
        query = query.filter(Q(data__icontains=search))
    if open_now:
        todays_integer = get_today_integer()
        est = pytz.timezone('US/Eastern')
        current_time_in_EST = datetime.now(est)
        query = query.filter(Q(location__serviceatlocations__service__holidayschedules__weekday=todays_integer) & 
                                               Q(location__serviceatlocations__service__holidayschedules__opens_at__lte = current_time_in_EST) &
                                               Q(location__serviceatlocations__service__holidayschedules__closes_at__gte = current_time_in_EST))
    return query

def get_locations(page, page_size, filters=None, location_fields_only=False) -> RawQuerySet:
    # TODO: we need to pass through location_fields_only param to all of the below queries
    logger.info("#########")
    logger.info("filteres" + " " + str(filters))
    logger.info("#########")
    queries = []

    search_term = filters.get("search")
    open_now = filters.get("open_now") == 'yes'

    num_pages = None
    result_count = None
    locations = None
    results = None

    if filters.get("food"):
        results = get_food_sql(page, page_size, filters.get("food_type"), search_term, open_now, location_fields_only)

    elif filters.get("shelter"):
        is_single = filters.get("shelter") and "single" in filters.get("shelter")
        is_family = filters.get("shelter") and "family" in filters.get("shelter")
        results = get_shelter_sql(page, page_size, is_single, is_family, search_term, open_now, location_fields_only)

    elif filters.get("clothing"):
        is_casual = filters.get("clothing") and "casual" in filters.get("clothing")
        is_professional = filters.get("clothing") and "professional" in filters.get("clothing")
        requires_referral = filters.get("requirement") and "referral-letter" in filters.get("requirement")
        requires_registered_client = filters.get("requirement") and "registered-client" in filters.get("requirement")
        no_requirement = filters.get("requirement") and "no" in filters.get("requirement")
        results = get_clothing_sql(page, page_size, is_casual, is_professional, requires_referral, requires_registered_client, no_requirement, search_term, open_now, location_fields_only)

    elif filters.get("personal_care"):
        is_toiletries = filters.get("personal_care") and "toiletries" in filters.get("personal_care")
        is_restrooms = filters.get("personal_care") and "restrooms" in filters.get("personal_care")
        is_showers = filters.get("personal_care") and "shower" in filters.get("personal_care")
        is_laundry = filters.get("personal_care") and "laundry" in filters.get("personal_care")
        is_haircuts = filters.get("personal_care") and "haircut" in filters.get("personal_care")

        requires_referral = filters.get("requirement") and "referral-letter" in filters.get("requirement")
        requires_registered_client = filters.get("requirement") and "registered-client" in filters.get("requirement")
        no_requirement = filters.get("requirement") and "no" in filters.get("requirement")

        results = get_personal_care_sql(page, page_size, is_toiletries, is_showers, is_laundry, is_haircuts, is_restrooms, requires_referral, requires_registered_client, no_requirement, search_term, open_now, location_fields_only)

    elif filters.get("health"):
        results = get_health_sql(page, page_size, search_term, open_now, location_fields_only)

    elif filters.get("other"):
        results = get_other_sql(page, page_size, search_term, open_now, location_fields_only)

    else: 
        results = get_all_sql(page, page_size, search_term, open_now, location_fields_only)

    return results

    

def query_string_or_filter(request, filters, key, is_multiple=False):
    if is_multiple:
        if request.GET.getlist(key, False):
            return request.GET.getlist(key, False)
    if request.GET.get(key, False):
        return request.GET.get(key, False)
    if filters and filters.get(key, False):
        return filters.get(key, False)
    
    return None


# @cache_page(60 * 15)
def map(request, slug=None, title=None, description=None, filters= None):
    logger.info("map view")


    page = None
    page_str = request.GET.get("page", None)
    if page_str is not None:
        page = int(page_str) - 1 # page is zero-indexed, but page query-param is one-indexed

    # values= any value for true, no querystring for false
    open_now = query_string_or_filter(request, filters, "open")

    food = query_string_or_filter(request, filters, "food")
    # values= pantry, soup_kitchen, or no filter

    shelter = query_string_or_filter(request, filters, "shelter")
    # values= single_adult, families, or no filter

    clothing = query_string_or_filter(request, filters, "clothing")
    # values= casual, professional, or no filter
    # values = referral_letter, registered_client, or none
    # you can comma separate these values to get multiple
    requirement_types = query_string_or_filter(request, filters, "requirement", True)
    if requirement_types:
        requirement_types = requirement_types[0]

    personal_care = None
    
    if filters and filters.get("personal-care", False):
        personal_care = filters.get("personal-care")
    else:
        personal_care = query_string_or_filter(request, filters, "personal-care")
    # values= toiletries, restrooms, showers, laundry, haircuts
    # you can comma separate these values to get multiple


    health = query_string_or_filter(request, filters, "health")
    other = query_string_or_filter(request, filters, "other")

    search = query_string_or_filter(request, filters, "search")

    is_advanced_filters = query_string_or_filter(request, filters, "adv")

                
    canonical_url = request.build_absolute_uri(request.path)

    is_htmx = False
    if "HTTP_HX_PUSH_URL" in request.META:
        is_htmx = True

    # merge the filters
    if filters is None:
        filters = {}

    new_filters = {
        "food": food,
        "shelter": shelter,
        "clothing": clothing,
        "personal_care": personal_care,
        "health": health,
        "other": other,
        "open_now": open_now,
        "food_type": food,
        "shelter": shelter,
        "shelter_type": shelter,
        "clothing_type": clothing,
        "requirement": requirement_types,
        "search": search
    }
    filters.update(new_filters)

    page_size = DEFAULT_PAGE_SIZE

    if request.GET.get("json", False):
        page = 0
        page_size = 999999
        num_pages, count, locations = get_locations(page, page_size, filters, True)
        return JsonResponse({"locations": locations, "count": count}, status=200)
    else:
        if page == None:
            page = 0
        
    title = "All Locations | YourPeer"
    description = "See all locations hosted on YourPeer offering essential resources, shelters, food pantries, and more in NYC."

    num_pages, count, locations = get_locations(page, page_size, filters)

    page = 0 if page == None else page
    has_previous = page > 0
    has_next = page < (num_pages - 1)
    display_page_num = page + 1
    next_page_number = display_page_num + 1 if page < num_pages else None
    previous_page_number = display_page_num - 1 if page > 0 else None

    response_obj = {
            "locations": locations,
            "page": display_page_num,
            "count":count,
            "page_size": page_size,
            "slug": slug,
            "canonical_url": canonical_url,
            "page_title": title,
            "page_description": description,
            "current_page": page + 1,
            "total_pages": num_pages,
            "next_page_number": next_page_number,
            "previous_page_number": previous_page_number,
            "has_previous": has_previous,
            "has_next": has_next,
            "is_food": food,
            "is_not_food": not food,
            "is_shelter": shelter,
            "is_not_shelter": not shelter,
            "is_clothing": clothing,
            "is_not_clothing": not clothing,
            "is_personal_care": personal_care,
            "is_not_personal_care": not personal_care,
            "is_health": health,
            "is_not_health": not health,
            "is_other": other,
            "is_not_other": not other,
            "is_open_now": open_now,
            "is_not_open_now_query": not open_now,
            "is_not_filter": not food and not shelter and not clothing and not personal_care and not health and not other,
            "is_filter": food or shelter or clothing or personal_care or health or other,
            "search": search,
            "is_advanced_filters": is_advanced_filters,
            "is_shelter_type_any": isinstance(shelter,str)  and "single" not in shelter and "families" not in shelter,
            "is_shelter_type_single_adult": shelter and "single" in shelter,
            "is_shelter_type_families": shelter and "family" in shelter,
            "is_food_type_any": isinstance(food,str) and not "pantry" in food and not "kitchen" in food,
            "is_food_type_pantry": food and "pantry" in food,
            "is_food_type_soup_kitchen": food and "kitchen" in food,
            "is_clothing_type_any": isinstance(clothing,str) and not "casual" in clothing and not "professional" in clothing,
            "is_clothing_type_casual": clothing and "casual" in clothing,
            "is_clothing_type_professional": clothing and "professional" in clothing,
            "is_personal_care_type_any": isinstance(personal_care,str) and not "toiletries" in personal_care and not "restrooms" in personal_care and not "showers" in personal_care and not "laundry" in personal_care and not "haircuts" in personal_care,
            "is_personal_care_type_toiletries": personal_care and "toiletries" in personal_care,
            "is_personal_care_type_restrooms": personal_care and "restrooms" in personal_care,
            "is_personal_care_type_showers": personal_care and "shower" in personal_care,
            "is_personal_care_type_laundry": personal_care and "laundry" in personal_care,
            "is_personal_care_type_haircuts": personal_care and "haircut" in personal_care,
            "is_requirement_types_none": requirement_types and 'no' in requirement_types,
            "is_requirement_types_referral_letter": requirement_types and "referral-letter" in requirement_types,
            "is_requirement_types_registered_client": requirement_types and "registered-client" in requirement_types,

        };
    # logger.info("======")
    # logger.info("response obj is " + str(response_obj))
    # logger.info("======")
    response = render(
        request,
        "map/map.html",
        response_obj
    )
    
    if is_htmx:
        response["HX-Push-Url"] = request.build_absolute_uri()
    return response


# change this to take an id or slug to specify the organization
def organization(request):
    return render(request, "organizations/organization.html")
    


# /locations
# "/locations/[location name] + [area]

# Example:
# Safe Horizon Streetwork Project
# /locations/safe-horizon-streetwork-project-harlem"

# /shelters-housing
# /shelters-housing/adult
# /shelters-housing/families

# /food
# /food/pantry
# /food/soup-kitchens

# /clothing
# /clothing/casual
# /clothing/professional

# /personal-care
# /personal-care/toiletries
# /personal-care/restrooms
# /personal-care/showers
# /personal-care/laundry-services
# /personal-care/haircuts-barbers

# /health-care



import traceback
import sys
def locations_slug(request, slug=None):
    logger.info("slug is " + slug)
    

    # TODO: redirects
    this_location = None
    response = None
    if slug is not None:
        # lookup slug and redirect
        this_location = None
        try:
            this_location = get_location_by_slug_from_gogetta_backend(slug)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code != 404:
                raise e # rethrow for anything other than 404

            # if we did get a 404, we can try to look up the redirect
            try:
                redirect = get_redirect_by_slug_from_gogetta_backend(slug)
                return HttpResponsePermanentRedirect(f'/locations/{redirect["slug"]}')

            except requests.exceptions.HTTPError as e:
                if e.response.status_code != 404:
                    raise e # rethrow for anything other than 404

                return HttpResponseNotFound()

        if this_location is not None:
            logger.info("json is " + str(request.META.get("json", False)))

            map_location = this_location

            with open(os.path.join(settings.BASE_DIR, "data/custom-streetviews.json")) as f:
                custom_cordinates = json.loads(f.read())
                slug = this_location.get('slug')

                if slug in custom_cordinates:
                    this_location['streetview'] = custom_cordinates[slug]
        
            if request.GET.get("json", False):
                response =  JsonResponse({"locations":[this_location]}, status=200)
                # response["HX-Push-Url"] = request.build_absolute_uri()
                return response

            response =  render(
                request,
                "map/map.html",
                {
                    "slug": slug,
                    "location_id": this_location["id"],
                    "location": this_location,
                    "page_title": this_location["area"]
                    + " "
                    + this_location["name"]
                    + " | YourPeer",
                    "page_description": this_location["name"] + " | YourPeer",
                },
            )
    # print("HX_PUSH is " + request.META.get("HTTP_HX_PUSH_URL", False))
    if request.META.get("HTTP_HX_PUSH_URL", False):
        print("pushing slug " + slug)
        response = map(request)
        response["HX-Push-Url"] = request.build_absolute_uri()
    
    return response
    
    



class LocationSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return [ f'/locations/{slug}' for slug in Locations.objects.values_list('slug', flat=True) ]

    def location(self, item):
        return item
    

def shelters_housing_list(request):
    title = "Shelters & Housing For Unhoused People In NYC | YourPeer"
    description = "Find safe accomodations options for unhoused individuals in NYC. Access our resources to help you find stable housing and support on your journey towards housing stability."
    return map(request, title=title, description=description, filters={"shelter": "yes", "housing": "yes"})


def shelters_housing_adult_list(request):
    title = "Adult Housing For Unhoused People In NYC | YourPeer"
    description = "Discover housing and accomodations for unhoused adults in NYC at YourPeer. Our network of resources aim to provide safe housing options for adults experiencing homelessness."
    return map(request, title=title, description=description, filters={"shelter": "single"})

def shelters_housing_families_list(request):
    title = "Family Shelters & Housing For Unhoused People In NYC | YourPeer"
    description = "Find family shelters and housing for unhoused people in NYC. Explore all of our family resources to ensure your family's well-being and find the support you need."
    return map(request, title=title, description=description, filters={"shelter": "families"})


# food category
def food_list(request):
    title = "Food For Unhoused People In NYC | YourPeer"
    description = "Access food resources for unhoused individuals in NYC through YourPeer. Find various food programs to alleviate hunger and receive much-needed nourishment in times of need."
    return map(request, title=title, description=description, filters={"food": "yes"})

def food_pantry_list(request):
    title = "Food Pantries For Unhoused People In NYC | YourPeer "
    description = "YourPeer connects unhoused people with local food pantries in NYC, providing sustenance during challenging times. Use YourPeer to find nearby food pantries offering food assistance."
    return map(request, title=title, description=description, filters={"food": "pantry", "food_type": "pantry"})

def food_soup_kitchens_list(request):
    title = "Soup Kitchens For Unhoused People In NYC | YourPeer"
    description = "Find soup kitchens and warm meals with YourPeer. Access nourishing meals and connect with caring communities through our comprehensive network of resources."
    return map(request, title=title, description=description, filters={"food": "kitchen", "food_type": "soup_kitchen"})

def clothing_list(request):
    title = "Free Clothing For Unhoused People In NYC | YourPeer"
    description = "Find resources offering free clothing for unhoused individuals in NYC with YourPeer.  Explore our resources for a range of clothing options to meet your specific needs."
    return map(request, title=title, description=description, filters={"clothing": "yes"})

def clothing_casual_list(request):
    title = "Free Casual Clothing For Unhoused People In NYC | YourPeer"
    description = "Easily find locations and resources offering free casual clothing for unhoused individuals in NYC at YourPeer."
    return map(request, title=title, description=description, filters={"clothing": "casual", "casual": True})

def clothing_professional_list(request):
    title = "Free Professional Clothing For Unhoused People In NYC | YourPeer"
    description = "Find locations and resources offering professional clothing for unhoused individuals in NYC at YourPeer."
    return map(request, title=title, description=description, filters={"clothing": "professional", "professional": True})

def personal_care_list(request):
    print("personal care list")
    title = "Personal Care Resources For Unhoused People In NYC | YourPeer"
    description = "Find personal care resources for unhoused individuals in NYC through YourPeer. Discover a range of services and resources for additional support. "
    return map(request, title=title, description=description, filters={"personal-care": "yes"})

def personal_care_toiletries_list(request):
    title = "Toiletries For Unhoused People In NYC | YourPeer"
    description = "Find toiletries and hygiene essentials for unhoused individuals in NYC with YourPeer. Access resources to ensure you have the necessary items for personal care and well-being."
    personal_care = query_string_or_filter(request, None, "personal-care")
    if personal_care:
        personal_care +="+toiletries"
    else:
        personal_care = "toiletries"
    return map(request, title=title, description=description, filters={"personal-care": personal_care})

def personal_care_restrooms_list(request):
    title = "Restrooms For Unhoused People In NYC | YourPeer"
    description = "YourPeer provides information on accessible restrooms in NYC for unhoused individuals. Discover safe and clean facilities to meet your restroom needs with our support."
    personal_care = query_string_or_filter(request, None, "personal-care")
    if personal_care:
        personal_care +="+restrooms"
    else:
        personal_care = "restrooms"
    return map(request, title=title, description=description, filters={"personal-care": personal_care})

def personal_care_showers_list(request):
    title = "Showers For Unhoused People In NYC | YourPeer"
    description = "Find shower facilities for unhoused individuals in NYC at YourPeer. Access showers and hygiene resources  to help you stay clean and refreshed during challenging times."
    personal_care = query_string_or_filter(request, None, "personal-care")
    if personal_care:
        personal_care +="+showers"
    else:
        personal_care = "showers"
    return map(request, title=title, description=description, filters={"personal-care": personal_care, "showers": True})

def personal_care_laundry_services_list(request):
    title = "Free Laundry Services For Unhoused People In NYC | YourPeer"
    description = "YourPeer connects unhoused individuals in NYC with free laundry services and locations. Explore our resources to find nearby laundry facilities."
    personal_care = query_string_or_filter(request, None, "personal-care")
    if personal_care:
        personal_care +="+laundry"
    else:
        personal_care = "laundry"
    

    return map(request, title=title, description=description, filters={"personal-care": personal_care, "laundry_services": True})

def personal_care_haircuts_barbers_list(request):
    title = "Haircuts & Barber For Unhoused People In NYC | YourPeer"
    description = "Find locations offering haircuts and barber services for unhoused individuals in NYC, with YourPeer. Access our resources for additional support. "
    personal_care = query_string_or_filter(request, None, "personal-care")
    if personal_care:
        personal_care +="+haircuts"
    else:
        personal_care = "haircuts"
    return map(request, title=title, description=description, filters={"personal-care": personal_care, "haircuts_barbers": True})

def health_list(request):
    title = "Health Care Services & Centers For Unhoused People | YourPeer"
    description = "Find health care services and centers for unhoused people in NYC. Take advantage of our support network and prioritize your health and well-being. "
    return map(request, title=title, description=description, filters={"health": "yes"})

def other_services_list(request):
    title = "Other Resources & Services For Unhoused People In NYC | YourPeer"
    description = "Discover information about all resources and services offered by locations hosted on YourPeer in NYC. "
    return map(request, title=title, description=description, filters={"other": "yes"})


def email_issue_report(request):
    print("emailing issue report")
    if request.method == "POST":
        print("emailing issue report")
        data = request.body.decode("utf-8")
        print("data is " + data)
        print("emailing issue report")

        subject = 'New Issue Report'
        from_email = 'micah@streetlives.nyc'
        #to = ['micah@streetlives.nyc']
        to = ['ypissuereport@streetlives.nyc']
        send_mail(subject, data, from_email, to, fail_silently=False)
    return HttpResponse("OK")
