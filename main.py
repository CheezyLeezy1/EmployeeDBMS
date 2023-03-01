import sys

import baseFunctions as bF
import employeeOperations as empOp


# prints main menu simply
def showMenu():
    print("\nPlease choose an option:")
    print("1. View an Employee")
    print("2. Add an Employee")
    print("3. Change Employee Details")
    print("4. Delete an Employee")
    print("5. View all Employees")
    print("6. Enter Payroll Details")
    print("7. Employee Reports")
    print("8. Export Data to CSV")
    print("9. Payroll Reports")
    print("10. Exit\n")


# Runs the main loop of the program, which displays a menu of options and prompts
# the user to choose one. Based on the user's choice, it calls functions from both the
# employeeOperations and baseFunctions modules. A simple exit operation is included
def runMain():
    while True:
        showMenu()
        choice = bF.checkInteger("Enter your choice: ")

        if choice == 1:
            print("You chose 'View an Employee'\n")
            empOp.viewEmployee()

        elif choice == 2:
            print("You chose 'Add an Employee'\n")
            empOp.addEmployee()

        elif choice == 3:
            print("You chose 'Change Employee Details'\n")
            empOp.updateEmployee()

        elif choice == 4:
            print("You chose 'Delete an Employee'\n")
            empOp.deleteEmployee()

        elif choice == 5:
            print("You chose 'View all Employees'\n")
            empOp.allEmployees()

        elif choice == 6:
            print("You chose 'Enter Payroll Details'\n")
            empOp.payrollDetails()

        elif choice == 7:
            print("You chose 'Reports'\n")
            empOp.writeToReport()

        elif choice == 8:
            print("You chose 'Export Data to CSV'\n")
            empOp.exportData()

        elif choice == 9:
            print("You chose 'PayRoll Report'")
            empOp.payrollReport()

        elif choice == 10:
            print("GoodBye!")
            sys.exit(1)
        else:
            print("Invalid choice. Please enter a valid number!\n")


if __name__ == '__main__':
    runMain()
