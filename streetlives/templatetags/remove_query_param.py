# Copyright (c) 2024 Streetlives, Inc.
# 
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

from django.template import Library
from urllib.parse import urlencode, urlparse, parse_qs

register = Library()

def remove_query_param(querydict, param):
    querydict_copy = querydict.copy()
    querydict_copy.pop(param, None)
    return querydict_copy.urlencode()

register.filter('remove_query_param', remove_query_param)
