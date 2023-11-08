# Set Management Status CLI (sms-cli)

Simple CLI tool to set the management status of Jamf Pro computer object(s) via the universal api. Iterates a Jamf Advanced Computer Search and updates each individual object.

> Jamf removed the ability to mass action modify the management account status for computers in 10.49. We can mass modify computer objects via the uapi instead.

## Setup

> For best results use a virtual environment and install all dependencies https://realpython.com/intro-to-pyenv/

1. Create an advanced computer search in Jamf Pro which filters just the devices you wish to mark as `unmanaged` / `managed`. 
2. Make note of the search id from the url.
3. `git clone` this repo.
4. Install project dependencies `pip install -r requirements.txt`. 
5. - To set computers as `unmanaged`:
    
    `python ./sms-cli.py --url=https://company.jamfcloud.com --username=user --unmanaged --id=156`
   
   - To set computers as `managed`:
   
   `python ./sms-cli.py --url=https://company.jamfcloud.com --username=user --managed --id=156`

   - For help:
  
   `python ./sms-cli.py --help`
   
   ```
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
   ```
## Output Example

```
$ python ./sms-cli.py --url=https://company.jamfcloud.com --username=user --managed --id=156 --password='pass'
Are you sure you want to change the management status for the device(s)? [y/N]: y
[SMS-CLI] Using search ID: Computers - Test Group
[SMS-CLI] Setting management status for host:host1 jssid:2988...
[SMS-CLI]...New management status = True
[SMS-CLI] Setting management status for host:host2 jssid:4277...
[SMS-CLI]...New management status = True
[SMS-CLI] Setting management status for host:host3 jssid:4117...
[SMS-CLI]...New management status = True
```

## Credits

https://gitlab.com/cvtc/appleatcvtc/jps-api-wrapper#install

https://click.palletsprojects.com/en/8.1.x/
