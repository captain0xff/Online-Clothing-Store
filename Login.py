import PySimpleGUI as sg
import mysql.connector as sqltor

def denimDestination():
    def custEmp():
        """This function asks the user if he/she is a customer or an employee."""
        sg.theme('DarkAmber')
        layout = [[sg.Text('Welcome to Denim Destination: ')],
                  [sg.Text('Are you an Employee? ')],
                  [sg.Text('Or are you a Customer ?')],
                  [sg.Button('Employee'), sg.Button('Customer'), sg.Button('Exit')]]

        window = sg.Window('WELCOME', layout, margins=(50, 50))
        while True:
            event, values = window.read()
            break
        window.close()
        return event


    def loginEmp():
        """
        If the user chooses Employee in the window produced by custEmp(), this function is called
        It is a login page for the employees
        """
        sg.theme('DarkAmber')
        layout = [[sg.Text('Employee ID: '), sg.Input(key = 'id')],
                  [sg.Text('User Name:   '), sg.Input(key='uname')],
                  [sg.Text('Password:     '), sg.Input(key='password', password_char='*')],
                  [sg.Button('Login'), sg.Button('Exit'), sg.Button('Go Back')]]
        #password_char parameter masks the given password with *
        window = sg.Window('Login - Employee', layout)
        while True:
            event, values = window.read()
            #values variable points at a dictionary with id, uname and password
            print(values)
            if event in (None, 'Exit', 'Go Back'):
                break
            elif event=='Login':
                if values['id']:
                    cursor.execute('SELECT * FROM EMPLOYEES WHERE ID = %d;' %(int(values['id'])))
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        #Checks if an employee with the given credentials exists of not
                        if data[0][2]==values['uname'] and data[0][3]==values['password']:
                            confirm = sg.popup_ok('Login Successful')
                            window.close()
                            return confirm
                    sg.popup_ok('User name or Password Incorrect')
                else:
                    #If the user doesn't input any ID and clicks Login
                    sg.popup_ok('Please Enter Some Data')
        window.close()
        return event



    def cust():
        """
        If the user chooses Customer in the window produced by custEmp(), this function is called
        This is a Login/Sign Up Page for Customers.
        """
        sg.theme('DarkAmber')
        layout = [[sg.Text('Login or Sign Up: ')],
                  [sg.Text('Do you want to Login? ----> '), sg.Button('Log-in', size=(10, 1))],
                  [sg.Text('Do you want to Sign Up? ----> '), sg.Button('Sign Up', size=(10, 1))],
                  [sg.Button('Go Back')]]
        window = sg.Window('Customer', layout, margins=(50, 50))
        while True:
            event, values = window.read()
            print(event)
            if event in (None, 'Exit', 'Go Back'):
                break
        window.close()
        return event



    mycon = sqltor.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'denim_destination_db')
    cursor = mycon.cursor()


    empCust = custEmp()
    while True:
        if empCust=='Employee':
            confirm = loginEmp()
            if confirm=='Go Back':
                empCust = custEmp()
            if confirm=='Exit' or confirm=='OK':
                break

        elif empCust=='Customer':
            logSign = cust()
            if logSign=='Go Back':
                empCust = custEmp()
            if logSign=='Exit':
                break
        elif empCust=='Exit':
            break

denimDestination()

