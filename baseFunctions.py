import re
from datetime import datetime

import mysql.connector
from _mysql_connector import MySQLInterfaceError
from mysql.connector import ProgrammingError


# This function establishes a connection to a MySQL database and returns the database object, it gets the password from
# a .env file, which adds a simple layer of security to the project and prevents hard-coding of a sensitive variable
def runDB():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="MyDatabase"
    )

    return db


# This function checks if a connection to a database is established and returns a Boolean based on the status.
# If an exception is caught, an appropriate error message is printed and the function returns False.
def checkConnection(database):
    try:
        if database.is_connected():
            return True

    except MySQLInterfaceError:
        printSQLInterfaceError()
        return False

    except ProgrammingError:
        printProgrammingError()
        return False

    except AttributeError:
        printAttributeError()
        return False


# checks string inputs
def checkString(prompt):
    while True:
        validString = input(prompt)
        if len(validString) > 1:
            return validString
        print("Invalid input. Please enter an input with more than 1 character and without numbers.")


# checks integer inputs
def checkInteger(prompt):
    while True:
        try:
            validInt = int(input(prompt))
            if validInt > 0:
                return validInt
            print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# checks float inputs
def checkFloat(prompt):
    while True:
        try:
            validFloat = float(input(prompt))
            if validFloat > 0:
                return validFloat
            print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


# validates an email against the regex pattern
def checkEmail(prompt):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    while True:
        email = input(prompt)
        if re.match(pattern, email):
            return email
        print("Invalid email entry, try again")


# validates a mobile number against the regex pattern
def checkPhoneNumber(prompt):
    pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
    while True:
        phone_number = input(prompt)
        if re.match(pattern, phone_number):
            return phone_number
        print("Invalid phone number, try again")


# validates the data using the datetime.strptime function
# it takes two arguments: the first argument is the string that needs to be converted to a datetime object,
# and the second argument is the format of the string.
def checkDate(prompt):
    while True:
        try:
            dateEntered = input(prompt)
            correctDate = datetime.strptime(dateEntered, '%Y-%m-%d').date()
            return correctDate
        except ValueError:
            print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")


def successMsg():
    print("Operation Successful!")


def exitMessage():
    print("Thank you for using our service!\n")


# these following methods prints a helping guide for dealing with exceptions
def printProgrammingError():
    print("\nError Connecting to Database: \n"
          "\nThis error is typically caused by an issue with the SQL query/syntax, such as one of the following:\n"
          "\n\t\t- a missing or incorrect table or column name \n"
          "\n\t\t- a missing or incorrect parameter \n"
          "\n\t\t- an issue with a username/password \n"
          "\nTo Resolve this Issue, please try the following: "
          "\n1. Check that the SQL query is correct and has no syntax errors"
          "\n2. Check that the table or column names are correct and exist in the database"
          "\n3. Check that all necessary parameters are included and in the correct format")


def printAttributeError():
    print("\nAttribute Error: \n"
          "\nThis error is typically caused by trying to access an attribute that does not exist or is not defined.\n"
          "\nTo Resolve this Issue, please try the following: "
          "\n1. Check that the attribute name is correct and exists in the object you are accessing"
          "\n2. Check that you are accessing the correct object and it has the attribute you are trying to access"
          "\n3. If you are working with a library or third-party module, check the documentation to ensure that you are"
          " using the correct attribute names and syntax")


def printSQLInterfaceError():
    print("\nError Connecting to Database: \n"
          "\nThis error is typically caused by a connection issue, such as one of the following:\n"
          "\n\t\t- an invalid user name or password \n"
          "\n\t\t- an incorrect port number \n"
          "\n\t\t- a firewall could be blocking the connection \n"
          "\n To Resolve this Issue, please try the following: "
          "\n1. Check that the connection details are correct"
          "\n2. Ensure the SQL Server is running"
          "\n3. Verify the connection is not being blocked, by an antivirus or firewall")
