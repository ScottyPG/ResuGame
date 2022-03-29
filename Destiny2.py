import requests
import json
import os
import urllib.parse
import pymysql
from dotenv import load_dotenv


class Destiny2:

    accountTag = ""
    memberType = 0
    membershipID = 0

    load_dotenv()
    HEADERS = {"X-API-Key": os.getenv('BUNGIE_TOKEN')}
    killsDeathRatio = 0
    winLossRatio = 0
    longestKillSpree = 0
    hoursPlayed = 0
    highestLightLevel = 0

    def __init__(self, userID):
        self.userID = userID
        self.setMemberTypePrompted()
        self.setaccounttag()
        # self.pullStatsPVP()
        # self.writeStats()

    def setMemberTypePrompted(self):
        print("[1] Xbox || [2] Playstation || [3] Steam || [4] Blizzard || [5] Stadia || [10] Demon || [254] BungieNext")
        tracker = -1
        while not (int(self.memberType) == 1 or int(self.memberType) == 2 or int(self.memberType) == 3 or
                   int(self.memberType) == 4 or int(self.memberType) == 5 or int(self.memberType) == 10 or
                   int(self.memberType) == 254):
            tracker += 1
            if (tracker == 0):
                self.memberType = int(
                    input("Enter the number corresponding to the type of Destiny 2 account you have: "))
            else:
                print("Error: Invalid Entry")
                self.memberType = int(
                    input("Enter the number corresponding to the type of Destiny 2 account you have: "))

    def setMemberType(self, num):
        self.memberType = num

    def setaccounttag(self):

        validTag = 0
        while (validTag == 0):
            print("Please enter your Destiny 2 gamer tag, found in your Bungie.net account (Ex. GamerTag#0000")
            self.accountTag = urllib.parse.quote(input(">>> "))
            profile = requests.get(
                "https://www.bungie.net/Platform/Destiny2/SearchDestinyPlayer/%s/%s/"
                % (self.memberType, self.accountTag), headers=self.HEADERS).json()
            if (len(profile['Response']) == 0):
                print("No account found for that account type.")
                # validTag = -1
            else:
                print("Success!")
                print(profile['Response'])
                self.membershipID = int(profile['Response'][0]['membershipId'])
                print(self.membershipID)
                validTag = 1
                self.pullStatsPVP()

    def pullStatsPVP(self):
        profile = requests.get("https://www.bungie.net/Platform/Destiny2/%s/Account/%s/Stats/"
                               % (self.memberType, self.membershipID), headers=self.HEADERS).json()
        self.killsDeathRatio = \
            profile['Response']['mergedAllCharacters']['results']['allPvP']['allTime']['killsDeathsRatio']['basic'][
                'displayValue']
        print(self.killsDeathRatio)
        self.winLossRatio = \
            profile['Response']['mergedAllCharacters']['results']['allPvP']['allTime']['winLossRatio']['basic'][
                'displayValue']
        print(self.winLossRatio)
        self.longestKillSpree = \
            profile['Response']['mergedAllCharacters']['results']['allPvP']['allTime']['longestKillSpree']['basic'][
                'displayValue']
        print(self.longestKillSpree)
        self.hoursPlayed = \
            round((int(profile['Response']['mergedAllCharacters']['merged']['allTime']['secondsPlayed']['basic'][
                'value']) / 3600), 1)
        print(self.hoursPlayed)
        self.highestLightLevel = \
            profile['Response']['mergedAllCharacters']['results']['allPvP']['allTime']['highestLightLevel']['basic'][
                'displayValue']
        print(self.highestLightLevel)
        self.writeStats()

    def writeStats(self):
        # destiny2_ID | StatID | StatName | StatType (Multi/Single) | StatCompleted (Boolean) NULL | StatValue(Float) NULL
        db = pymysql.connect(host='ads-mysql-capstonespg.cillfjzebayd.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password=os.getenv('DATABASE_PSWD'),
                             database='GameStats')
        cursor = db.cursor()
        sql = '''UPDATE user SET destiny2_ID = '%s' WHERE userID = '%s' ''' % (self.membershipID, self.userID)
        cursor.execute(sql)
        sql2 = '''insert into Destiny2(userID, destiny2_ID, statID, StatName, StatType, StatCompleted, StatValue) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            self.userID, self.membershipID, 'M001', 'K/D', 'MULTI', 1, self.killsDeathRatio)
        cursor.execute(sql2)
        sql3 = '''insert into Destiny2(userID, destiny2_ID, statID, StatName, StatType, StatCompleted, StatValue) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            self.userID, self.membershipID, 'M002', 'Win/Loss Ratio', 'MULTI', 1, self.winLossRatio)
        cursor.execute(sql3)
        sql4 = '''insert into Destiny2(userID, destiny2_ID, statID, StatName, StatType, StatCompleted, StatValue) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            self.userID, self.membershipID, 'M003', 'Longest Kill Spree', 'MULTI', 1, self.longestKillSpree)
        cursor.execute(sql4)
        sql5 = '''insert into Destiny2(userID, destiny2_ID, statID, StatName, StatType, StatCompleted, StatValue) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            self.userID, self.membershipID, 'M004', 'Hours Played', 'MULTI', 1, self.hoursPlayed)
        cursor.execute(sql5)
        sql6 = '''insert into Destiny2(userID, destiny2_ID, statID, StatName, StatType, StatCompleted, StatValue) values('%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            self.userID, self.membershipID, 'M005', 'Highest Light Level', 'MULTI', 1, self.highestLightLevel)
        cursor.execute(sql6)
        db.commit()
        # print("Wrote stat?")
