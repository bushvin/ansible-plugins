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

import os
from ansible import utils
from ansible import errors
import ansible.constants as C

class VarsModule(object):


    _base_host_vars = "~/.ansible/host_vars"
    _base_group_vars = "~/.ansible/group_vars"
    _host_allowed_facts =  [ 'ansible_ssh_user', 'ansible_ssh_pass', 'ansible_sudo', 'ansible_sudo_pass', 'ansible_ssh_private_key_file', 'ansible_become', 'ansible_become_user', 'ansible_become_pass' ]
    _group_allowed_facts = [ 'ansible_ssh_user', 'ansible_ssh_pass', 'ansible_sudo', 'ansible_sudo_pass', 'ansible_ssh_private_key_file', 'ansible_become', 'ansible_become_user', 'ansible_become_pass' ]

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()
        self._base_host_vars = os.path.expanduser(self._base_host_vars)
        self._base_group_vars = os.path.expanduser(self._base_group_vars)


    def run(self, host, vault_password=None):
        """ For backwards compatibility, when only vars per host were retrieved
            This method should return both host specific vars as well as vars
            calculated from groups it is a member of """
        result = {}
        result.update(self.get_host_vars(host, vault_password))
        
        for g in host.groups:
            result.update(self.get_group_vars(g,vault_password))
            if C.DEFAULT_HASH_BEHAVIOUR == "merge":
                result = utils.merge_hash(result, data)
            else:
                result.update(data)
        return result


    def get_host_vars(self, host, vault_password=None):
        result = {}
        
        filename = os.path.join(self._base_host_vars, "%s.yml" % host.name)
        if os.path.isfile( filename ):
            res = utils.parse_yaml_from_file(filename, vault_password=vault_password)
            if type(res) != dict:
                raise errors.AnsibleError("%s must be stored as a dictionary/hash" % filename)
            data = dict()
            for el in res:
                if len(self._host_allowed_facts) == 0 or el in self._host_allowed_facts:
                    data.update( { el: res[el] } )
            result.update(data)
                
        return result


    def get_group_vars(self, group, vault_password=None):
        result = {}
        
        filename = os.path.join(self._base_group_vars, "%s.yml" % group.name)
        if os.path.isfile( filename ):
            res = utils.parse_yaml_from_file(filename, vault_password=vault_password)
            if type(res) != dict:
                raise errors.AnsibleError("%s must be stored as a dictionary/hash" % filename)
            data = dict()
            for el in res:
                if len(self._group_allowed_facts) == 0 or el in self._group_allowed_facts:
                    data.update( { el: res[el] } )
            result.update(data)

        return result
