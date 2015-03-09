# -*- coding: utf-8 -*-

"""
Copyright (C) 2014 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# stdlib
from logging import getLogger
from traceback import format_exc

# gevent
from gevent.lock import RLock

import odoorpc

# Zato
from zato.common.util import ping_odoo
from zato.server.connection.queue import ConnectionQueue

# ################################################################################################################################

logger = getLogger(__name__)

# ################################################################################################################################

class OdooWrapper(object):
    """ Wraps a queue of connections to Odoo.
    """
    def __init__(self, config, server):
        self.config = config
        self.server = server
        self.url = '{protocol}://{user}:******@{host}:{port}/{database}'.format(**self.config)
        self.client = ConnectionQueue(
            self.config.pool_size, self.config.queue_build_cap, self.config.name, 'Odoo', self.url, self.add_client)

        self.update_lock = RLock()
        self.logger = getLogger(self.__class__.__name__)

    def build_queue(self):
        with self.update_lock:
            self.client.build_queue()

    def add_client(self):

        conn = odoorpc.ODOO(self.config.host, protocol=self.config.protocol, port=self.config.port)
        try:
            conn.login(self.config.database, self.config.user, self.config.password)
        except Exception, e:
            logger.warn('Could not connect to Odoo (%s), e:`%s`', self.config.name, format_exc(e))

        try:
            ping_odoo(conn)
        except Exception, e:
            logger.warn('Could not ping Odoo (%s), e:`%s`', self.config.name, format_exc(e))

        self.client.put_client(conn)
