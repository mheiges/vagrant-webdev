#!/usr/bin/env python

'''
Dynamic Ansible inventory.

  - Get /dashboard connection from installsite.yml which
  includes the entry
        dashboard:
          hostname: w1.trichdb.org
  - download /dashboard/json to file hosthame_dashboard.json
  - merge installsite.yml into hosthame_dashboard.json

Final website variables are under the 'ebrc' namespace.

    {
      "all": {
        "vars": {
          "ebrc": {
            "httpd": {
              "basic_auth_required": false, 
              "vhost": "sa.vm.trichdb.org"
            }, 
            "wdk": {
              "buildnumber": "31", 
        ...

'''

import yaml
import json
import re
import urllib2
from ansible.utils.vars import merge_hash

usersettings_file = 'installsite.yml'

def main():
  usersettings = load_settings_file(usersettings_file)
  dashboardsettings_file = fetch_dashboard_json_to_file(usersettings['dashboard'])
  dashboardsettings = load_settings_file(dashboardsettings_file)
  presettings = reduce(merge_hash, [dashboardsettings, usersettings])
  settings = reduce(merge_hash, [presettings, derived_settings(presettings)])
  print(json.dumps(inventory(settings), sort_keys=True, indent=2))

def inventory(settings):
  return {
    'all': {
      'vars': {
        'ebrc': settings,
      }
    }
  }

def derived_settings(presettings):
  regex = re.compile(r'^jdbc:[^@]+@', re.IGNORECASE)
  return {
    'website': {
      '_path': '/var/www/' + presettings['wdk']['modelname'] + '/' + presettings['tomcat']['webapp']
    },
    'wdk': {
      'modelconfig': {
        'appdb': {'_alias': regex.sub('', presettings['wdk']['modelconfig']['appdb']['connectionurl']) },
        'userdb': {'_alias': regex.sub('', presettings['wdk']['modelconfig']['userdb']['connectionurl']) }
      }
    }
  }


def fetch_dashboard_json_to_file(dash_data):
  dash_host = dash_data['hostname']
  dash_uri = 'http://' + dash_host + '/dashboard/json'

  try:
    response = urllib2.urlopen(dash_uri)
    content = response.read()
  except urllib2.HTTPError, e:
    print "HTTPError with %s: %s" % (dash_uri, e)
    raise
  except Exception, e:
    print "Exception with %s: %s" % (dash_uri, e)
    raise

  try:
    data = json.loads(content)
  except Exception, e:
    print "Exception reading /dashboard json: %s" % (e)
    raise

  dashboard_file = dash_host + '_dashboard.json'
  dash_fh = open(dashboard_file, 'w')
  dash_fh.write(json.dumps(data, indent=2))
  return dashboard_file

def load_settings_file(settings_file):
  with open(settings_file, 'r') as stream:
    try:
      usersettings = yaml.load(stream)
      return usersettings
    except yaml.YAMLError as exc:
      print(exc)


if __name__ == '__main__':
  main()
