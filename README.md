# assessment-grader
Export Survey Monkey scores and import into assessment grader google sheet

## Create Gooogle Drive Application ##
### Prerequisites ###
- Python 2.6 or greater
- The pip package management tool
- A Google account with Google Drive enabled


### 1: Turn on the Drive API ###
- Make sure you are signed into the appropriate google account.
- Follow the instructions [here](https://developers.google.com/drive/api/v3/quickstart/python) to create a new Cloud Platform project and automatically enable the Drive API.


### 2. Download Credentials ###
- In resulting dialog click **DOWNLOAD CLIENT CONFIGURATION** and save the file **credentials.json** to the project directory.



## Run Script ##
```
pip install -r requirements.txt
python primes_script.py
```
