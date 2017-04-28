ansible-plugins
===============

These are my custom plugins I've written for Ansible (https://github.com/ansible/ansible):

## vars_plugins/
### user_dir_vars.py
This plugin mimicks the behavior of group_vars and host_vars in the inventory and playbook in the user's home directory (~/.ansible to be exact).
`_host_allowed_facts` and `_group_allowed_facts` can be empty (allow any facts) or contain a list, in which case it will filter out any other facts.
## filter_plugins
### humansizetobytes.py
This plugin adds a jinja filter to your runtime (humansizetobytes) which converts Human readable sizes into bytes.

