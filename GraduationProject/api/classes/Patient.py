class Patient:
    def __init__(self, username="", password="", firstname="", lastname="", age=0, email="", phone_number=""):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.phone_number = phone_number

    def setID(self, idd):
        self.ID = idd

    def getID(self):
        return self.ID

    def setUsername(self, name):
        self.username = name

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def setFirstname(self, fname):
        self.firstname = fname

    def getFirstname(self):
        return self.firstname

    def setLastname(self, lname):
        self.lastname = lname

    def getLastname(self):
        return self.lastname

    def setAge(self, age):
        self.age = age

    def getAge(self):
        return self.age

    def setEmail(self, email):
        self.email = email

    def getEmail(self):
        return self.email

    def setPhone(self, phone):
        self.phone_number = phone

    def getPhone(self):
        return self.phone_number
