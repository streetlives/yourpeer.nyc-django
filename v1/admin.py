# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


from django.contrib import admin
from .models import *
from django.apps import apps


# register all the models from models.py
admin.site.register(apps.all_models['v1'].values())
