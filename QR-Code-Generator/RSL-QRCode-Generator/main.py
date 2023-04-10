# from admin_functions import AdminFunctions
# admin = AdminFunctions()
# admin.create_folder()

import sys
import re
import json
import hashlib
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi("MainPage.ui", self)
        self.signInButton.clicked.connect(self.gotoLoginPage)
        self.createAccountButton.clicked.connect(self.gotoCreateAccountPage)
        self.recoverAccountButton.clicked.connect(self.gotoAccountRecoveryPage)

    def gotoLoginPage(self):
        login = LoginPage()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoCreateAccountPage(self):
        createAccount = CreateAccountPage()
        widget.addWidget(createAccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoAccountRecoveryPage(self):
        accountRecovery = AccountRecoveryPage()
        widget.addWidget(accountRecovery)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginPage(QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi("LoginPage.ui", self)
        self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backButton.clicked.connect(self.gotoMainPage)
        self.signInButton.clicked.connect(self.login)

    def gotoMainPage(self):
        mainPage = MainPage()
        widget.addWidget(mainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def login(self):
        """Verifies the account details on login attempt"""
        search_key1 = "username"
        search_key2 = "password"
        username = self.usernameTxtInput.text().upper()
        password = self.passwordTxtInput.text().upper()
        f = "UserDetails.txt"
        # Read all the dictionaries from the file
        with open(f, "r") as file:
            dict_list = [json.loads(line) for line in file]
        # Search for a matching account
        match_found = False
        for dictionary in dict_list:
            if dictionary.get(search_key1) == username and hashlib.sha512(
                    password.encode()).hexdigest() == dictionary.get(search_key2):
                print("Login successful!")
                match_found = True
                self.gotoMainPage()  # TODO: Change to the hub page when created#
                break
        # Display error message if no match is found
        if not match_found:
            self.errorLabel.setText("Incorrect login details, please try again.")


class CreateAccountPage(QMainWindow):
    def __init__(self):
        super(CreateAccountPage, self).__init__()
        loadUi("CreateAccountPage.ui", self)
        self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createButton.clicked.connect(self.verify_account_creation)
        self.backButton.clicked.connect(self.gotoMainPage)

    def gotoMainPage(self):
        mainPage = MainPage()
        widget.addWidget(mainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def verify_account_creation(self):
        """Verify the username and password pass the required criteria"""
        self.errorLabel.setText("")
        username = self.usernameTxtInput.text().upper()
        password = self.passwordTxtInput.text().upper()
        recoveryPassword = self.recoveryPasswordTxtInput.text().upper()
        f = 'Usernames.txt'
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        lines = []
        try:
            with open(f, "r") as file:
                # Read the binary file to a list to test the while loop
                lines = file.read().split('\n')

        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating file...")

        if username in lines:
            self.errorLabel.setText("Username is taken, please try again.")
        elif len(username) < 3 or len(username) > 12:
            self.errorLabel.setText("Username length must be between 3 - 12 characters.")
        elif len(password) < 8:
            self.errorLabel.setText("Password length must be greater than 8 characters long")
        elif not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            self.errorLabel.setText("Password must contain a mixture of letters, numbers and special characters")
        elif regex.search(password) is None:
            self.errorLabel.setText("Password must contain special characters")
        elif len(recoveryPassword) < 1:
            self.errorLabel.setText("Please enter a recovery answer.")
        else:
            try:
                with open(f, "a") as file:
                    file.write(username + '\n')
            # Throw exception if the file does not exist.
            except FileNotFoundError:
                print("File does not exist, creating new file...")

            self.create_account()
            print("Account successfully created")

    def create_account(self):
        """A function that will create the user account"""
        username = self.usernameTxtInput.text().upper()
        password = self.passwordTxtInput.text().upper()
        recoveryPhrase = self.recoveryPhraseComboBox.currentText()
        recoveryPassword = self.recoveryPasswordTxtInput.text().upper()
        f = 'UserDetails.txt'
        ff = 'UserQuestion.txt'
        fff = 'UserPhrase.txt'
        hashed_password = hashlib.sha512(password.encode()).hexdigest()
        hashed_recoveryPassword = hashlib.sha512(recoveryPassword.encode()).hexdigest()
        try:
            # Open the .bin file for writing - ('With open' automatically closes the file upon completion)
            with open(f, "a") as file:
                credentials = {'username': username, 'password': hashed_password}
                file.write(json.dumps(credentials) + "\n")
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")

        try:
            # Open the .bin file for writing - ('With open' automatically closes the file upon completion)
            with open(ff, "a") as file:
                credentials = {'username': username, 'recoveryPass': hashed_recoveryPassword}
                file.write(json.dumps(credentials) + "\n")
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")

        try:
            # Open the .bin file for writing - ('With open' automatically closes the file upon completion)
            with open(fff, "a") as file:
                credentials = {'username': username, 'recoveryPass': recoveryPhrase}
                file.write(json.dumps(credentials) + "\n")
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")


class AccountRecoveryPage(QMainWindow):
    def __init__(self):
        super(AccountRecoveryPage, self).__init__()
        loadUi("AccountRecoveryPage.ui", self)
        self.backButton.clicked.connect(self.gotoMainPage)
        self.proceedButton.clicked.connect(self.verify_username)

    def gotoMainPage(self):
        mainPage = MainPage()
        widget.addWidget(mainPage)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoAccountRecoveryPage2(self):
        accountRecovery2 = AccountRecoveryPage2()
        widget.addWidget(accountRecovery2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def verify_username(self):
        f = 'Usernames.txt'
        ff = 'TempUsernames.txt'
        inputUser = self.usernameTxtInput.text().upper()

        try:
            # Read all the usernames from the file
            with open(f, "r") as file:
                usernames = file.read().split('\n')
                print(usernames)
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")

        # for each username in the usernames list
        for username in usernames:
            if username != inputUser:
                self.errorLabel.setText("Username is not recognised.")
            else:
                # Write the valid username to the file
                with open(ff, "w") as file:
                    file.write(inputUser)
                self.gotoAccountRecoveryPage2()


class AccountRecoveryPage2(QMainWindow):
    def __init__(self):
        super(AccountRecoveryPage2, self).__init__()
        loadUi("AccountRecoveryPage2.ui", self)
        self.load_user_phrase()

    def load_user_phrase(self):
        f = 'TempUsernames.txt'
        try:
            # Read all the usernames from the file
            with open(f, "r") as file:
                tempUser = file.read().strip()
                print(tempUser)
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")

        search_key = "username"
        search_value = tempUser  # value1
        ff = "UserPhrase.txt"

        # Read all the usernames from the file
        with open(ff, "r") as file:
            dict_list = [json.loads(line) for line in file]

        # Search the dict_list to find a match
        for dictionary in dict_list:
            if dictionary.get(search_key) == search_value:
                recoveryPhrase = list(dictionary.values())[1]
                self.recoveryPhraseLabel.setText(f"{recoveryPhrase}")



# main
app = QApplication(sys.argv)
mainPage = MainPage()
widget = QStackedWidget()
widget.addWidget(mainPage)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

sys.exit(app.exec())
