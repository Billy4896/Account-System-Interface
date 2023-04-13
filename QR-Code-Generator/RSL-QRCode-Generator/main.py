# from admin_functions import AdminFunctions
# admin = AdminFunctions()
# admin.create_folder()

import sys
import re
import json
import hashlib
import PyQt5.QtCore as QtCore
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class Navigation:
    """Navigation class: Provides functionality to navigate between different pages of the application."""

    @staticmethod
    def goto_main_page():
        """Sets the index of MainPage into view."""
        main_page = MainPage()
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def goto_login_page():
        """Sets the index of LoginPage into view."""
        login = LoginPage()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def goto_create_account_page():
        """Sets the index of CreateAccountPage into view."""
        create_account = CreateAccountPage()
        widget.addWidget(create_account)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def goto_account_recovery_page():
        """Sets the index of AccountRecoveryPage into view."""
        account_recovery = AccountRecoveryPage()
        widget.addWidget(account_recovery)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def goto_account_recovery_page2():
        """Sets the index of AccountRecoveryPage2 into view."""
        accountRecovery2 = AccountRecoveryPage2()
        widget.addWidget(accountRecovery2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    @staticmethod
    def goto_account_recovery_page3():
        """Sets the index of AccountRecoveryPage3 into view."""
        accountRecovery3 = AccountRecoveryPage3()
        widget.addWidget(accountRecovery3)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class MainPage(QMainWindow):
    """Main Page class: Landing page once the application has been booted."""
    def __init__(self):
        """Loads the MainpPage.ui and provides functionality to the signInButton, createAccountButton & the recoverAccountButton."""
        super(MainPage, self).__init__()
        loadUi("MainPage.ui", self)
        self.signInButton.clicked.connect(Navigation.goto_login_page)
        self.createAccountButton.clicked.connect(Navigation.goto_create_account_page)
        self.recoverAccountButton.clicked.connect(Navigation.goto_account_recovery_page)


class LoginPage(QMainWindow):
    """Login Page class: Provides access to the user to log into the application."""
    def __init__(self):
        """Loads the LoginPage.ui and provides functionality to the signInButton & the backButton. The passwordTxtInput is also masked here."""
        super(LoginPage, self).__init__()
        loadUi("LoginPage.ui", self)
        self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.backButton.clicked.connect(Navigation.goto_main_page)
        self.signInButton.clicked.connect(self.login)
        self.showPasswordCheckBox.stateChanged.connect(self.show_or_hide_password)

    def login(self):
        """Verifies the account details on login attempt"""
        search_key1 = "username"
        search_key2 = "password"
        username = self.usernameTxtInput.text().upper()
        password = self.passwordTxtInput.text().upper()
        f = "UserDetails.txt"
        try:
            # Read all the dictionaries from the file
            with open(f, "r") as file:
                dict_list = [json.loads(line) for line in file]
        # Throw exception if the file does not exist.
        except FileNotFoundError:
            print("File does not exist, creating new file...")
        # Search for a matching account
        match_found = False
        for dictionary in dict_list:
            if dictionary.get(search_key1) == username and hashlib.sha512(
                    password.encode()).hexdigest() == dictionary.get(search_key2):
                print("Login successful!")
                match_found = True
                Navigation.goto_main_page()  # TODO: Change to the hub page when created#
                break
        # Display error message if no match is found
        if not match_found:
            self.errorLabel.setText("Incorrect login details, please try again.")

    def show_or_hide_password(self):
        """A function that will take show or hide the password inputs by detecting if a checkbox is checked."""
        if self.showPasswordCheckBox.isChecked():
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)


class CreateAccountPage(QMainWindow):
    """Create Account Page class: Provides access to the user to create an account for the application."""
    def __init__(self):
        """Loads the CreateAccountPage.ui and provides functionality to the createButton & the backButton. The passwordTxtInput is also masked here."""
        super(CreateAccountPage, self).__init__()
        loadUi("CreateAccountPage.ui", self)
        self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createButton.clicked.connect(self.verify_account_creation)
        self.backButton.clicked.connect(Navigation.goto_main_page)
        self.showPasswordCheckBox.stateChanged.connect(self.show_or_hide_password)

    def verify_account_creation(self):
        """Verify the username and password and pass the required criteria"""
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
        Navigation.goto_main_page()

    def show_or_hide_password(self):
        """A function that will take show or hide the password inputs by detecting if a checkbox is checked."""
        if self.showPasswordCheckBox.isChecked():
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)


