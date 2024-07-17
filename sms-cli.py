#!/usr/bin/env python3
# encoding: utf-8
#
# isthisthingon. - 20240717
#
#

'''python ./sms-cli.py --help
  Usage: sms-cli.py [OPTIONS]

  Simple CLI tool to modify the management status of Jamf Pro computer
  object(s)  via the classic api. Iterates a Jamf Pro 'Advanced Computer
  Search' and updates  each individual object. Now supports client based auth.

  Options:
    --url TEXT               Jamf Pro url - e.g https://company.jamfcloud.com
                             [required]
    --client_id TEXT         Jamf Pro api Client ID with permissions -
                             Computers: Read, Update. Users: Update. Advanced
                             Computer Searches: Read.  [required]
    --client_secret TEXT     Jamf Pro Client Secret associated with the supplied
                             Client ID.  [required]
    --managed / --unmanaged  Required management status of computer object in
                             Jamf Pro.  [required]
    --id INTEGER             Advanced Computer Search ID.  [required]
    --help                   Show this message and exit.
'''

from jps_api_wrapper.classic import Classic
import click
import os
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

# file log handler
file = logging.FileHandler("output.log",mode='w')
file.setFormatter(logformat)

# console log handler
console = logging.StreamHandler()
console.setFormatter(logformat)

# add handlers
logger.addHandler(file)
logger.addHandler(console)

@click.command()
@click.option('--url', required=True, help='Jamf Pro url - e.g https://company.jamfcloud.com')
@click.option('--client_id', required=True, help='Jamf Pro api Client ID with permissions - Computers: Read, Update. Users: Update. Advanced Computer Searches: Read.')
@click.option('--client_secret', required=True, help='Jamf Pro Client Secret associated with the supplied Client ID.')
@click.option('--managed/--unmanaged', required=True, help='Required management status of computer object in Jamf Pro.')
@click.option('--id', required=True, type=int, help='Advanced Computer Search ID.')

def set_management_status(url,client_id,client_secret,managed,id):

  """ Simple CLI tool to modify the management status of Jamf Pro computer object(s) 
  via the classic api. Iterates a Jamf Pro 'Advanced Computer Search' and updates 
  each individual object. Now supports client based auth."""

  ''' xml payload needs string value from cli boolean '''
  desired_status = str(managed).lower()
  payload = f'<computer><general><remote_management><managed>{desired_status}</managed></remote_management></general></computer>'

  ''' use jps-api-wrapper to do the heavy lifting '''
  with Classic(url, client_id, client_secret, client=True) as classic:
    computer_group = classic.get_advanced_computer_search(id=id, data_type='json')
    logger.info(f"Using group: {computer_group['advanced_computer_search']['name']}")
    '''loop group members and extract managed value'''
    for item in computer_group['advanced_computer_search']['computers']:
      jssid = item['id']
      logger.info(f"Setting management status for host:{item['Computer_Name']} jssid:{jssid}...")
      classic.update_computer(id=jssid, data=payload)
      management_status = classic.get_computer(id=jssid, subsets=['General'])
      logger.info(f"...New management status = {management_status['computer']['general']['remote_management']['managed']}")

if __name__ == '__main__':
  set_management_status()
