# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from django.apps import AppConfig


class StreetlivesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "streetlives"
