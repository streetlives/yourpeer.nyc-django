# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

# register URls
from django.conf import settings
from django.urls import path
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView

from . import views

def redirect_map(request):
    return HttpResponseRedirect("/locations/")

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us", views.about_us, name="about-us"),
    path("privacy-policy", views.privacy_policy, name="privacy-policy"),
    path("terms-of-use", views.terms_of_use, name="terms-of-use"),
    path("contact-us", views.contact_us, name="contact-us"),
    path("donate", views.donate, name="donate"),
    path("user-feedback", views.sign_up, name="user-feedback"),

  

    path("food", views.food_list, name="food"),
    path("food/", RedirectView.as_view(pattern_name="food", permanent=True) , name="food-redirect"),

    path("clothing", views.clothing_list, name="clothing"),
    path("clothing/", RedirectView.as_view(pattern_name="clothing", permanent=True) , name="clothing-redirect"),

    path("personal-care", views.personal_care_list, name="personal-care"),
    path("personal-care/", RedirectView.as_view(pattern_name="personal-care", permanent=True) , name="personal-care-redirect"),

    path("health-care", views.health_list, name="health"),
    path("health-care/", RedirectView.as_view(pattern_name="health", permanent=True) , name="health-redirect"),

    path("other-services", views.other_services_list, name="other-services"),
    path("other-services/", RedirectView.as_view(pattern_name="other-services", permanent=True) , name="other-services-redirect"),


    path("locations", views.map, name="map"),
    path("locations/", RedirectView.as_view(pattern_name='map',permanent=True), name="map-redirect"),

    path("locations/<slug:slug>", views.locations_slug, name="location-detail"),
    path("locations/<slug:slug>/", RedirectView.as_view(pattern_name='location-detail',permanent=True), name="map-redirect"),

    path("shelters-housing", views.shelters_housing_list, name="shelters-housing"),
    path("shelters-housing/", RedirectView.as_view(pattern_name='shelters-housing',permanent=True), name="shelters-housing-redirect"),

    path("shelters-housing/adult", views.shelters_housing_adult_list, name="shelters-housing-adult"),
    path("shelters-housing/adult/", RedirectView.as_view(pattern_name='shelters-housing-adult',permanent=True), name="shelters-housing-adult-redirect"),

    path("shelters-housing/families", views.shelters_housing_families_list, name="shelters-housing-families"),
    path("shelters-housing/families/", RedirectView.as_view(pattern_name='shelters-housing-families',permanent=True), name="shelters-housing-families-redirect"),


    path("food/pantry", views.food_pantry_list, name="food-pantry"),
    path("food/pantry/", RedirectView.as_view(pattern_name='food-pantry',permanent=True), name="food-pantry-redirect"),

    path("food/soup-kitchens", views.food_soup_kitchens_list, name="food-soup-kitchens"),
    path("food/soup-kitchens/", RedirectView.as_view(pattern_name='food-soup-kitchens',permanent=True), name="food-soup-kitchens-redirect"),

    path("clothing/casual", views.clothing_casual_list, name="clothing-casual"),
    path("clothing/casual/", RedirectView.as_view(pattern_name='clothing-casual',permanent=True), name="clothing-casual-redirect"),

    path("clothing/professional", views.clothing_professional_list, name="clothing-professional"),
    path("clothing/professional/", RedirectView.as_view(pattern_name='clothing-professional',permanent=True), name="clothing-professional-redirect"),


    path("personal-care/toiletries", views.personal_care_toiletries_list, name="personal-care-toiletries"),
    path("personal-care/toiletries/", RedirectView.as_view(pattern_name='personal-care-toiletries',permanent=True), name="personal-care-toiletries-redirect"),

    path("personal-care/restrooms", views.personal_care_restrooms_list, name="personal-care-restrooms"),
    path("personal-care/restrooms/", RedirectView.as_view(pattern_name='personal-care-restrooms',permanent=True), name="personal-care-restrooms-redirect"),

    path("personal-care/showers", views.personal_care_showers_list, name="personal-care-showers"),
    path("personal-care/showers/", RedirectView.as_view(pattern_name='personal-care-showers',permanent=True), name="personal-care-showers-redirect"),

    path("personal-care/laundry-services", views.personal_care_laundry_services_list, name="personal-care-laundry-services"),
    path("personal-care/laundry-services/", RedirectView.as_view(pattern_name='personal-care-laundry-services',permanent=True), name="personal-care-laundry-services-redirect"),


    path("personal-care/haircuts-barbers", views.personal_care_haircuts_barbers_list, name="personal-care-haircuts-barbers"),  
    path("personal-care/haircuts-barbers/", RedirectView.as_view(pattern_name='personal-care-haircuts-barbers',permanent=True), name="personal-care-haircuts-barbers-redirect"),

    path("organization", views.organization, name="organization"),
    path("organization/", RedirectView.as_view(pattern_name='organization',permanent=True), name="organization-redirect"),

    path("report", views.email_issue_report, name="report"),

    path("map/", redirect_map, name="redirect_map"),

    path("map/", redirect_map, name="redirect_map"),

    path("geocode/analytics/all", views.proxy_get, name="redirect_map"),
] 

if settings.IS_BACKEND:
    urlpatterns += [
        path("", views.health_check, name="health-check")
    ]
