'''The code for the main login page'''
#Import the needed modules
import PySimpleGUI as sg
import mysql.connector as sql
import settings as st

#Connect to the mysql database and create a cursor
mycon=sql.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor=mycon.cursor()

#Set the PysimpleGUI theme
sg.theme('DarkAmber')

def Main_menu():
    #The welcome menu
    layout=[[sg.Image('Logo.png')],
            [sg.Btn('Customer Login',key='CL',size=(29,2)),sg.Btn('Employee Login',key='EL',size=(28,2))]]

    #Create the main menu window
    window=sg.Window(st.caption,layout)

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        if e==sg.WIN_CLOSED:
            rng=False
        elif e=='CL':
            Customer_sign_in_menu()

        elif e=='EL':
            Employee_sign_in_menu()

    #If any option is selected close the main window
    window.close()


def Employee_sign_in_menu():
    #Employee sign_in menu
    pass


def Customer_sign_in_menu():
    #Customer sign_in menu
    #The layout for the sign in window
    msg=sg.Text('Please Login...',size=(30,1))
    layout=[[msg],
            [sg.Text('Email ID',size=(8,1)),sg.Input('',key='ID')],
            [sg.Text('Password',size=(8,1)),sg.Input('',key='PD')],
            [sg.Btn('Login',key='OK'),sg.Btn('Sign up',key='SN')]]

    #Create the sign in window
    window=sg.Window(st.caption,layout)

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        if e==sg.WIN_CLOSED:
            rng=False
        elif e=='SN':
            Customer_sign_up()
        elif e=='OK':
            email=v['ID']
            passwd=v['PD']
            cursor.execute('select email_id,password from customer')
            data=cursor.fetchall()
            for i in data:
                if email==i[0] and passwd==i[1]:
                    rng=False
                    break
            else:
                msg.update(value='Invalid email or password...')

    window.close()


def Customer_sign_up():
    #Menu for new customers to sign_up
    #Create the sign up button and store it in a var for future usage
    button=sg.Btn('Sign up',key='DN',disabled=True)

    #The layout of the window
    layout=[[sg.Text('Please sign up...')],
            [sg.Text('Email ID',size=(8,1)),sg.Input('',key='EI')],
            [sg.Text('Password',size=(8,1)),sg.Input('',key='PD')],
            [sg.Text('Name',size=(8,1)),sg.Input('',key='NM')],
            [sg.Text('Phone No.',size=(8,1)),sg.Input('',key='PH')],
            [sg.Checkbox('I agree to the terms and conditions',key='CK',enable_events=True)],
            [button,sg.Btn('Cancel',key='CN2')]]

    #Create the window for sign up
    window=sg.Window(st.caption,layout)

    #Add data to the customer data base
    command='insert into customer values({name},{ph},{email},{passwd},0)'

    rng=True
    while rng:
        #Take events and values
        e,v=window.read()
        print(e,v)
        if e==sg.WIN_CLOSED or e=='CN2':
            rng=False
        elif v['CK']==True:
            button.update(disabled=False)
        if e=='DN':
            name='\''+v['NM']+'\''
            email='\''+v['EI']+'\''
            password='\''+v['PD']+'\''
            command=command.format(name=name,ph=int(v['PH']),email=email,passwd=password)
            print(command)
            cursor.execute(command)
            mycon.commit()
            rng=False

    #Close the window
    window.close()


#Run the code only if the current file run
if __name__=='__main__':
    Main_menu()
