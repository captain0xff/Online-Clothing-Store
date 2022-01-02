#Broke many lines in two parts cuz pylint loves it
"""This module will be used for functionalities of the employee"""
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import PySimpleGUI as sg
import mysql.connector as sqltor
from mysql.connector import errors as mysql_errors
#from datetime import datetime
import settings as st


mycon= sqltor.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor = mycon.cursor()
def Main(emp = ''):
    """This Function is responsible for the display of Employee Screen"""
    global data
    global data_product
    #global data
    sg.theme('DarkAmber')
    font = ("Arial", 11)
    stck_data = display_stock()
    stats = [[sg.Combo(default_value='Monthly Profit',
        values=['Daily Profit','Monthly Profit'],readonly=True,key = 'profit'),sg.Button('GO')],
        [sg.Button('Popularity of Categories',key = 'cat_pie')],
        [sg.Button('Total Items sold per Brand', key = 'item_sold')]]
    customer_det = cust_details()
    layout = [
        [sg.Text(f"Welcome {emp}",font=font)],
        [sg.Text('')],
        [sg.Text('Please choose the function')],
        [sg.TabGroup([
        [sg.Tab("Edit Stock Data",stck_data,key = 'Edit'),
            sg.Tab("Statistics",stats),sg.Tab("See Customer Details",customer_det)]],key='Tabs')],
        [sg.Text("")]
    ]
    win = sg.Window('Welcome',layout)
    while True:
        event,value = win.read() 
        print(event,value)

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
                prod_clicked = value['Table'][0]
                prod_click_id = int(data_product[prod_clicked][0])
                update_data(prod_click_id)
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
        if event == 'Delete':
            prod_clicked = value['Table'][0]
            prod_click_id = int(data_product[prod_clicked][0])
            #print(prod_click_id)
            cursor.execute(f"DELETE FROM PRODUCTS WHERE ID = {prod_click_id}")
            mycon.commit()
            cursor.execute("SELECT * FROM PRODUCTS")
            data_product = cursor.fetchall()
            win['Table'].update(data_product)
        if event == 'cust_Table':
            #cursor.execute('SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS')
            #data = cursor.fetchall()
            #print(data)
            em = data[value['cust_Table'][0]][2] #Basically extracting email
            #print(data[value['Table'][0]])
            win['show_det'].update(em)
            win['show'].update(disabled = False)
        
        if event == 'GO' and value['profit'] == 'Daily Profit':
            daily_profit()
        if event == 'cat_pie':
            categ_chart()
        if event == 'item_sold':
            brand_item()
        if event is None:
            break
        

def display_stock():
    """This displays the products"""
    cursor.execute("SELECT * FROM PRODUCTS")
    global data_product
    data_product = cursor.fetchall()
    for i in range(len(data_product)):
        data_product[i] = list(data_product[i])
        for j in range(len(data_product[i])):
            if isinstance(data_product[i][j],int):
                data_product[i][j] = str(data_product[i][j])
    heading = ['Prod ID','Name','Brand','Size','Quantity','Cost_Price','Selling_Price']
    layout1 = [[sg.Text('Product List')],
    [sg.Table(data_product,headings = heading,key = 'Table',justification='left'
    ,auto_size_columns=True,expand_y = True)],
    [sg.Button('Add',key = 'Add'),sg.Button('Update Stock',key = 'Update'),sg.Button('Delete',key = 'Delete')],
    ]
    return layout1
#check
def add_stock():
    """This function enables the employee to add new products in stock"""
    lay = [[sg.Text('Enter Product ID',size = (18,1)),sg.Input(key = 'id',enable_events=True)],
    [sg.Text('Product Name',size = (18,1)),sg.Input(key = 'name',enable_events=True)],
    [sg.Text('Product Brand',size = (18,1)),sg.Input(key = 'brand',enable_events=True)],
    [sg.Text('Product Size',size = (18,1)),sg.Input(key = 'size',enable_events=True)],
    [sg.Text('Product Quantity',size = (18,1)),sg.Input(key = 'quantity',enable_events=True)],
    [sg.Text('Product Cost Price',size = (18,1)),sg.Input(key = 'cost_price',enable_events=True)],
    [sg.Text('Product Selling Price',size = (18,1)),sg.Input(key ='selling_price',enable_events=True)],
    [sg.Text('Product Category',size = (18,1)),sg.Input(key ='category',enable_events=True)]]
    layout = [[sg.Frame("Add New Stock",lay)],
    [sg.Button('Go Back'),sg.Button('Confirm',key = 'Confirm',disabled=True)]
    ]
    window = sg.Window("New Product",layout=layout)
    while True:
        event,value = window.read()
        print(event,value)
        if event in (None, "Go Back"):
            window.close()
            break
        cursor.execute(f"SELECT * from products where ID  = '{value['id']}'")
        """CHECKING CONSTRAINTS"""
        prod_id = cursor.fetchone() is None
        print('141',prod_id)
        con2 = len(value['name']) <= 50
        con3 = len(value['brand']) <= 50
        con4 = value['size'] in ('S','M','L','XL', 'XXL', 'XXXL','NA')
        con5 = value['quantity'].isnumeric()
        con6 = string_float(value['cost_price'])  #Checks if valid float
        con7 = string_float(value['selling_price'])
        con8 = value['category'] in ('Kids','Men','Women')
        check = [value['id'],value['name'],value['brand'],value['size'],value['quantity'],
        value['cost_price'],value['selling_price'],value['category'],con8,con7,con6,con5,con4,con3,con2,prod_id]
        if all(check):
            window['Confirm'].update(disabled = False)
        else:
            window['Confirm'].update(disabled = True)
        if event == 'Confirm':
            insert_prod = """INSERT INTO PRODUCTS
            (ID,Name,Brand,Size,Quantity,Cost_Price,Selling_Price, Category)
            Values(%s,%s,%s,%s,%s,%s,%s,%s)"""
            upd_value = [list(value.values())] 
            cursor.executemany(insert_prod,upd_value)
            mycon.commit()
            sg.popup('Stock Added to Database')
            window.close()
            #print(upd_value)
            break
        


