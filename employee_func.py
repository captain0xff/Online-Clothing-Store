"""This module will be used for functionalities of the employee"""
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import PySimpleGUI as sg
import mysql.connector as sqltor
from mysql.connector import errors as mysql_errors
from mysql.connector.locales.eng import client_error

file=open('settings.txt')
data=file.readlines()
file.close()
for i in range(len(data)):
    data[i]=data[i][:-1]
mycon = sqltor.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])
cursor = mycon.cursor()
def main(emp = ''):
    """This Function is responsible for the display of Employee Screen"""
    global data
    global data_product
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
        if event in (None, 'Exit'):
            break
        if event == 'show':
            show_details(data[value['cust_Table'][0]])
        if event == 'Add':
            add_stock()
            cursor.execute("SELECT * FROM PRODUCTS")
            data = cursor.fetchall()
            win['Table'].update(data)
        elif event == 'Update':
            try:
                prod_clicked = value['Table'][0]
                prod_click_id = int(data_product[prod_clicked][0])
                update_data(prod_click_id)
                cursor.execute("SELECT * FROM PRODUCTS")
                data = cursor.fetchall()
                win['Table'].update(data)
            except IndexError:
                sg.popup( "Warning: No Product Selected",title = "WARNING")
        elif event == 'Delete' :
            try:
                prod_clicked = value['Table'][0]
                prod_click_id = int(data_product[prod_clicked][0])
                #print(prod_click_id)
                cursor.execute(f"DELETE FROM PRODUCTS WHERE ID = {prod_click_id}")
                mycon.commit()
                cursor.execute("SELECT * FROM PRODUCTS")
                data_product = cursor.fetchall()
                win['Table'].update(data_product)
            except IndexError:
                sg.popup('NO PRODUCTS SELECTED')
        if event == "sort_amt":
            query = """SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            ORDER BY Total_Price DESC"""
            cursor.execute(query)
            data =  cursor.fetchall()
            win['cust_Table'].update(data)
        if event in ('search_name','Name') and value:
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Name LIKE '{value['Name']}%'"""
            cursor.execute(query)
            data =  cursor.fetchall()
            win['cust_Table'].update(data)
        elif event in ('search_email','email'):
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Email_ID LIKE '{value['email']}%'"""
            cursor.execute(query)
            data =  cursor.fetchall()
            win['cust_Table'].update(data)
        elif event in('search_phn','mob'):
            query = f"""SELECT Name,Phone_Number,Email_ID,Total_Price FROM CUSTOMERS
            WHERE Phone_Number LIKE '{value['mob']}%'"""
            #print(query)
            cursor.execute(query)
            data =  cursor.fetchall()
            #print(data)
            win['cust_Table'].update(data)
        if event == 'cust_Table' and value['cust_Table']!=[]:
            em = data[value['cust_Table'][0]][2] #Basically extracting email
            win['show_det'].update(em)
            win['show'].update(disabled = False)
        if event == 'GO' and value['profit'] == 'Daily Profit':
            daily_profit()
        elif event == 'GO' and value['profit'] == 'Monthly Profit':
            monthly()
        elif event == 'cat_pie':
            categ_chart()
        elif event == 'item_sold':
            brand_item()
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
    [sg.Button('Add',key = 'Add'),sg.Button('Update Stock',key = 'Update'),
        sg.Button('Delete',key = 'Delete')]]
    return layout1
def add_stock():
    """This function enables the employee to add new products in stock"""
    msg = sg.Text('Enter appropriate data')
    lay = [[msg],[sg.Text('Enter Product ID',size = (18,1)),
            sg.Input(key = 'id',enable_events=True)],
    [sg.Text('Product Name',size = (18,1)),sg.Input(key = 'name',enable_events=True)],
    [sg.Text('Product Brand',size = (18,1)),sg.Input(key = 'brand',enable_events=True)],
    [sg.Text('Product Size',size = (18,1)),sg.Input(key = 'size',enable_events=True)],
    [sg.Text('Product Quantity',size = (18,1)),sg.Input(key = 'quantity',enable_events=True)],
    [sg.Text('Product Cost Price',size = (18,1)),sg.Input(key = 'cost_price',enable_events=True)],
    [sg.Text('Product Sell Price',size=(18,1)),sg.Input(key ='selling_price',enable_events=True)],
    [sg.Text('Product Category',size = (18,1)),sg.Input(key ='category',enable_events=True)]]
    layout = [[sg.Frame("Add New Stock",lay)],
    [sg.Button('Go Back'),sg.Button('Confirm',key = 'Confirm')]
    ]
    window = sg.Window("New Product",layout=layout)
    while True:
        event,value = window.read()
        #print(event,value)
        if event in (None, "Go Back"):
            window.close()
            break
        try:
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
        except mysql_errors.DatabaseError:
            msg.update("WRONG DATA ENTERED",text_color='Red')
