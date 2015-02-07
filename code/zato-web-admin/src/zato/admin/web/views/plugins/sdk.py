# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
import logging

# Zato
from zato.admin.web.views import Index as _Index

class Index(_Index):
    method_allowed = 'GET'
    url_name = 'plugins-sdk'
    template = 'plugins/sdk.html'
    service_name = 'zato.plugins.sdk.get-list'