import PySimpleGUI as sg
import mysql.connector as sqltor
from mysql.connector.locales.eng import client_error
from datetime import date
import employee_func as ef

file=open('settings.txt')
data=file.readlines()
file.close()
for i in range(len(data)):
    data[i]=data[i][:-1]
mycon = sqltor.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])

cursor = mycon.cursor()

# Set the PysimpleGUI theme and font
main_font_title=("Times New Roman", "12")
main_font_normal=("Times New Roman", "11")

def Main(email):
    def cart(cartData1):
        global price,data
        nonlocal dataIFEmpty
        heading1 = ['Product ID', 'Product Name', 'Brand', 'Size', 'Category', 'Quantity', 'Price']
        table=sg.Table(cartData1, headings=heading1,key='-TABLE2-',justification='center',enable_events=True, font=main_font_normal)
        priceMsg = sg.Text('{:.2f}'.format(price), font=main_font_normal)
        buyButton = sg.Button('Buy', font=main_font_normal)
        removeButton = sg.Button('Remove',key='RM', font=main_font_normal)
        clearButton = sg.Button('Clear',key='CLR', font=main_font_normal)
        goBackButton = sg.Button('Go Back', font=main_font_normal)
        layout1 = [[sg.Text('YOUR CART', font=main_font_normal)],
                  [table],
                  [sg.Text('Total Amount = ', font=main_font_normal), priceMsg],
                  [buyButton, goBackButton, clearButton, removeButton]]
        window1 = sg.Window('Your Cart', layout1, finalize=True, font=main_font_normal)
        remove_from_cart=None
        while True:
            event1, values1 = window1.read()
            if event1 in (None, 'Go Back'):
                break

            elif event1=='CLR':
                cartData1=[]
                cartDict.clear()
                table.update(cartData1)
                price = 0.0
                priceMsg.update('{}'.format(price))
                cursor.execute('SELECT ID,Name,Brand,Size,Category, Quantity,Selling_Price FROM PRODUCTS')
                data = list(cursor.fetchall())
                dataIFEmpty = list(data)
                sg.popup_timed('The cart has been cleared!', font=main_font_normal)
                window1.close()

            elif event1=='-TABLE2-' and values1['-TABLE2-']!=[]:
                remove_from_cart=values1['-TABLE2-'][0]

            elif event1=='RM' and remove_from_cart!=None and len(cartData1)>remove_from_cart:
                dat = cartData1[remove_from_cart]
                dataForNow = data if data else dataIFEmpty
                for i in dataForNow:
                    if i[0]==dat[0]:
                        i[5]+=dat[5]
                        data = dataIFEmpty = list(dataForNow)
                        break
                else:
                    tempList = list(dat)
                    tempList[6] = round(dat[6]/dat[5], 2)
                    if data:
                        data.append(tempList)
                        data.sort()
                        dataIFEmpty = list(data)
                    else:
                        dataIFEmpty.append(tempList)
                        dataIFEmpty.sort()
                        data = list(dataIFEmpty)
                price-=float(dat[6])
                price = round(price,2)
                var = 0
                for i in cartDict:
                    if var==remove_from_cart:
                        cartDict.pop(i)
                        cartData1.pop(remove_from_cart)
                        break
                    var+=1
                table.update(cartData1)
                priceMsg.update('{:.2f}'.format(price))

                if len(cartData1)==0:
                    sg.popup_timed('The cart is empty!', font=main_font_normal)
                    window1.close()

            elif event1=='Buy':
                confirm = sg.popup_yes_no('Are you sure you want to buy these products?', font=main_font_normal)
                if confirm == 'Yes':
                    final_data = list(cartData1)
                    for i in final_data:
                        idNow = i[0]
                        cursor.execute(f'SELECT Cost_Price FROM PRODUCTS WHERE ID = {idNow}')
                        priceNow = cursor.fetchone()[0]
                        profit = round(float(i[6]-priceNow*i[5]), 2)
                        i.append(profit)

                    for i in cartData1:
                        id1 = i[0]
                        cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %id1)
                        quantity = cursor.fetchall()
                        quantity = quantity[0][4]-i[5]
                        if quantity>1:
                            cursor.execute(f'UPDATE Products SET Quantity = {quantity} WHERE ID = {id1}')
                        else: 
                            cursor.execute(f'DELETE FROM Products WHERE ID = {id1}')
                    
                    """INVOICE NUMBER GENERATION"""
                    today = date.today()
                    pur_date = today.strftime("%Y-%m-%d") #Changing format to YYYY-MM-DD (i.e 2021-10-31)
                    cursor.execute(f"SELECT COUNT(DISTINCT  Invoice_Number) FROM PURCHASE WHERE Purchase_Date = '{pur_date}'")
                    result = cursor.fetchone() #Basically returns number of entries in purchase table
                    today = pur_date.replace('-','') #changing 2021-10-31 to 20211031
                    c = str(result[0]+1).zfill(6)
                    inv_num = today+'-'+c#format is %d%m%Y-N where N is cardinality of purchase
                    query = """INSERT INTO PURCHASE
                    VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """

                    #modifying list final_data as per the format of purchase table in sql
                    for i in range(len(final_data)): 
                        final_data[i].insert(0,inv_num) #Inserted Invoice number in  index 0
                        final_data[i].insert(1,email) #Inserted cust email in index 1
                        final_data[i].insert(9,pur_date) #Inserted purchase date in last
                    cursor.executemany(query,final_data)
                    cursor.execute(f"SELECT Total_Price FROM CUSTOMERS WHERE Email_ID = '{email}'")
                    pri = cursor.fetchone()[0]
                    pri = int(pri)+price
                    cursor.execute(f"UPDATE CUSTOMERS SET Total_Price = {pri} WHERE Email_ID = '{email}'")


                    sg.popup_ok(f'Purchase Successful. Total Amount Spent = {price}', font=main_font_normal)
                    window1.close()

                    return event1
        window1.close()

    def filter_menu():
        cursor.execute('select distinct category from products')
        categories=[]
        for i in cursor.fetchall():
            categories.append(i[0])
        cursor.execute('select distinct brand from products')
        brands=[]
        for i in cursor.fetchall():
                brands.append(i[0])
        txt=sg.Text('Filter or sort the data..',size=(35,1), font=main_font_normal)
        layout=[[txt]]
        layout.append([sg.Text('Sort', font=main_font_normal)])
        layout.append([sg.Radio('Name',1,default=True,key='R1', font=main_font_normal)])
        layout.append([sg.Radio('High To Low',1,key='R2', font=main_font_normal)])
        layout.append([sg.Radio('Low To High',1,key='R3', font=main_font_normal)])
        layout.append([sg.Text('Categories')])
        for i in categories:
            elem=sg.Checkbox(i,default=True,key=i, font=main_font_normal)
            layout.append([elem])
        layout.append([sg.Text('Brands', font=main_font_normal)])
        layout.append([sg.Checkbox('All',key='BALL',enable_events=True, font=main_font_normal)])
        for i in brands:
            elem=sg.Checkbox(i,default=False,key=i, font=main_font_normal)
            layout.append([elem])
        layout2=[[sg.Column(layout,scrollable=True)]]
        layout2.append([sg.Btn('Apply Filters',key='AP', font=main_font_normal)])

        window2=sg.Window('Filters',layout2)
        rng=True
        filters_applied=False
        while rng:
            events,values=window2.read()
            if events==sg.WIN_CLOSED:
                rng=False
            if events=='BALL':
                if values['BALL']:
                    for i in brands:
                        window2[i].update(True)
                else:
                    for i in brands:
                        window2[i].update(False)
            elif events=='AP':
                brands_sel=[]
                cats_sel=[]
                sort_sel='R1'
                for i in values:
                    if i in categories and values[i]==True:
                        cats_sel.append(i)
                    elif i in brands and values[i]==True:
                        brands_sel.append(i)
                    elif i in ('R1','R2','R3') and values[i]==True:
                        sort_sel=i
                if (brands_sel and cats_sel) or (sort_sel in ('R1','R2', 'R3')):
                    if len(brands_sel)!=1:
                        brands_sel=tuple(brands_sel)
                    else:
                        brands_sel="('{}')".format(brands_sel[0])
                    if len(cats_sel)!=1:
                        cats_sel=tuple(cats_sel)
                    else:
                        cats_sel="('{}')".format(cats_sel[0])
                    if sort_sel=='R1':
                        sort_sel='Name'
                    elif sort_sel=='R2':
                        sort_sel='Selling_Price DESC'
                    else:
                        sort_sel='Selling_Price'
                    if sort_sel in ('Name', 'Selling_Price DESC', 'Selling_Price'):
                        if len(brands_sel)==0:
                            brands_sel = tuple(brands)
                        if len(cats_sel)==0:
                            cats_sel=tuple(categories)
                    cmd="""SELECT ID,Name,Brand,Size, Category,Quantity,Selling_Price 
                    FROM PRODUCTS
                    WHERE Brand in {brand} and category in {category}
                    ORDER BY {sort}
                    """.format(brand=brands_sel,category=cats_sel,sort=sort_sel)
                    cursor.execute(cmd)
                    data=cursor.fetchall()
                    for i in range(len(data)):
                        data[i] = list(data[i])
                    cartContents={}
                    for i in cartDict:
                        cartContents[i[0]]=cartDict[i][0]
                    product_data=[]
                    for i in data:
                        product_data.append(i[0])
                    for i in cartContents:
                        if i in product_data:
                            index=product_data.index(i)
                            new_quantity=int(data[index][5])-cartContents[i]
                            if new_quantity:
                                data[index][5]=new_quantity
                            else:
                                data.pop(index)

                    if data:
                        window2.close()
                        return data
                    else:
                        txt.update('No product matches the given filter options',text_color='red')
                        print('\a')
                else:
                    txt.update('No category or brand selected',text_color='red')
                    print('\a')
        window2.close()

    def ord_hist(mail):
        cursor.execute(f"""SELECT INVOICE_NUMBER, PURCHASE_DATE, SUM(PRODUCT_TOT_COST) FROM PURCHASE
        WHERE CUSTOMER_EMAIL = '{mail}'
        GROUP BY INVOICE_NUMBER ORDER BY PURCHASE_DATE DESC""")
        purchase_data = cursor.fetchall()
        heading = ['Invoice Number',  'Purchase date','Total Cost']
        if not purchase_data:
            sg.popup('NO DATA FOUND', font=main_font_normal)
        else:
            table = sg.Table(purchase_data,headings=heading,key='pur_table',enable_events=True, font=main_font_normal)
            layout = [
            [table],
            [sg.Button('Exit',key = 'Exit', font=main_font_normal),sg.Button('Show More',disabled = True,key='show_more', font=main_font_normal)]
            ]
            win = sg.Window(f'{mail}',layout)
            while True:
                event1,value = win.read()  #Extracting only event
                if event1  in ('Exit',None):
                    win.close()
                    break
                if event1 == 'pur_table' and value['pur_table'] != []:
                    win['show_more'].update(disabled=False)
                if event1 == 'show_more' and value['pur_table'] != []:
                    ind_select = value['pur_table'][0]
                    inv_num = purchase_data[ind_select][0]
                    date = purchase_data[ind_select][1]
                    ef.more_details(inv_num,date)

    
    global price, cartData, cartDict, data
    heading = ['Product ID', 'Product Name', 'Brand', 'Size', 'Category', 'Quantity', 'Price']
    msg = sg.Text('',size=(20,0), font=main_font_normal)
    inp=sg.Input(key='-IN-', enable_events = True, font=main_font_normal,readonly=True, disabled_readonly_background_color='Gray',disabled_readonly_text_color='Black')
    spin=sg.Spin(1,initial_value=1,disabled=True, key = 'Spin', enable_events=True, font=main_font_normal)
    table=sg.Table(data, headings = heading, justification = 'centre', key = '-TABLE1-',enable_events=True, font=main_font_normal)
    atcButton = sg.Button('Add to Cart', disabled = True, font=main_font_normal)
    gtcButton = sg.Button('Go to Cart', disabled = True, font=main_font_normal)
    search=sg.Input(key='SB',enable_events=True, font=main_font_normal)
    filterBtn = sg.Btn('Filters',key='FL', font=main_font_normal)
    ord_button = sg.Button('Order History',key = 'order_history', font=main_font_normal)
    cursor.execute(f"SELECT Name FROM CUSTOMERS WHERE Email_ID = '{email}'")
    name = cursor.fetchone()
    layout = [[sg.Text(f'Hello, {name[0]}', font=main_font_title)],
              [sg.Text('Search', font=main_font_normal),search, filterBtn,ord_button],
              [table],
              [sg.Text('Product ID:', font=main_font_normal), msg,sg.Text(size=(20, 1), key='-OUTPUT-', font=main_font_normal)],
              [inp],
              [sg.Text('Quantity', font=main_font_normal),spin],
              [atcButton, gtcButton, sg.Button('Exit', font=main_font_normal)]]

    window = sg.Window('Products', layout, finalize = True)

    if len(cartDict) != 0:
        gtcButton.update(disabled=False)
    prod=None
    flag = False
    flag2 = False
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break

        elif event == 'order_history':
            ord_hist(email)

        elif event=='SB':
            inp.update('')
            cmd='''SELECT ID,Name,Brand,Size,Category,Quantity,Selling_Price 
            FROM PRODUCTS
            WHERE NAME LIKE \'{name}%\''''
            cmd=cmd.format(name=values['SB'])
            cursor.execute(cmd)
            dataIFEmpty = list(data)
            data=cursor.fetchall()
            for i in range(len(data)):
                data[i] = list(data[i])
            cartContents={}
            for i in cartDict:
                cartContents[i[0]]=cartDict[i][0]
            product_data=[]
            for i in data:
                product_data.append(i[0])
            for i in cartContents:
                if i in product_data:
                    index=product_data.index(i)
                    new_quantity=int(data[index][5])-cartContents[i]
                    if new_quantity:
                        data[index][5]=new_quantity
                    else:
                        data.pop(index)
            table.update(data)

        elif values['-TABLE1-']==[] and values['-IN-']=='' and event!='FL':
            atcButton.update(disabled = True)

        elif event=='-TABLE1-' and values['-TABLE1-'] != []:
            spin.update(1)
            idSelected = values['-TABLE1-'][0]
            prod=str(data[idSelected][0])
            inp.update(prod)
            quantity1 = data[idSelected][5]
            spin.update(values=tuple(range(1,quantity1+1)),disabled=False)
            atcButton.update(disabled = False)
            flag = True

        elif event=='-IN-' and values['-IN-']!='':
            spin.update(1)
            flag = False
            if values['-IN-'].isdigit():
                idSelected = int(values['-IN-'])
                for i in range(len(data)):
                    if data[i][0]==idSelected:
                        idSelected = i
                        flag = True
                        break
            if flag:
                quantity1 = data[idSelected][5]
                atcButton.update(disabled = False)
                spin.update(values=tuple(range(1, quantity1+1)), disabled=False)
            else:
                atcButton.update(disabled = True)
                spin.update(disabled = True)

        elif event=='FL':
            window.Disable()
            filtered_data=filter_menu()
            window.Enable()
            window.Hide()
            window.UnHide()
            if filtered_data:
                data=filtered_data
                table.update(data)
            search.update('')

        elif event =='Add to Cart' and flag:
            for i in range(len(data)):
                data[i] = list(data[i])
            #Declared the variable for my convenience and ease of understanding
            prod_ID_selected = int(values['-IN-'])
            cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %(prod_ID_selected))
            proData = cursor.fetchall()
            temp = (proData[0][0], proData[0][1], proData[0][2], proData[0][3], proData[0][7], proData[0][6])
            cartData.append(temp)
            q = str(values['Spin'])
            chk1 = q.isdigit()==False
            chk2 = '.' in q
            chk3 = int(q)>proData[0][4]
            chk4 = int(q)<=0
            chk5 = temp in cartDict
            chk6 = chk5 and (proData[0][4]-cartDict[temp][0]-int(q)<0)
            if  chk1 or chk2 or chk3 or chk4 or chk6:
                msg.update('Invalid Quantity Entered')
            else:
                q = int(q)
                if temp not in cartDict:
                    cartDict[temp] = [q, temp[5]*q]
                else:
                    cartDict[temp][0] += q
                    cartDict[temp][1] += temp[5]*q
                price+=float(temp[5]*q)
                price = round(price, 2)
                #This part of the code is responsible for updating the table as we add items to cart
                quantity = proData[0][4]
                for i in range(len(data)):
                    prod_searched = list(data[i])
                    prod_searched.pop(5)
                    if prod_searched[0] == prod_ID_selected:
                        data[i][5] = quantity-cartDict[tuple(prod_searched)][0]
                msg.update('Added to Cart')
                window['-IN-'].update('') #Clears the Input Window after we Add items to Cart
                table.update(data)
                spin.update(1,disabled = True)
                temp_table = []
                for i in range(len(data)):
                    if data[i][5] != 0:  #data[i][4] is the quantity
                        temp_table.append(data[i])
                table.update(temp_table)
                data = list(temp_table)
                spin.update(disabled = True)
                atcButton.update(disabled = True)
        if len(cartDict)==0:
            gtcButton.update(disabled=True)
        else:
            gtcButton.update(disabled=False)

        if event == 'Go to Cart' and len(cartDict)!=0:
            cartDataFinal = []
            for i in cartDict:
                cartDataFinal.append(list(i)[:5]+cartDict[i])
            flag2 = True
            window.close()
            break

    if flag2:
        action = cart(cartDataFinal)
        msg.update('')
        if action=='Buy':
            sg.popup_timed('Thank you for shopping with us', font=main_font_normal)
            window.close()
        else:
            if not data:
                data = dataIFEmpty
            Main(email)

    mycon.commit()

price = 0
cartData = []
cartDict = {}
cursor.execute('SELECT ID,Name,Brand,Size,Category,Quantity,Selling_Price FROM PRODUCTS')
data = cursor.fetchall()
if __name__=='__main__':
    Main('gauravchanda@gmail.com')
    mycon.commit()