def update_data(ID):
    """This function allows employee to modify the details of existing stock"""
    lay = [[sg.Text('Product ID',size = (18,1),),
        sg.Input(default_text = ID, key = 'ID',readonly=True,tooltip = "It's Read Only",
            disabled_readonly_background_color='Gray',disabled_readonly_text_color='Black')],
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
    """This function shows the list of customers"""
    global data
    heading = ['Name','Phone_Number','Email_ID','Total_Purchase_Amt']
    table = sg.Table(data,headings=heading,key = 'cust_Table',enable_events=True)
    layout = [[sg.Radio("Sort by Purchase Amount",group_id='sort',key = 'sort_amt',
        enable_events=True),
        sg.Radio("Sort by Purchse Date",group_id='sort',key = 'sort_date',enable_events=True)],
    [sg.Text('Search by Name',size = (14,1)),sg.Input(key = 'Name',enable_events=True),
        sg.Button('Search',key = 'search_name')],
    [sg.Text('Search by Email ID',size = (14,1)),sg.Input(key = 'email',enable_events=True),
        sg.Button('Search',key = 'search_email')],
    [sg.Text('Search by Mobile',size = (14,1)),sg.Input(key = 'mob',enable_events=True),
        sg.Button('Search',key = 'search_phn')],
    [table],
    [sg.Input(key = 'show_det'),sg.Button('Show Details', disabled=True,key = 'show')],
    [sg.Button('Exit')]
    ]
    return layout

def show_details(dat):#dat is a tuple containing name, mob, email, pur_amount
    """This function shows the details of the customer"""
    heading = ['Invoice Number', 'Total Cost', 'Purchase date']
    cursor.execute(f"""SELECT INVOICE_NUMBER, PURCHASE_DATE, SUM(PRODUCT_TOT_COST) FROM PURCHASE
    WHERE CUSTOMER_EMAIL = '{dat[2]}'
    GROUP BY INVOICE_NUMBER""")
    purchase_data = cursor.fetchall()
    print(1,purchase_data)
    if not purchase_data:
        sg.popup('NO DATA FOUND')
    
    else:
        table = sg.Table(purchase_data,headings=heading,key='pur_table',enable_events=True)
        layout = [
        [sg.Text(f'Name: {dat[0]}')],
        [sg.Text(f'Mobile Number: {dat[1]}')],
        [sg.Text(f'Email: {dat[2]}')],
        [sg.Text(f'Total Amount Purchased: {round(dat[3],2)}')],
        [table],
        [sg.Button('Exit',key = 'Exit'),sg.Button('Show More',disabled = True,key='show_more')]
        ]
        win = sg.Window(f'{dat[2]}',layout)
        while True:
            event1,value = win.read()  #Extracting only event
            print(event1, value)
            if event1  in ('Exit',None):
                win.close()
                break
            if event1 == 'pur_table' and value['pur_table'] != []:
                win['show_more'].update(disabled=False)
            if event1 == 'show_more' and value['pur_table'] != []:
                ind_select = value['pur_table'][0]
                inv_num = purchase_data[ind_select][0]
                date = purchase_data[ind_select][1]
                more_details(inv_num,date)
                
def more_details(invoice,date):
    print(254,invoice)
    cursor.execute(f"""SELECT Product_ID ,Product_Name ,Product_Brand ,Product_Size ,
            Product_Category ,Quantity_Purchased ,Product_tot_cost FROM PURCHASE
            WHERE Invoice_Number = '{invoice}'""")
    specific_info = cursor.fetchall()
    heading = ['Product_ID' ,'Product_Name' ,'Product_Brand' ,'Product_Size' ,
            'Product_Category' ,'Quantity_Purchased' ,'Product_tot_cost']
    table = sg.Table(headings=heading,values = specific_info)
    layout = [[sg.Text(f'INVOICE NUMBER: {invoice}')],[sg.Text(f'DATE OF PURCHASE: {date}')],
    [table]]
    prod_win = sg.Window(title = 'More Information', layout=layout)
    while True:
        event,value = prod_win.read()
        print(event,value)
        if event is None:
            break
    
    
def daily_profit():
    """This function plots daily profit"""
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
def monthly():
    """This function plots monthly sale"""
    cursor.execute("""select DATE_FORMAT(purchase_date ,'%M %Y'), sum(quantity_purchased)
        from purchase
        group by monthname(purchase_date) ORDER BY PURCHASE_DATE;""")
    monthly_data = cursor.fetchall()
    month = [monthly_data[i][0] for i in range(len(monthly_data))]
    sale = [monthly_data[i][1] for i in range(len(monthly_data))]
    #print(monthly_data)
    plt.bar(month,sale)
    plt.show()
def categ_chart():
    """This function plots the categorical popularity chart"""
    cursor.execute("""select sum(quantity_purchased), product_category from purchase
        group by product_category;""")
    cat_data = cursor.fetchall()
    #print(cat_data)
    sale_data = [cat_data[i][0] for i in range(len(cat_data))]
    label = [cat_data[i][1] for i in range(len(cat_data))]
    print(sale_data,label)
    plt.pie(sale_data,labels = label,shadow=True, autopct = '%1.1f%%',
        wedgeprops={'edgecolor':'black'})
    plt.show()


def brand_item():
    """This function plots brand popularity graph"""
    cursor.execute("""select sum(quantity_purchased), product_brand from purchase
        group by Product_brand;""")
    sold_data = cursor.fetchall()
    no_item = [sold_data[i][0] for i in  range(len(sold_data))] #y-axis
    brand_name = [sold_data[i][1] for i in range(len(sold_data))] #x-axis
    plt.barh(brand_name,no_item)
    plt.tight_layout()
    plt.show()

if __name__=='__main__':
    main()
mycon.commit()
