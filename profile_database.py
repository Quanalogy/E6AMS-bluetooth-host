import sqlite3

class DatabaseConnection(object):

    def __init__(self, path_to_database):
        self.path = path_to_database
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE if not exists profiles (id INTEGER, command TEXT)''')
        cursor.close()
        connection.close()

    def addProfile(self, profile: int, command: str):

        if not self.getProfileCommand(profile):
            # The entry does not exist, create it
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO profiles VALUES ({}, '{}')".format(profile, command))
            connection.commit()
            cursor.close()
            connection.close()
        else:
            print("You've tried to create a profile that does exist, if you want to change this value")

    def getProfileCommand(self, profile: int):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cursor.execute("SELECT command from profiles WHERE id={}".format(profile))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        if not rows:
            print("No returned values")

        for row in rows:
            print("The row:", row[0])

        return rows

    def updateProfile(self, profile: int, command: str):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        cmd = """UPDATE profiles SET command = '{}' WHERE id = {}""".format(command, profile)
        cursor.execute(cmd)
        connection.commit()
        cursor.close()
        connection.close()

database = DatabaseConnection("/home/munk/Documents/School/ITAMS/profiles_database")
# database.addProfile(1, "Hello World")
database.getProfileCommand(1)
database.updateProfile(1, "New Command")
database.getProfileCommand(1)
database.getProfileCommand(2)