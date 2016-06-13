# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# Copyright (C) 2016 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Manage the Glances ports list (Ports plugin)."""

from glances.compat import range
from glances.logger import logger


class GlancesPortsList(object):

    """Manage the ports list for the ports plugin."""

    _section = "ports"
    _default_refresh = 60
    _default_timeout = 3

    def __init__(self, config=None, args=None):
        # ports_list is a list of dict (JSON compliant)
        # [ {'host': 'www.google.fr', 'port': 443, 'refresh': 30, 'description': Internet, 'status': True} ... ]
        # Load the configuration file
        self._ports_list = self.load(config)

    def load(self, config):
        """Load the ports list from the configuration file."""
        ports_list = []

        if config is None:
            logger.debug("No configuration file available. Cannot load ports list.")
        elif not config.has_section(self._section):
            logger.warning("No [%s] section in the configuration file. Cannot load ports list." % self._section)
        else:
            logger.debug("Start reading the [%s] section in the configuration file" % self._section)
            refresh = config.get_value(self._section, 'refresh', default=self._default_refresh)
            timeout = config.get_value(self._section, 'timeout', default=self._default_timeout)
            for i in range(1, 256):
                new_port = {}
                postfix = 'port_%s_' % str(i)

                # Read mandatories configuration keys: host and port
                for s in ['host', 'port']:
                    new_port[s] = config.get_value(self._section, '%s%s' % (postfix, s))

                if new_port['host'] is None or new_port['port'] is None:
                    continue

                # Read optionals configuration keys
                new_port['description'] = config.get_value(self._section,
                                                           '%sdescription' % postfix,
                                                           default="%s:%s" % (new_port['host'], new_port['port']))

                # Default status
                new_port['status'] = None

                # Refresh rate in second
                new_port['refresh'] = refresh

                # Timeout in second
                new_port['timeout'] = timeout

                # Add the server to the list
                logger.debug("Add port %s:%s to the static list" % (new_port['host'], new_port['port']))
                ports_list.append(new_port)

            # Ports list loaded
            logger.debug("Ports list loaded: %s" % ports_list)

        return ports_list

    def get_ports_list(self):
        """Return the current server list (dict of dict)."""
        return self._ports_list

    def set_server(self, pos, key, value):
        """Set the key to the value for the pos (position in the list)."""
        self._ports_list[pos][key] = value