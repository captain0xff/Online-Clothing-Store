#Broke many lines in two parts cuz pylint loves it
"""This module will be used for functionalities of the employee"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import PySimpleGUI as sg
import mysql.connector as sqltor
import settings as st
import csv

mycon= sqltor.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor = mycon.cursor()
def Main(emp = ''):
    global data
    """This Function is responsible for the display of Employee Screen"""
    #global data
    sg.theme('DarkAmber')
    font = ("Arial", 11)
    stck_data = display_stock()
    finance = [[sg.Button('Daily Profit',key = "Daily Profit")]]
    customer_det = cust_details()
    layout = [
        [sg.Text(f"Welcome {emp}",font=font)],
        [sg.Text('')],
        [sg.Text('Please choose the function')],
        [sg.TabGroup([
        [sg.Tab("Edit Stock Data",stck_data,key = 'Edit'),
            sg.Tab("Show Profit Analysis",finance),sg.Tab("See Customer Details",customer_det)]],key='Tabs')],
        [sg.Text("")]
    ]
    win = sg.Window('Welcome',layout)
    while True:
        event,value = win.read() #Values variable was getting wasted
        if event == 'Delete':
            #prod_id = 
            pass
        if event == 'show':
            #print(value)
            show_details(data[value['cust_Table'][0]])
        if event == 'Add':
            add_stock()
            cursor.execute("SELECT * FROM PRODUCTS")
            data = cursor.fetchall()
            win['Table'].update(data)
        
        if event == 'Update':
            try:
                update_data(value['Table'][0]+1)
                cursor.execute("SELECT * FROM PRODUCTS")
                data = cursor.fetchall()
                win['Table'].update(data)
            except IndexError:
                sg.popup( "Warning: No Product Selected",title = "WARNING")
        if event == "sort_amt":
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            ORDER BY Total_Price DESC"""
            cursor.execute(query)
            
            data =  cursor.fetchall()
            #sg.Print(data1)
            win['cust_Table'].update(data)
            #print('Meow')
        if event in ('search_name','Name') and value:
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Name LIKE '{value['Name']}%'"""
            cursor.execute(query)
            data =  cursor.fetchall()
            #print(data)
            win['cust_Table'].update(data)
            #break
        elif event == 'search_email':
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Email_ID = '{value['email']}'"""
            #print(query)
            cursor.execute(query)
            data =  cursor.fetchall()
            #print(data)
            win['cust_Table'].update(data)
        elif event == 'search_phn':
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Phone_Number = '{value['mob']}'"""
            #print(query)
            cursor.execute(query)
            data =  cursor.fetchall()
            #print(data)
            win['cust_Table'].update(data)
        if event == 'cust_Table':
            #cursor.execute('SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS')
            #data = cursor.fetchall()
            #print(data)
            em = data[value['cust_Table'][0]][2] #Basically extracting email
            #print(data[value['Table'][0]])
            win['show_det'].update(em)
            win['show'].update(disabled = False)
        
        if event == 'Daily Profit':
            profit_analysis()
        if event is None:
            break
        

def display_stock():
    """This displays the products"""
    cursor.execute("SELECT * FROM PRODUCTS")
    data = cursor.fetchall()
    for i in range(len(data)):
        data[i] = list(data[i])
        for j in range(len(data[i])):
            if isinstance(data[i][j],int):
                data[i][j] = str(data[i][j])
    heading = ['Prod ID','Name','Brand','Size','Quantity','Cost_Price','Selling_Price']
    layout1 = [[sg.Text('Product List')],
    [sg.Table(data,headings = heading,key = 'Table',justification='left'
    ,auto_size_columns=True,expand_y = True)],
    [sg.Button('Add',key = 'Add'),sg.Button('Update Stock',key = 'Update'),sg.Button('Delete',key = 'Delete')],
    ]
    return layout1
#check
def add_stock():
    """This function enables the employee to add new products in stock"""
    lay = [[sg.Text('Enter Product ID',size = (18,1)),sg.Input(key = 'id')],
    [sg.Text('Enter Product Name',size = (18,1)),sg.Input(key = 'name')],
    [sg.Text('Enter Product Brand',size = (18,1)),sg.Input(key = 'brand')],
    [sg.Text('Enter Product Size',size = (18,1)),sg.Input(key = 'size')],
    [sg.Text('Quantity of Product',size = (18,1)),sg.Input(key = 'quantity')],
    [sg.Text('Cost Price of Product',size = (18,1)),sg.Input(key = 'cost_price')],
    [sg.Text('Selling Price of Product',size = (18,1)),sg.Input(key ='selling_price')]
    ]
    layout = [[sg.Frame("Add New Stock",lay)],
    [sg.Button('Go Back'),sg.Button('Confirm')]
    ]
    window = sg.Window("New Product",layout=layout)
    while True:
        event,value = window.read()
        #print(event,value)
        if event == 'Confirm':
            sg.popup('Stock Added to Database')
            window.close()
            insert_prod = """INSERT INTO PRODUCTS
            (ID,Name,Brand,Size,Quantity,Cost_Price,Selling_Price)
            Values(%s,%s,%s,%s,%s,%s,%s)"""
            upd_value = [list(value.values())]
            cursor.executemany(insert_prod,upd_value)
            #print(upd_value)
            break
        if event in (None, "Go Back"):
            window.close()
            break


def update_data(ID):
    """This function allows employee to modify the details of existing stock"""
    lay = [[sg.Text('Product ID',size = (18,1)),
        sg.Input(default_text = ID, key = 'ID',readonly=True,tooltip = "It's Read Only")],
    [sg.Text('Product Name',size = (18,1)),sg.Input(key = 'Name')],
    [sg.Text('Product Brand',size = (18,1)),sg.Input(key = 'Brand')],
    [sg.Text('Product Size',size = (18,1)),sg.Input(key = 'Size')],
    [sg.Text('Quantity of Product',size = (18,1)),sg.Input(key = 'Quantity')],
    [sg.Text('Cost Price of Product',size = (18,1)),sg.Input(key = 'Cost_Price')],
    [sg.Text('Selling Price of Product',size = (18,1)),sg.Input(key ='Selling_Price')]
    ]
    layout=[[sg.Text("Instructions: The data which is not to be updated shall be left blank")],
        [sg.Frame("Add New Stock",lay)],
    [sg.Button('Go Back'),sg.Button('Confirm')]
    ]
    win = sg.Window('Update Data',layout,finalize=True)
    while True:
        event,value = win.read()
        #print(event,value)
        if event == 'Confirm':
            for i in value:
                if value[i] != '' and i!= 'ID':
                    print(i,value[i])
                    cursor.execute(f"""UPDATE PRODUCTS SET {i} = '{value[i]}'
                    WHERE ID = {int(ID)}""")
                    print('Meow Testing')
            sg.popup('Data Updated')
            win.close()
        #print(event,value)
        if event is None:
            break



cursor.execute('SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS')
data = cursor.fetchall()
def cust_details():
    global data
    #cursor.execute('SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS')
    #d = cursor.fetchall()
    #print('data',data)
    heading = ['Name','Phone_Number','Email_ID','Total_Purchase_Amt']
    table = sg.Table(data,headings=heading,key = 'cust_Table',enable_events=True)
    layout = [[sg.Radio("Sort by Purchase Amount",group_id='sort',key = 'sort_amt',enable_events=True),sg.Radio("Sort by Purchse Date",group_id='sort',key = 'sort_date',enable_events=True)],
    [sg.Text('Search by Name',size = (14,1)),sg.Input(key = 'Name',enable_events=True),sg.Button('Search',key = 'search_name')],
    [sg.Text('Search by Email ID',size = (14,1)),sg.Input(key = 'email'),sg.Button('Search',key = 'search_email')],
    [sg.Text('Search by Mobile',size = (14,1)),sg.Input(key = 'mob'),sg.Button('Search',key = 'search_phn')],
    [table],
    [sg.Input(key = 'show_det'),sg.Button('Show Details', disabled=True,key = 'show')],
    [sg.Button('Exit')]
    ]
    #print('layout',list(layout[4]))
    return layout

def show_details(dat):
    try: 
        with open(f'Customer data//{dat[2]}.csv') as f: #Opens the csv file 
            rdr = csv.reader(f)
            heading = next(rdr) 
            #print(heading)
            purchase_data = list(rdr)
            #print("DATA",dat)
            #print('pur data',purchase_data)
            table = sg.Table(purchase_data,headings=heading)
        layout = [
            [sg.Text(f'Name: {dat[0]}')],
            [sg.Text(f'Mobile Number: {dat[1]}')],
            [sg.Text(f'Email: {dat[2]}')],
            [sg.Text(f'Total Amount Purchased: {round(dat[3],2)}')],
            [table],
            [sg.Button('Exit',key = 'Exit')] 
        ]
        win = sg.Window(f'{dat[2]}',layout)
        while True:
            #print("Lol")
            
            event1,value = win.read()
            #print(event1,value)
            if event1  in ('Exit',None):
                win.close()
                break
    except FileNotFoundError:
        sg.popup("NO RECORDS FOUND")
def profit_analysis():
    cursor.execute("SELECT Purchase_Date,SUM(Purchase_Amount) FROM PURCHASE GROUP BY Purchase_Date")
    data = cursor.fetchall()
    day = []
    sale = []
    for i in range(len(data)):
        day.append(data[i][0])
        sale.append(data[i][1])
    print(day)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot(day, sale, color='red', marker='o')
    plt.title('Sale per Day', fontsize=14)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Total Sale Amount', fontsize=14)
    plt.grid(True)
    plt.show()

if __name__=='__main__':
    Main()


mycon.commit()