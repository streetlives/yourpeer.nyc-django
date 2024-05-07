# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.


# A script that's needed to setup django if it's not already running on a server.
# Without this, you won't be able to import django modules
import sys, os, django

#BASE_DIR="/Users/micahsmith/dev/sl/streetlives_v2/"


# Find the project base directory
BASE_DIR = BASE_DIR or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Add the project base directory to the sys.path
# This means the script will look in the base directory for any module imports
# Therefore you'll be able to import analysis.models etc
sys.path.insert(0, BASE_DIR)

# The DJANGO_SETTINGS_MODULE has to be set to allow us to access django imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# This is for setting up django
django.setup()


from v1.models import *

# get_user_model
from django.contrib.auth import get_user_model




