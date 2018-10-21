import configparser
'''
Global varialbes are varialbes defined previously
in the group_vars/ or host_vars/ directories
'''
GLOBAL_VARS = {
   'ADMIN_PASS',
   'CINDER_DBPASS',
   'CINDER_PASS',
   'DASH_DBPASS',
   'DEMO_PASS',
   'GLANCE_DBPASS',
   'KEYSTONE_DBPASS',
   'METADATA_SECRET',
   'NEUTRON_DBPASS',
   'GLANCE_PASS',
   'NEUTRON_PASS',
   'NOVA_DBPASS',
   'NOVA_PASS',
   'PLACEMENT_PASS',
   'RABBIT_PASS',
   'PROVIDER_INTERFACE_NAME',
   'OVERLAY_INTERFACE_IP_ADDRESS',
   'MANAGEMENT_INTERFACE_IP_ADDRESS',
   'PRIVATE_ADDRESS',
   'PRIVATE_NETWORK',
   'TIME_ZONE'
}

OTHER_VARS = {
	'controller': 'HOST_NAME',
    '10.0.0.11': 'PRIVATE_ADDRESS',
    '10.0.0.0/24': 'PRIVATE_NETWORK',
}

def replace_vars(line):
	'''
	Example: This is my ADMIN_PASS -> "This is my {{ ADMIN_PASS }}"
	'''
	res = line
	for item in GLOBAL_VARS:
		if line.find(item) != -1:
			res = line.replace(item, '{{ ' + item + ' }}')
	for item in OTHER_VARS:
		if line.find(item) != -1:
			res = line.replace(item, '{{ '+ OTHER_VARS[item] + ' }}')
	return '"{}"'.format(res)

def readlines(file):
	'''
	Read file line by line, excluding the '\n' character
	at the end of each line and discard all blank line 
	'''
	with open(file, 'r') as f:
		return list(filter(None, ''.join(f.readlines()).split('\n')))

def ini2yaml(ini_file, yaml_dict_name):
	'''
	Convert an ini_file to a YAML dict
	'''
	ini_config = configparser.ConfigParser()
	ini_config.read(ini_file)
	result = [yaml_dict_name+':']
	for name, section in ini_config.items():
		result.append('  - name: {}'.format(name))
		result.append('    attributes:')
		for option, value in section.items():
			result.append('      - option: {}'.format(option))
			result.append('        value: {}'.format(replace_vars(value)))
	return '\n'.join(result)

def ini_file(name, path, yaml_dict_name):
	res = \
	'''
- name: {}
  ini_file:
    path: {}
    section: "{{{{ item.0.name }}}}"
    option: "{{{{ item.1.option }}}}"
    value: "{{{{ item.1.value }}}}"
    backup: yes
  with_subelements:
    - " {{{{ {} }}}}"
    - attributes
	'''
	return res.format(name, path, yaml_dict_name)

def apt(package_file, name, state='present'):
	res = '- name: {}\n  apt:\n    name: "{{{{ item }}}}"\n    state: {}\n  with_items:'
	res = [res.format(name, state)]
	for pkg in readlines(package_file):
		res.append('    - {}'.format(pkg))
	return '\n'.join(res)

def shell(command_file, name, sql=False, environment=None):
	res = '- name: {}\n  shell: "{{{{ item }}}}"\n  with_items:'
	res = [res.format(name)]
	for command in readlines(command_file):
		if sql:
			res.append('    - {}'.format('mysql --execute ' + replace_vars(command)))
		else:
			res.append('    - {}'.format(replace_vars(command)))
	if environment is not None:
		res.append('  environment: ' + replace_vars(environment))
	
	return '\n'.join(res)

if __name__ == '__main__':
	return