#!/usr/bin/env python3
# encoding: utf-8
#
# isthisthingon. - 20231016
#
#

'''python ./sms-cli.py --help
Usage: sms-cli.py [OPTIONS]

  Simple CLI tool to set the management status of Jamf Pro computer object(s)
  via the universal api. Iterates a Jamf Advanced Computer Search and updates 
  each individual object.

Options:
  --url TEXT               Jamf Pro url - e.g https://company.jamfcloud.com
                           [required]
  --username TEXT          Jamf Pro user with permissions - Computers: Read,
                           Update, Users: Update.  [required]
  --managed / --unmanaged  Required management status of computer object in
                           Jamf Pro.  [required]
  --id INTEGER             Jamf Pro Advanced Computer Search ID.  [required]
  --password TEXT          Jamf Pro user password.
  --yes                    Confirm the action without prompting.
  --help                   Show this message and exit.
'''

from jps_api_wrapper.classic import Classic
from jps_api_wrapper.pro import Pro
import click
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
@click.option('--username', required=True, help='Jamf Pro user with permissions - Computers: Read, Update, Users: Update.')
@click.option('--managed/--unmanaged', required=True, help='Required management status of computer object in Jamf Pro.')
@click.option('--id', required=True, type=int, help='Advanced Computer Search ID.')
@click.password_option(help='Jamf Pro user password.')
@click.confirmation_option(prompt='Are you sure you want to change the management status for the device(s)?')

def set_management_status(url,username,managed,id,password):

    """Simple CLI tool to set the management status of Jamf Pro computer object(s)
    via the universal api. Iterates a Jamf Advanced Computer Search and updates 
    each individual object."""

    ''' xml payload needs string value from cli boolean '''
    desired_status = str(managed).lower()
    payload = f'<computer><general><remote_management><managed>{desired_status}</managed></remote_management></general></computer>'

    ''' use jps-api-wrapper to do the heavy lifting '''
    with Classic(url, username, password) as classic:
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
