#!/usr/bin/env python

import urllib2
import re
import sys
import subprocess
import os
from distutils.spawn import find_executable

if not find_executable('openvpn'):
    "openvpn seems to be not installed"
    sys.exit(1)

if len(sys.argv) < 2:
    print "Usage: ./{0} <config_file.ovpn>".format(sys.argv[0])
    print "Usage: ./{0} --test".format(sys.argv[0])
    sys.exit(1)

temp_auth_file = '/tmp/auth_info.txt'
config_file = sys.argv[1]

url = "https://www.vpnbook.com/freevpn"
pattern = re.compile(r'Password:\s<.+?>(?P<pass>.+?)</.+>')

web_page = urllib2.urlopen(url).read()

username = 'vpnbook'
password = pattern.search(web_page).group('pass')

print "Username = {0}".format(username)
print "Password = {0}".format(password)
print "Config file = {0}".format(config_file)

with open(temp_auth_file, 'w') as auth_info:
    auth_info.writelines(username + '\n')
    auth_info.writelines(password + '\n')

if sys.argv[1] != "--test":
    if not os.path.isfile(config_file):
        print "Config file {0} does not exist".format(config_file)
        sys.exit(1)
    try:
       subprocess.call(['openvpn', '--config', "%s" % config_file, 
'--auth-user-pass', "%s" % temp_auth_file])
    except KeyboardInterrupt:
       os.remove(temp_auth_file)
       sys.exit(1)



