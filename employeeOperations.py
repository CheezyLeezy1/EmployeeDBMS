import baseFunctions as bF
from datetime import date


# this function was created to stop the re-use of code, as it is needed throughout
# it takes a cursor object passed in, which allows it to select based on the employeeID entered
def quickFetchEmployee(cursor):
    employeeID = bF.checkInteger("\nPlease Enter an Employee ID: ")
    viewCommand = "SELECT * From myDB.Employee where idEmployee = %s"
    cursor.execute(viewCommand, [employeeID])

    employee = cursor.fetchone()
    if employee is None:
        print("No Employee Found with that ID\n")
    else:
        print("\nID: {}\nName: {} {}\nAddress: {}\nEmail: {}\nPhone: {}\nStart Date: {}\nEnd Date: {}\n".format(
            employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], employee[7]))
        return employee


# simple view method, uses the run db and check connection methods from baseFunctions file
# this allows errors to be caught in the start-up of the database
def viewEmployee():
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    if bF.checkConnection(db):
        while True:
            bF.successMsg()
            quickFetchEmployee(cursor)

            choice = bF.checkString("Would you like to view another employee? Yes/No : ").lower()

            if choice.startswith("y"):
                continue
            elif choice.startswith("n"):
                break
            else:
                print("Invalid Input.")

        cursor.close()
        db.close()


# adds an employee by using validated variables and passing them into the cursor
# utilises the %s placeholder compatible with mysql, and allows data to be passed in without risk of SQLInjection
def addEmployee():
    db = bF.runDB()
    cursor = db.cursor(buffered=True)
    if bF.checkConnection(db):
        while True:
            firstName = bF.checkString("Please Enter The First Name of the Employee: ")
            lastName = bF.checkString("Please Enter The Last Name of the Employee: ")
            address = bF.checkString("Please Enter The Home Address of the Employee: ")
            email = bF.checkEmail("Please Enter the Email Address of the Employee: ")
            mobile = bF.checkPhoneNumber("Please Enter the Phone Number of the Employee: ")
            startDate = bF.checkDate("Please Enter the Employee Start Date: YYYY-MM-DD: ")
            endDate = bF.checkDate("Please Enter the Employee End Date: YYYY-MM-DD: ")

            insertCommand = "INSERT INTO myDB.Employee(firstName, surname, address, email, mobile, startDate," \
                            " endDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(insertCommand, (firstName, lastName, address, email, mobile, startDate, endDate))

            db.commit()

            bF.successMsg()

            choice = bF.checkString("Would you like to add another employee? Yes/No : ").lower()

            if choice.startswith("y"):
                continue
            elif choice.startswith("n"):
                break
            else:
                print("Invalid Input.")

        cursor.close()
        db.close()


