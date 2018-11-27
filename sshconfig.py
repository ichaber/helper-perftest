#!/usr/local/bin/python3

"""
Takes input from stdin and parses it as json to get IP addresses out of a result from an AWS commandline command.
The output is a ssh config for all IPs named in ascending order.

Example usage with aws cli and aws-vault:
aws-vault --debug exec accountName -- aws ec2 describe-instances --filters "Name=tag:$Type,Values=$TagValue" | ./sshconfig.py
"""

import sys
import json

templ = """
Host perftest{0:d}
       User ubuntu
       HostName {1:s}
       IdentityFile ~/.ssh/keyname.pem
"""

perfdata = ''
for line in sys.stdin:
    perfdata += str(line.strip())

perftestjson = json.loads(perfdata)

#Fetch IP addresses from json input
ips = [instance[field] for reservation in perftestjson['Reservations'] for instance in reservation['Instances'] for field in instance if field == 'PublicIpAddress']

for key, ip in enumerate(ips):
    print(templ.format(key, ip))