def update_data(ID):
    """This function allows employee to modify the details of existing stock"""
    lay = [[sg.Text('Product ID',size = (18,1),),
        sg.Input(default_text = ID, key = 'ID',readonly=True,tooltip = "It's Read Only",disabled_readonly_background_color='Gray',disabled_readonly_text_color='Black')],
    [sg.Text('Product Name',size = (18,1)),sg.Input(key = 'Name')],
    [sg.Text('Product Brand',size = (18,1)),sg.Input(key = 'Brand')],
    [sg.Text('Product Size',size = (18,1)),sg.Input(key = 'Size')],
    [sg.Text('Quantity of Product',size = (18,1)),sg.Input(key = 'Quantity')],
    [sg.Text('Cost Price of Product',size = (18,1)),sg.Input(key = 'Cost_Price')],
    [sg.Text('Selling Price of Product',size = (18,1)),sg.Input(key ='Selling_Price')]
    ]
    msg=sg.Text("Instructions: The data which is not to be updated shall be left blank")
    layout=[[msg],
        [sg.Frame("Add New Stock",lay)],
    [sg.Button('Go Back'),sg.Button('Confirm')]
    ]
    win = sg.Window('Update Data',layout,finalize=True)
    while True:
        event,value=win.read()
        if event is None:
            break
        try: 
            if event == 'Confirm':
                for i in value:
                    if value[i] != '' and i!= 'ID':
                        print(i,value[i])
                        cursor.execute(f"""UPDATE PRODUCTS SET {i} = '{value[i]}'
                        WHERE ID = {int(ID)}""")
                sg.popup('Data Updated')
                win.close()
        except mysql_errors.DatabaseError:
            msg.update('Wrong data entered...')
        #print(event,value)
        


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

def show_details(dat): #dat is a tuple containing name, mob, email, pur_amount
    #print(dat)
    heading = ['Invoice Number', 'Total Cost', 'Purchase date']
    cursor.execute(f"""SELECT INVOICE_NUMBER, PURCHASE_DATE, SUM(PRODUCT_TOT_COST) FROM PURCHASE 
    WHERE CUSTOMER_EMAIL = '{dat[2]}'
    GROUP BY INVOICE_NUMBER""")
    purchase_data = cursor.fetchall()
    print(purchase_data)
    if not purchase_data:
        sg.popup('NO DATA FOUND')  
    else:
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
    
def daily_profit():
    cursor.execute("""SELECT PURCHASE_DATE,SUM(PRODUCT_TOT_COST) FROM PURCHASE  
    GROUP BY PURCHASE_DATE 
    ORDER BY PURCHASE_DATE DESC LIMIT 7""")
    prof_day = cursor.fetchall()
    dates = [prof_day[i][0] for i in range(len(prof_day))] #Extracting dates from sql db
    amt = [prof_day[i][1] for i in range(len(prof_day))] #Extracting daily profit from sql db
    print(dates)
    plt.plot_date(dates,amt,linestyle='solid')
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b, %d %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.title('Daily Profit (Last 7 days)')
    plt.ylabel('Profit in rupees')
    plt.xlabel('Date')
    plt.show()

def categ_chart():
    cursor.execute("select sum(quantity_purchased), product_category from purchase group by product_category;")
    cat_data = cursor.fetchall()
    #print(cat_data)
    sale_data = [cat_data[i][0] for i in range(len(cat_data))]
    label = [cat_data[i][1] for i in range(len(cat_data))]
    print(sale_data,label)
    plt.pie(sale_data,labels = label,shadow=True, autopct = '%1.1f%%',wedgeprops={'edgecolor':'black'})
    plt.show()


def brand_item():
    cursor.execute("select sum(quantity_purchased), product_brand from purchase group by Product_brand;")
    sold_data = cursor.fetchall()
    no_item = [sold_data[i][0] for i in  range(len(sold_data))] #y-axis
    brand_name = [sold_data[i][1] for i in range(len(sold_data))] #x-axis
    plt.bar(brand_name,no_item)
    plt.tight_layout()
    plt.show()

def string_float(s):
    try:
        float(s)
        return True
    except:
        return False

if __name__=='__main__':
    Main()


mycon.commit()