# view all employees, for each row found, it formats and prints them back
# uses another style of print statement as first approaches were too long
def allEmployees():
    db = bF.runDB()
    cursor = db.cursor(buffered=True)
    if bF.checkConnection(db):
        selectAll = "SELECT * FROM myDB.Employee"
        cursor.execute(selectAll)

        results = cursor.fetchall()
        bF.successMsg()
        for row in results:
            print("ID: {}\nName: {} {}\nAddress: {}\nEmail: {}\nPhone: {}\nStart Date: {}\nEnd Date: {}\n".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        cursor.close()
        db.close()


# update statement according to design specification, find an employee, then update that employee
# the quick fetch employee method returns an employee tuple, which is accessed using the employee[0] syntax
def updateEmployee():
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    if bF.checkConnection(db):
        while True:
            employee = quickFetchEmployee(cursor)

            firstName = bF.checkString("Please Enter The First Name of the Employee: ")
            lastName = bF.checkString("Please Enter The Last Name of the Employee: ")
            address = bF.checkString("Please Enter The Home Address of the Employee: ")
            email = bF.checkEmail("Please Enter the Email Address of the Employee: ")
            mobile = bF.checkPhoneNumber("Please Enter the Phone Number of the Employee: ")
            startDate = bF.checkDate("Please Enter the Employee Start Date: YYYY-MM-DD: ")
            endDate = bF.checkDate("Please Enter the Employee End Date: YYYY-MM-DD: ")

            updateCommand = "UPDATE myDB.Employee SET firstName = %s, surname = %s, address = %s, email = %s, " \
                            "mobile = %s, startDate = %s, endDate = %s WHERE idEmployee = %s"

            cursor.execute(updateCommand, (firstName, lastName, address, email, mobile, startDate, endDate,
                                           employee[0]))

            db.commit()
            bF.successMsg()

            choice = bF.checkString("Would you like to update another employee? Yes/No : ").lower()

            if choice.startswith("y"):
                continue
            elif choice.startswith("n"):
                break
            else:
                print("Invalid Input.")

        cursor.close()
        db.close()


# delete statement according to design specification, find an employee, then ask whether to delete that employee
# the quick fetch employee method returns an employee tuple, which is accessed using the employee[0] syntax
def deleteEmployee():
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    if bF.checkConnection(db):
        while True:
            employee = quickFetchEmployee(cursor)

            checkSure = bF.checkString("Are you sure you want to delete this employee? Yes/No : ").lower()

            if checkSure.startswith("y"):
                deleteStatement = "DELETE FROM myDB.Employee where idEmployee = %s"
                cursor.execute(deleteStatement, [employee[0]])
                db.commit()
                bF.successMsg()

            elif checkSure.startswith("n"):
                print("Bringing you back to main menu...")
                break

            choice = bF.checkString("Would you like to delete another employee? Yes/No : ").lower()

            if choice.startswith("y"):
                continue
            elif choice.startswith("n"):
                break
            else:
                print("Invalid Input.")

        cursor.close()
        db.close()


# This function is used to enter payroll details for an employee, and then save them to the database.
def payrollDetails():
    # Run the runDB function to connect to the database and return a database object and a cursor object.
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    # Check if the connection to the database was successful.
    if bF.checkConnection(db):
        # Keep running the loop until the user decides to exit.
        while True:
            # Display a success message to the user.
            bF.successMsg()

            # Set the employee variable to None.
            employee = None

            # Keep running the loop until an employee is found.
            while employee is None:
                # Call the quickFetchEmployee function to find an employee based on the ID entered by the user.
                employee = quickFetchEmployee(cursor)

            # Prompt user for details
            hoursWorked = bF.checkInteger("Please Enter Your Hours Worked: ")
            payRate = bF.checkFloat("Please Enter Your Pay Rate: ")
            taxRate = bF.checkFloat("Please Enter Your Tax Rate: ")

            # Calculate the tax percent.
            taxPercent = "{:.2f}".format(taxRate / 100)

            # Get the current date.
            dateCreated = date.today()

            # Create the insertPayroll string and execute it with the cursor object.
            insertPayroll = "INSERT INTO myDB.Payroll(idEmployee, hoursWorked, payRate, taxRate, dateCreated) VALUES " \
                            "(%s, %s, %s, %s, %s)"
            cursor.execute(insertPayroll, (employee[0], hoursWorked, payRate, taxPercent, dateCreated))

            # Commit the changes to the database.
            db.commit()

            # Display a success message to the user.
            bF.successMsg()

            # Ask the user if they want to print a payslip.
            payslip = bF.checkString("Would you like to print a payslip for this employee? Yes/No : ").lower()

            # If the user wants to print a payslip, call the writePayslip function to create a payslip.
            if payslip.startswith("y"):
                writePayslip(employee, hoursWorked, payRate, taxRate)

                # Ask the user if they want to enter payroll details for another employee.
                choice1 = bF.checkString(
                    "Would you like to enter payroll details for another employee? Yes/No : ").lower()

                # If the user wants to enter payroll details for another employee, continue the loop.
                if choice1.startswith("y"):
                    continue

                # If the user does not want to enter payroll details for another employee, break the loop.
                elif choice1.startswith("n"):
                    break

            elif payslip.startswith("n"):

                # Ask the user if they want to enter payroll details for another employee.
                choice2 = bF.checkString(
                    "Would you like to enter payroll details for another employee? Yes/No : ").lower()

                # If the user wants to enter payroll details for another employee, continue the loop.
                if choice2.startswith("y"):
                    continue

                # If the user does not want to enter payroll details for another employee, break the loop.
                elif choice2.startswith("n"):
                    break

            else:
                print("Invalid Input.")


def calcGross(hoursWorked, payRate):
    grossPay = hoursWorked * payRate
    return grossPay


def calcNet(grossPay, taxPaid):
    netPay = grossPay - taxPaid
    return netPay


def calcTax(grossPay, taxRate):
    taxPaid = grossPay * (taxRate / 100)
    return taxPaid


def writePayslip(employee, hoursWorked, payRate, taxRate):

    # Makes the name into one string
    name = employee[1] + " " + employee[2]

    # Get Today's Date
    dateCreated = date.today()

    # Create a payslip based on design specification, which includes employee name and date created
    filename = "/Users/leecampbell/PycharmProjects/EmployeeDatabase/payslip" + f"{employee[1]+employee[2]}" + \
               f"{dateCreated}" + ".txt"

    # Calculate and get return values and variable assignment
    grossPay = calcGross(hoursWorked, payRate)
    taxPaid = calcTax(grossPay, taxRate)
    netPay = calcNet(grossPay, taxPaid)

    # Opens a filename, uses write mode, which will overwrite the existing if it exists
    # Assumption is that they will not create two payslips on the same date
    with open(filename, "w", ) as file:
        file.write("=" * 45 + "\n")
        file.write("Payslip Details".center(45) + "\n")
        file.write("=" * 45 + "\n")
        file.write("{:<20}: {}\n".format("EmpID", employee[0]))
        file.write("{:<20}: {}\n".format("EmpName", name))
        file.write("{:<20}: {}\n".format("HoursWorked", hoursWorked))
        file.write("{:<20}: €{:.2f}\n".format("PayRate", payRate))
        file.write("{:<20}: €{:.2f}\n".format("GrossPay", grossPay))
        file.write("{:<20}: €{:.2f}\n".format("TaxPaid", taxPaid))
        file.write("{:<20}: €{:.2f}\n".format("NetPay", netPay))
        file.write("=" * 45 + "\n")
        file.write("\n\n")

    print("Payslip Generated and Located @ : " + filename)


def payrollReport():
    # Run the runDB function to connect to the database and return a database object and a cursor object.
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    # Check if the connection to the database was successful.
    if bF.checkConnection(db):
        # Keep running the loop until the user decides to exit.
        while True:

            # Set the employee variable to None.
            employee = None

            # Keep running the loop until an employee is found.
            while employee is None:
                # Call the quickFetchEmployee function to find an employee based on the ID entered by the user.
                employee = quickFetchEmployee(cursor)

            # Prompt user for answer, according to design specification
            choice = bF.checkString("Would you like to run the employee payroll report? Yes/No : ").lower()
            if choice.startswith("y"):

                # employee is automatically return thanks to quickFetchEmployee method
                selectCommand = "SELECT * FROM myDB.Payroll WHERE myDB.Payroll.idEmployee = %s"
                empID = employee[0]

                cursor.execute(selectCommand, [empID])
                payrollData = cursor.fetchall()

                # Simple check, len() can be used also
                if payrollData is None:
                    print("No Payroll Data Found for this Employee")

                # If data is found, run this
                elif payrollData is not None:
                    name = employee[1] + employee[2]

                    # Create the payroll report file.
                    filename = "/Users/leecampbell/PycharmProjects/EmployeeDatabase/PayrollReport-{}.txt".format(name)

                    # Define the header for the report.
                    header = "\tEmployee ID: {:<14} | First Name: {:<15} | Last Name: {:<12}\n". \
                        format(employee[0], employee[1], employee[2])

                    # Define the body headings for the report.
                    body = "{:<12} | {:<12} | {:<12} | {:<12} | {:<12} | {:<12} | {:<12}".format(
                        "Date", "Hours Worked", "Rate of Pay", "Gross Pay", "Tax Rate", "Tax Paid", "Net Pay"
                    )

                    # Get todays date
                    today = date.today()

                    # Write the file, pass in headers and body
                    with open(filename, "w") as file:
                        # Write the header to the file.
                        file.write(header)
                        file.write("-" * 100 + "\n")

                        # Write the body headings to the file.
                        file.write(body + "\n")
                        file.write("-" * 100 + "\n")

                        # For each data row return, calculate gross pay, taxPaid, net pay and pass it in into a row
                        for data in payrollData:
                            grossPay = calcGross(data[2], data[3])
                            taxPaid = calcTax(grossPay, data[4])
                            netPay = calcNet(grossPay, taxPaid)

                            # Formats the row to align with the body headings
                            row = "{:<12} | {:<12} | {:<12} | {:<12} | {:<12} | {:<12.2f} | {:<12.2f}".format(
                                str(today), data[2], data[3], data[4], grossPay, taxPaid, netPay)

                            # For each row, write the formatted row and end with a new line
                            file.write(row + "\n")

                    print("Successfully created Report at : " + filename)

                    # Ask the user if they want to generate a report for another employee
                    choice = bF.checkString("Do you want to run the report for another employee? Yes/No : ").lower()

                    if choice.startswith("y"):
                        payrollReport()

                    elif choice.startswith("n"):
                        print("Back to the main menu...")
                        return
                    else:
                        print("Invalid Input")



            elif choice.startswith("n"):
                input("Press any key to continue...")
                return

            else:
                print("Invalid Input.")


def writeToReport():
    # Creating the file, can be replaced with C:\TEMP\
    filename = "/Users/leecampbell/PycharmProjects/EmployeeDatabase/report.txt"

    # Define the Headings for the Report
    headings = "{:<12} | {:<25} | {:<30} | {:<29} | {:<15} | {:<12}| {:<12}".format(
        "ID", "Name", "Address", "Email", "Mobile", "StartDate", "EndDate"
    )

    # Connect to the database
    db = bF.runDB()
    cursor = db.cursor(buffered=True)

    # Check if the connection was successful
    if bF.checkConnection(db):

        # Select all employees from the Employee table
        selectAll = "SELECT * FROM myDB.Employee"
        cursor.execute(selectAll)

        # Fetch all the results
        results = cursor.fetchall()

        # open file for writing
        with open(filename, "w") as file:
            # write headings
            file.write(headings + "\n")
            file.write("-" * 155 + "\n")

            # Format the employee details as a string
            for row in results:
                # Joining the name together for ease
                name = row[1] + " " + row[2]
                rowFormatted = (
                    "{:<12}".format(row[0]),
                    "{:<25}".format(name),
                    "{:<30}".format(row[3]),
                    "{:<29}".format(row[4]),
                    "{:<15}".format(row[5]),
                    "{:<11}".format(str(row[6])),
                    "{:<12}".format(str(row[7]))
                )

                # Formatting the rows and separating with |
                rowString = " | ".join(rowFormatted)

                # Write the employee details to the file
                file.write(rowString + "\n")
                file.write("-" * 155 + "\n")

        print("\nAnalytical Report Created at : " + filename)


def exportData():
    filename = "/Users/leecampbell/PycharmProjects/EmployeeDatabase/payroll.csv"

    db = bF.runDB()

    cursor = db.cursor(buffered=True)

    if bF.checkConnection(db):
        getAllCommand = "SELECT * FROM myDB.Employee, myDB.Payroll " \
                        "WHERE myDB.Employee.idEmployee = myDB.Payroll.idEmployee " \
                        "ORDER BY myDB.Payroll.idEmployee "

        cursor.execute(getAllCommand)
        results = cursor.fetchall()

        with open(filename, "w") as file:
            for row in results:
                name = row[1] + " " + row[2]
                rowFormatted = (
                    "{}".format(row[0]),
                    "{:}".format(name),
                    "{}".format(row[3]),
                    "{}".format(row[4]),
                    "{}".format(row[5]),
                    "{}".format(str(row[6])),
                    "{}".format(str(row[7])),
                    "{}".format(row[8]),
                    "{}".format(row[9]),
                    "{}".format(row[10]),
                    "{}".format(str(row[11])),
                    "{}".format(str(row[12])),
                    "{}".format(str(row[13]))
                )
                file.write(str(rowFormatted))
                file.write("\n")

        print("Data exported to: ", filename)

