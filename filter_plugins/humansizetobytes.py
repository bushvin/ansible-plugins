#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2015, William Leemans <willie@elaba.net>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import math

UNITS = {
      'decimal': { 'units': [ 'B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y' ],
                   'factor': 1000
                 },
      'binary': {  'units': [ 'Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi' ],
                   'factor': 1024
                   }
      }

def humansizetobytes(size):
   size_org = size
   n = ""
   while size and size[0:1].isdigit() or size[0:1] == '.':
      n = n + size[0]
      size = size[1:]

   n = float(n)
   unit = size.strip()
   if unit == 'k':
      unit = 'K'
   for setname, setinfo in UNITS.items():
      if unit in setinfo['units']:
         idx = setinfo['units'].index(unit)
         factor = setinfo['factor']
         break
   else:
     raise ValueError("error interpreting %r" % size_org)
   return int(n * math.pow(factor,idx))

class FilterModule(object):
   def filters(self):
      return {
            'humansizetobytes': humansizetobytes
            }
