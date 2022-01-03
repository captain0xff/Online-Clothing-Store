"""The code for the main login page"""
# Import the needed modules
import PySimpleGUI as sg
import sys
import warnings
import mysql.connector as sqltor
import time
import os


# Set the PysimpleGUI theme
sg.theme("DarkAmber")

"""Code for checking environment"""
idle = True if "idlelib.run" in sys.modules else False  # Credit goes to stackexchange
if idle == True:
    warnings.warn("This code malfunctions in IDLE... Launching in terminal...")
    time.sleep(3)
    current_dir = os.getcwd()
    os.system(f"{current_dir}/login.py")
# Connect to the mysql database and create a cursor
try:
    file=open('settings.txt')
    data=file.readlines()
    file.close()
    for i in range(len(data)):
        data[i]=data[i][:-1]
    mycon = sqltor.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])
except sqltor.errors.ProgrammingError:
    layout=[
    [sg.Text('Host',size=(7,None)),sg.Input('localhost',key='H')],
    [sg.Text('User',size=(7,None)),sg.Input('root',key='U')],
    [sg.Text('Password',size=(7,None)),sg.Input('',key='P')],
    [sg.Button('Done',key='DN')]
    ]
    window=sg.Window('Credentials',layout)
    while True:
        event,values=window.read()
        if event==sg.WIN_CLOSED:
            break
        elif event=='DN':
            hostname=values['H']
            username=values['U']
            password=values['P']
            break
    window.close()
    settings_data="""{}
{}
{}
denim_destination_db
""".format(hostname,username,password)
    file=open('settings.txt','w')
    file.write(settings_data)
    file.close()
    import create_database
    mycon = sqltor.connect(host=hostname, user=username, passwd=password, database='denim_destination_db')
import employee_func
import purchasing

cursor = mycon.cursor()

def Main_menu():
    # The welcome menu
    image = "Logo.gif"
    layout = [
        [sg.Image(key="IMG")],
        [
            sg.Btn("Customer Login", key="CL", expand_x=True),
            sg.Btn("Employee Login", key="EL", expand_x=True),
        ],
    ]

    # Create the main menu window
    window = sg.Window(
        'Denim Destination', layout, finalize=True, element_justification="center"
    )
    img = window["IMG"]
    option_choosen = None

    rng = True
    while rng:
        # Take events and values
        e, v = window.read(timeout=1)
        if e == sg.WIN_CLOSED:
            rng = False
        elif e == "CL":
            option_choosen = 1
            rng = False

        elif e == "EL":
            option_choosen = 0
            rng = False
        img.update_animation_no_buffering(image, 2000)

    # If any option is selected close the main window
    window.close()

    if option_choosen == 1:
        Customer_sign_in_menu()
    elif option_choosen == 0:
        Employee_sign_in_menu()


def Employee_sign_in_menu():
    """
    If the user chooses Employee in the window produced by custEmp(), this function is called
    It is a login page for the employees
    """
    msg = sg.Text("Please Login...", size=(50, 1))
    layout = [
        [msg],
        [sg.Text("Employee ID: "), sg.Input(key="id")],
        [sg.Text("User Name:   "), sg.Input(key="uname")],
        [sg.Text("Password:     "), sg.Input(key="password", password_char="\u2022")],
        [sg.Button("Login"), sg.Button("Go Back")],
    ]
    # password_char parameter masks the given password with *
    window = sg.Window("Login - Employee", layout)
    option_choosen = None
    while True:
        event, values = window.read()
        # values variable points at a dictionary with id, uname and password
        if event == sg.WIN_CLOSED:
            break
        if event == "Go Back":
            option_choosen = 2
            break
        elif event == "Login":
            if values["id"] and values["uname"] and values["password"]:
                if values["id"][-1] in "0123456789":
                    cursor.execute(
                        "SELECT * FROM EMPLOYEES WHERE ID = %d;" % (int(values["id"]))
                    )
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        # Checks if an employee with the given credentials exists of not
                        if (
                            data[0][2] == values["uname"]
                            and data[0][3] == values["password"]
                        ):
                            option_choosen = 1
                            break
                    msg.update(
                        value="Invalid employee ID, username or password...",
                        text_color="red",
                    )
                    print("\a")
                else:
                    msg.update(
                        "Please enter positive integer in employee ID...",
                        text_color="red",
                    )
                    print("\a")
            else:
                # If the user doesn't input any ID and clicks Login
                msg.update(value="Please enter all the data", text_color="red")
                print("\a")

    window.close()

    if option_choosen == 1:
        employee_func.Main()
    elif option_choosen == 2:
        Main_menu()


