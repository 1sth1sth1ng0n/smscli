# Set Management Status CLI (sms-cli)

Simple CLI tool to modify the management status of Jamf Pro computer object(s) via the classic api. Iterates a Jamf Pro 'Advanced Computer Search' and updates each individual object. Now supports client based auth.

> Jamf removed the ability to mass action modify the management account status for computers in 10.49. We can mass modify computer objects via the api instead.

> Basic Authentication in the Classic API is no longer supported and will be turned off for all 11.5.0 instances to provide enhanced security. 

## Setup

> For best results use a pyhthon virtual environment and install all dependencies https://realpython.com/intro-to-pyenv/

1. Create an advanced computer search in Jamf Pro which filters just the devices you wish to modify as `unmanaged` / `managed`. 
2. Make note of the search id from the url.
3. `git clone` this repo.
4. Install project dependencies `pip install -r requirements.txt`. 
5. - To set computers as `unmanaged`:
    
    `python ./sms-cli.py --url=https://company.jamfcloud.com --client_id=XXXX --client_secret=XXXX --unmanaged --id=156`
   
   - To set computers as `managed`:
   
   `python ./sms-cli.py --url=https://company.jamfcloud.com --client_id=XXXX --client_secret=XXXX --managed --id=156`

   - For help:
  
   `python ./sms-cli.py --help`
   
   ```
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
   ```
## Output Example

```
$ python ./sms-cli.py --url=https://company.jamfcloud.com --client_id=XXXX --client_secret=XXXX --unmanaged --id=156
[SMS-CLI] Using search ID: Computers - Test Group
[SMS-CLI] Setting management status for host:host1 jssid:2988...
[SMS-CLI]...New management status = False
[SMS-CLI] Setting management status for host:host2 jssid:4277...
[SMS-CLI]...New management status = False
[SMS-CLI] Setting management status for host:host3 jssid:4117...
[SMS-CLI]...New management status = False
```

## Credits

https://gitlab.com/cvtc/appleatcvtc/jps-api-wrapper#install

https://click.palletsprojects.com/en/8.1.x/
