#!/usr/bin/python3

# Copyright 2018 Scott Hurrey

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys, getopt
import requests
import json

def main(argv):
    user = ''
    password = ''
    oldgroup = ''
    newgroup = ''
    host = ''
    debug = False

    if len(sys.argv) < 6:
        print ('changeGroupUrl.py -j <jive domain i.e. https://my.community.com> -u <jive username> -p <jive password> -g <old group name> -n <new group name>')
        sys.exit(3)

    try:
      opts, args = getopt.getopt(argv,"dhu:p:g:n:j:",["user=","pass=","oldgroup=","newgroup=","host="])
    except getopt.GetoptError:
      print ('changeGroupUrl.py -j <jive domain i.e. https://my.community.com> -u <jive username> -p <jive password> -g <old group name> -n <new group name> -h -d' )
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('changeGroupUrl.py -j <jive domain i.e. https://my.community.com> -u <jive username> -p <jive password> -g <old group name> -n <new group name> -h -d')
            sys.exit()
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-p", "--pass"):
            password = arg
        elif opt in ("-g", "--oldgroup"):
            oldgroup = arg
        elif opt in ("-n", "--newgroup"):
            newgroup = arg
        elif opt in ("-j", "--jive"):
            host = arg
        elif opt in ("-d", "--debug"):
            debug = True
    if debug:
        print ('Jive Domain is ', host)
        print ('User is ', user)
        print ('Password is ', password)
        print ('Old Group is ', oldgroup)
        print ('New Group is ', newgroup)

    payload = { 'filter' : 'search(' + oldgroup + ')' }
    r = requests.get(host + '/api/core/v3/search/places', params=payload, auth=(user, password))

    if debug:
        print ('URL +---------------------------------------------+')
        print(r.url)

    data = r.json()

    if debug:
        print(data)

    if r.status_code != requests.codes.ok:
        print('Error searching for group: ', r.status_code)
        sys.exit(4)

    if data['list']:
        print('Processing groups...')
    else:
        print('Old group not found')
        sys.exit(5)

    for current_group in data['list']:
        if debug:
            print(current_group['resources']['html']['ref'])

        if(current_group['resources']['html']['ref'] == host + '/groups/' + oldgroup):
            place_url = current_group['resources']['self']['ref']
            group_type = current_group['groupType']

            if debug:
                print('placeURL: ' + place_url + ', groupType: ' + group_type)
            break

    if place_url:
        if debug:
            print('OUTSIDEFOR: placeURL: ' + place_url + ', groupType: ' + group_type)

        print("Changing group name " + oldgroup + " to " + newgroup + "...")

        json = { 'groupType' : group_type, 'displayName' : newgroup }

        changed=requests.put(place_url, json=json, auth=(user, password))

        if debug:
            print(changed.status_code)

        if changed.status_code != requests.codes.ok:
            print('Error updating group URL: ', changed.status_code)
            sys.exit(4)
    else:
        print('Old group not found')
        sys.exit(6)

if __name__ == "__main__":
   main(sys.argv[1:])
