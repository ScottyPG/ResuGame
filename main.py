from dotenv import load_dotenv
import requests
import os
from dotenv import load_dotenv
import urllib.parse


HEADERS = {"X-API-Key": 'af6949815cf340f291d1d0e55a95cec3'}
memberType = 3
# membershipID = 4611686018467936766
# profile = requests.get("https://www.bungie.net/Platform/Destiny2/%s/Account/%s/Stats/"
#                         % (membershipType, membershipID), headers=HEADERS).json()

# print(profile['Response'])
# load_dotenv()
# print(os.getenv('DATABASE_PSWD'))

accountTag = urllib.parse.quote(input(">>> "))
profile = requests.get(
                "https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/%s/%s/"
                % (memberType, accountTag), headers=HEADERS).json()
print(len(profile['Response']))