class AccountRecoveryPage(QMainWindow):
    """Account Recovery Page class: Provides access to the user to recover an account used in the application."""
    def __init__(self):
        """Loads the AccountRecoveryPage.ui and provides functionality to the proceedButton & the backButton."""
        super(AccountRecoveryPage, self).__init__()
        loadUi("AccountRecoveryPage.ui", self)
        self.backButton.clicked.connect(Navigation.goto_main_page)
        self.proceedButton.clicked.connect(self.verify_username)

    def verify_username(self):
        """A function that will verify the user account exists."""
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
                Navigation.goto_account_recovery_page2()


class AccountRecoveryPage2(QMainWindow):
    """Account Recovery Page2 class: Provides access to the user to recover an account used in the application."""
    def __init__(self):
        super(AccountRecoveryPage2, self).__init__()
        loadUi("AccountRecoveryPage2.ui", self)
        self.load_user_phrase()
        self.backButton.clicked.connect(Navigation.goto_account_recovery_page)
        self.proceedButton.clicked.connect(self.verify_user_phrase)

    def load_user_phrase(self):
        """A function that loads the users recovery phrase."""
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

    def verify_user_phrase(self):
        """A function that verifies the users recovery phrase."""
        f = 'TempUsernames.txt'
        try:
            # Read all the usernames from the file
            with open(f, "r") as file:
                tempUser = file.read().strip()
                print(tempUser)
        # If the file cannot be found print error statement.
        except FileNotFoundError:
            print("File does not exist, creating new file...")

        search_key1 = "username"
        search_value1 = tempUser  # value1
        search_key2 = "recoveryPass"
        search_value2 = self.passwordTxtInput.text().upper()
        ff = "UserQuestion.txt"

        try:
            # Read all the usernames from the file
            with open(ff, "r") as file:
                dict_list = [json.loads(line) for line in file]
                print(dict_list)
        # Handle any exceptions that are raised
        except Exception as e:
            print("Error:", e)

        for dictionary in dict_list:
            if dictionary.get(search_key1) == search_value1 and hashlib.sha512(search_value2.encode()).hexdigest() == dictionary.get(search_key2):
                print("A match is found!")
                Navigation.goto_account_recovery_page3()


class AccountRecoveryPage3(QMainWindow):
    """Account Recovery Page3 class: Provides access to the user to recover an account used in the application."""
    def __init__(self):
        super(AccountRecoveryPage3, self).__init__()
        loadUi("AccountRecoveryPage3.ui", self)
        self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repasswordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.mainMenuButton.clicked.connect(Navigation.goto_main_page)
        self.proceedButton.clicked.connect(self.password_match)
        self.showPasswordCheckBox.stateChanged.connect(self.show_or_hide_password)

    def password_match(self):
        """A function that will compare password strings"""
        password = self.passwordTxtInput.text().upper()
        repassword = self.repasswordTxtInput.text().upper()

        if password == repassword:
            self.update_password()
        else:
            self.errorLabel.setText("The passwords entered do not match.")

    def update_password(self):
        """A function that will update the user password details in the UserDetails.txt"""
        ff = "UserDetails.txt"
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        search_key1 = "username"
        modify_key = "password"
        new_value = self.passwordTxtInput.text().upper()

        if len(new_value) < 8:
            self.errorLabel.setText("Password length must be greater than 8 characters long.")

        elif not (any(c.isalpha() for c in new_value) and any(c.isdigit() for c in new_value)):
            self.errorLabel.setText("Password must contain a mixture of letters, numbers and special characters.")

        elif regex.search(new_value) is None:
            self.errorLabel.setText("Password must contain special characters.")

        else:
            # Hash the password using SHA-256
            hashed_password = hashlib.sha256(new_value.encode()).hexdigest()

            # Read all the dictionaries from the file
            with open(ff, "r") as file:
                dict_list = [json.loads(line) for line in file]

            # Modify the required dictionary
            for dictionary in dict_list:
                if dictionary.get(search_key1) == hashed_password:
                    dictionary[modify_key] = new_value
                    break  # Stop searching after the first match is found

            # Write all the dictionaries back to the file
            with open(ff, "w") as file:
                for dictionary in dict_list:
                    file.write(json.dumps(dictionary) + "\n")

            print("Password has been successfully changed.")
            Navigation.goto_main_page()

    def show_or_hide_password(self):
        """A function that will take show or hide the password inputs by detecting if a checkbox is checked."""
        if self.showPasswordCheckBox.isChecked():
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.repasswordTxtInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.passwordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)
            self.repasswordTxtInput.setEchoMode(QtWidgets.QLineEdit.Password)



# Main - The following block of code runs the application.
app = QApplication(sys.argv)
mainPage = MainPage()
widget = QStackedWidget()
widget.addWidget(mainPage)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

sys.exit(app.exec())
