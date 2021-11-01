'''The code for the main login page'''
#Import the needed modules
import PySimpleGUI as sg
import mysql.connector as sql
import settings as st
import employee_func
import purchasing

#Connect to the mysql database and create a cursor
mycon=sql.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor=mycon.cursor()

#Set the PysimpleGUI theme
sg.theme('DarkAmber')

def Main_menu():
    #The welcome menu
    layout=[[sg.Image('Logo.png',key='IMG')],
            [sg.Btn('Customer Login',key='CL',size=(29,2)),sg.Btn('Employee Login',key='EL',size=(29,2))]]

    #Create the main menu window
    window=sg.Window(st.caption,layout,finalize=True)
    window['IMG'].expand(True,True,True)

    option_choosen=None

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        if e==sg.WIN_CLOSED:
            rng=False
        elif e=='CL':
            option_choosen=1
            rng=False

        elif e=='EL':
            option_choosen=0
            rng=False

    #If any option is selected close the main window
    window.close()

    if option_choosen==1:
        Customer_sign_in_menu()
    elif option_choosen==0:
        Employee_sign_in_menu()



def Employee_sign_in_menu():
    """
    If the user chooses Employee in the window produced by custEmp(), this function is called
    It is a login page for the employees
    """
    msg = sg.Text('Please Login...',size=(50,1))
    layout = [[msg],
              [sg.Text('Employee ID: '), sg.Input(key='id')],
              [sg.Text('User Name:   '), sg.Input(key='uname')],
              [sg.Text('Password:     '), sg.Input(key='password', password_char='*')],
              [sg.Button('Login'), sg.Button('Go Back')]]
    # password_char parameter masks the given password with *
    window = sg.Window('Login - Employee', layout)
    option_choosen=None
    while True:
        event, values = window.read()
        # values variable points at a dictionary with id, uname and password
        if event==sg.WIN_CLOSED:
            break
        if event=='Go Back':
            option_choosen=2
            break
        elif event == 'Login':
            if values['id'][-1] in '0123456789':
                if values['id'] and values['uname'] and values['password']:
                    cursor.execute('SELECT * FROM EMPLOYEES WHERE ID = %d;' % (int(values['id'])))
                    data = cursor.fetchall()
                    print(data)
                    if data:
                        # Checks if an employee with the given credentials exists of not
                        if data[0][2] == values['uname'] and data[0][3] == values['password']:
                            option_choosen=1
                            break
                    msg.update(value = 'Invalid employee ID, username or password...')
                else:
                    # If the user doesn't input any ID and clicks Login
                    msg.update(value = 'Please enter all the data')
            else:
                msg.update('Please enter positive integer in employee ID...')
    window.close()

    if option_choosen==1:
        employee_func.Main()
    elif option_choosen==2:
        Main_menu()


def Customer_sign_in_menu():
    #Customer sign_in menu
    #The layout for the sign in window
    msg=sg.Text('Please Login...',size=(30,1))
    layout=[[msg],
            [sg.Text('Email ID',size=(8,1)),sg.Input('',key='ID')],
            [sg.Text('Password',size=(8,1)),sg.Input('',key='PD',password_char='*')],
            [sg.Btn('Login',key='OK'),sg.Btn('Go Back',key='GB'),sg.Btn('Sign up',key='SN')]]

    #Create the sign in window
    window=sg.Window('Customer Sign in',layout)

    #Some variables
    option_choosen=None

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        if e==sg.WIN_CLOSED:
            rng=False
        elif e=='GB':
            option_choosen=2
            rng=False
        elif e=='SN':
            Customer_sign_up()
        elif e=='OK':
            email=v['ID']
            passwd=v['PD']
            if email and passwd:
                cursor.execute('select email_id,password from customers')
                data=cursor.fetchall()
                for i in data:
                    if email==i[0] and passwd==i[1]:
                        option_choosen=1
                        rng=False
                else:
                    msg.update(value='Invalid email or password...')
            else:
                msg.update(value='Please enter all the data...')
    window.close()
    if option_choosen==1:
        purchasing.Main(email)
    elif option_choosen==2:
        Main_menu()


def Customer_sign_up():
    #Menu for new customers to sign_up
    #Create the sign up button and store it in a var for future usage
    button=sg.Btn('Sign up',key='DN',disabled=True)

    #The layout of the window
    msg=sg.Text('Please sign up...',size=(50,1))
    layout=[[msg],
            [sg.Text('Email ID',size=(8,1)),sg.Input('',key='EI')],
            [sg.Text('Password',size=(8,1)),sg.Input('',key='PD',password_char='*')],
            [sg.Text('Name',size=(8,1)),sg.Input('',key='NM')],
            [sg.Text('Phone No.',size=(8,1)),sg.Input('',key='PH')],
            [sg.Checkbox('I agree to the terms and conditions',key='CK',enable_events=True)],
            [button,sg.Btn('Cancel',key='CN2')]]

    #Create the window for sign up
    window=sg.Window('Customer Sign up',layout)

    #Add data to the customer data base
    command="insert into customers values('{name}','{ph}','{email}','{passwd}',0)"

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        if e==sg.WIN_CLOSED or e=='CN2':
            rng=False
        elif v['CK']==True:
            button.update(disabled=False)
        if e=='DN':
            name=v['NM']
            email=v['EI']
            password=v['PD']
            phone_no=v['PH']
            if name and email and password and phone_no:
                if len(phone_no)==10 and phone_no[0]!='0':
                    cursor.execute('select Email_ID,Phone_Number from customers')
                    data=cursor.fetchall()
                    for i in data:
                        if email==i[0] or phone_no==i[1]:
                            msg.update('Another account has the same email or phone number...')
                            break
                    else:
                        command=command.format(name=name,ph=phone_no,email=email,passwd=password)
                        cursor.execute(command)
                        mycon.commit()
                        rng=False
                else:
                    msg.update('Invalid phone number...')
            else:
                msg.update('Please enter all the data...')



    #Close the window
    window.close()


#Run the code only if the current file run
if __name__=='__main__':
    Main_menu()