def Customer_sign_in_menu():
    # Customer sign_in menu
    # The layout for the sign in window
    msg = sg.Text("Login to access our wide range of products...")
    layout = [
        [msg],
        [sg.Text("Email ID", size=(7, 1)), sg.Input("", key="ID")],
        [
            sg.Text("Password", size=(7, 1)),
            sg.Input("", key="PD", password_char="\u2022"),
        ],
        [
            sg.Btn("Login", key="OK"),
            sg.Btn("Go Back", key="GB"),
            sg.Btn("Sign up", key="SN"),
        ],
    ]

    # Create the sign in window
    window = sg.Window("Customer Sign in", layout)

    # Some variables
    option_choosen = None

    rng = True
    while rng:
        # Take events and values
        e, v = window.read()
        if e == sg.WIN_CLOSED:
            rng = False
        elif e == "GB":
            option_choosen = 2
            rng = False
        elif e == "SN":
            Customer_sign_up()
        elif e == "OK":
            email = v["ID"]
            passwd = v["PD"]
            if email and passwd:
                cursor.execute("select email_id,password from customers")
                data = cursor.fetchall()
                for i in data:
                    if email == i[0] and passwd == i[1]:
                        option_choosen = 1
                        rng = False
                        break
                else:
                    msg.update(value="Invalid email or password...", text_color="red")
                    print("\a")
            else:
                msg.update(value="Please enter all the data...", text_color="red")
                print("\a")
    window.close()
    if option_choosen == 1:
        purchasing.mycon.commit()
        purchasing.Main(email)
    elif option_choosen == 2:
        Main_menu()


def Customer_sign_up():
    # Menu for new customers to sign_up
    # Create the sign up button and store it in a var for future usage
    button = sg.Btn("Sign up", key="DN", disabled=True)

    # The layout of the window
    msg = sg.Text("New to Denim Destination? Sign up..", size=(50, 1))
    layout = [
        [msg],
        [sg.Text("Email ID", size=(8, 1)), sg.Input("", key="EI")],
        [
            sg.Text("Password", size=(8, 1)),
            sg.Input("", key="PD", password_char="\u2022"),
        ],
        [sg.Text("Name", size=(8, 1)), sg.Input("", key="NM")],
        [sg.Text("Phone No.", size=(8, 1)), sg.Input("", key="PH")],
        [
            sg.Checkbox(
                "I agree to the terms and conditions", key="CK", enable_events=True
            )
        ],
        [button, sg.Btn("Cancel", key="CN2")],
    ]

    # Create the window for sign up
    window = sg.Window("Customer Sign up", layout)

    # Add data to the customer data base
    command = "insert into customers values('{name}','{ph}','{email}','{passwd}',0)"

    rng = True
    while rng:
        # Take events and values
        e, v = window.read()
        if e == sg.WIN_CLOSED or e == "CN2":
            rng = False
        elif v["CK"] == True:
            button.update(disabled=False)
        if e == "DN":
            name = v["NM"]
            email = v["EI"]
            password = v["PD"]
            phone_no = v["PH"]
            if name and email and password and phone_no:
                if len(phone_no) == 10 and phone_no[0] != "0":
                    cursor.execute("select Email_ID,Phone_Number from customers")
                    data = cursor.fetchall()
                    for i in data:
                        if email == i[0] or phone_no == i[1]:
                            msg.update(
                                "Another account has the same email or phone number...",
                                text_color="red",
                            )
                            print("\a")
                            break
                    else:
                        command = command.format(
                            name=name, ph=phone_no, email=email, passwd=password
                        )
                        cursor.execute(command)
                        mycon.commit()
                        rng = False
                else:
                    msg.update("Invalid phone number...", text_color="red")
                    print("\a")
            else:
                msg.update("Please enter all the data...", text_color="red")
                print("\a")

    # Close the window
    window.close()


# Run the code only if the current file run
if __name__ == "__main__":
    Main_menu()
