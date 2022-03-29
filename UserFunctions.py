from dotenv import load_dotenv
import pymysql
import Destiny2
import os

load_dotenv()
db = pymysql.connect(host='ads-mysql-capstonespg.cillfjzebayd.us-east-1.rds.amazonaws.com',
                     user='admin',
                     password=os.getenv('DATABASE_PSWD'),
                     database='GameStats')
cursor = db.cursor()

userID = 0
currentUser = -1

def createuser():
    username = input("Username (<16 chars): ")
    password = input("Password: ")
    sql = '''
    insert into user(username, password) values('%s', '%s')''' % (username, password)
    cursor.execute(sql)
    db.commit()
    print("User created.")
    sql_ID = '''SELECT userID FROM user WHERE username = '%s' AND password = '%s' ''' % (username, password)
    cursor.execute(sql_ID)
    global userID, currentUser
    userID = (cursor.fetchone())[0]
    currentUser = userID

def printusers():
    sql2 = '''select userID from user'''
    cursor.execute(sql2)
    print(cursor.fetchall())

def addDestiny2():
    global userID
    obj = Destiny2.Destiny2(userID)
    # dreadmute#4406
    # Omniscient Bias#2431

def selectUser():
    global currentUser
    if (currentUser < 0):
        print(" ! No user currently selected ! ")
        validUser = 0
        while (validUser == 0):
            userSet = int(input("Enter the user ID for the account you'd like to select >>> "))
            sql = '''select userID from user'''
            cursor.execute(sql)
            userIDList = cursor.fetchall()
            # print(userIDList)
            for x in range(len(userIDList)):
                if (userIDList[x][0] == userSet):
                    currentUser = int(userSet)
                    validUser = 1
                    print("Success! User ID found!")
                    break
                else:
                    if (x == len(userIDList)-1):
                        print("User ID not registered.")
    else:
        print("Currently selected User: " + str(currentUser))

def printCurrentUser():
    db.commit()
    global currentUser
    if (currentUser < 0):
        selectUser()
    sql2 = '''select * from user WHERE userID = '%s' ''' % (currentUser)
    cursor.execute(sql2)
    print(cursor.fetchall())


if __name__ == "__main__":
    print('''
What would you like to do?
[1] Create User
[2] Select User
[3] Add Destiny 2 Account
...
[7] Print Currently Selected User (raw)
[8] Print Users
[9] Quit''')
    onoff = 0
    while (onoff == 0):
        request = input(">>> ")

        if (request == '1'):
            createuser()
            continue
        if (request == '2'):
            selectUser()
            continue
        if (request == '3'):
            selectUser()
            addDestiny2()
            continue
        if (request == '7'):
            printCurrentUser()
            continue
        if (request == '8'):
            printusers()
            continue
        if (request == '9'):
            onoff = 1
            break
        else:
            print("Invalid entry, Please choose integer value corresponding to options below:")
