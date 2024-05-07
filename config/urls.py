# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


"""ia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, reverse
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap


from streetlives import urls
from config import settings
from streetlives.views import LocationSitemap

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("", include("streetlives.urls")),
    path("sadmin/", admin.site.urls),
    path("", include('pwa.urls'))
]

# if we're not in live serve a disallow to all user-agents via robots.txt
if not settings.IS_LIVE:
    urlpatterns
    urlpatterns += [
        path(
            "robots.txt",
            lambda x: HttpResponse(
                "User-Agent: *\nDisallow: /", content_type="text/plain"
            ),
            name="robots_file",
        )
    ]
else:
    urlpatterns += [
        path(
            "robots.txt",
            lambda x: HttpResponse(
                "User-Agent: *\nAllow: /", content_type="text/plain"
            ),
            name="robots_file",
        )
    ]

# add in the static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# generate the static stiemap
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        # return the pages we added into the urlpatterns above
        return [
            "home",
            "about-us",
            "privacy-policy",
            "terms-of-use",
            "contact-us",
            "donate",
            "food",
            "clothing",
            "personal-care",
            "health",
            "other-services",
            "shelters-housing",
            "shelters-housing-adult",
            "shelters-housing-families",
            "food-pantry",
            "food-soup-kitchens",
            "clothing-casual",
            "clothing-professional",
            "personal-care-toiletries",
            "personal-care-restrooms",
            "personal-care-showers",
            "personal-care-laundry-services",
            "personal-care-haircuts-barbers",
            "organization",
            "map",
        ]
    
    def location(self, item):
        return reverse(item)


# add in the sitemap.xml
urlpatterns += [
    path("sitemap.xml", sitemap, {"sitemaps": {
        "static": StaticViewSitemap,
        "locations": LocationSitemap
        }})
]
