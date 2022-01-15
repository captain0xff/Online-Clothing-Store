import PySimpleGUI as sg
import mysql.connector as sqltor
from mysql.connector.locales.eng import client_error
from datetime import date

file=open('settings.txt')
data=file.readlines()
file.close()
for i in range(len(data)):
    data[i]=data[i][:-1]
mycon = sqltor.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])

cursor = mycon.cursor()


def Main(email):
    def cart(cartData1):
        global price,data
        sg.theme('DarkAmber')
        print(cartData1)
        heading1 = ['Product ID', 'Product Name', 'Brand', 'Size', 'Category', 'Quantity', 'Price']
        table=sg.Table(cartData1, headings=heading1,key='-TABLE2-',justification='center',enable_events=True)
        priceMsg = sg.Text('{:.2f}'.format(price))
        buyButton = sg.Button('Buy')
        layout1 = [[sg.Text('YOUR CART')],
                  [table],
                  [sg.Text('Total Amount = '), priceMsg],
                  [buyButton, sg.Button('Go Back'),sg.Button('Clear',key='CLR'),sg.Button('Remove',key='RM')]]
        window1 = sg.Window('Your Cart', layout1, finalize=True)
        remove_from_cart=None
        
        while True:
            event1, values1 = window1.read()
            print(event1,values1)
            if event1 in (None, 'Go Back'):
                break
            if event1=='CLR':
                cartData1=[]
                cartDict.clear()
                table.update(cartData1)
                price = 0.0
                priceMsg.update('{}'.format(price))
                cursor.execute('SELECT ID,Name,Brand,Size,Category, Quantity,Selling_Price FROM PRODUCTS')
                data = list(cursor.fetchall())
                sg.popup_timed('The cart has been cleared!')
                window1.close()

            if event1=='-TABLE2-' and values1['-TABLE2-']!=[]:
                remove_from_cart=values1['-TABLE2-'][0]
                print(49)
            print(remove_from_cart)
            if event1=='RM' and remove_from_cart!=None and len(cartData1)>remove_from_cart:
                print(cartData1)
                dat = cartData1[remove_from_cart]
                print(dat)
                for i in data:
                    if i[0]==dat[0]:
                        i[5]+=dat[5]
                        break
                else:
                    a = len(data)
                    for i in range(len(data)):
                        if data[i][0]>dat[0]:
                            a = i
                            break
                    tempList = list(dat)
                    print(tempList)
                    tempList[5] = round(dat[6]/dat[5], 2)
                    data.insert(a, tempList)
                    print(data)
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
                    sg.popup_timed('The cart is empty!')
                    window1.close()


            if event1=='Buy':
                confirm = sg.popup_yes_no('Are you sure you want to buy these products?')
                if confirm == 'Yes':
                    for i in cartData1:
                        id1 = i[0]
                        cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %id1)
                        quantity = cursor.fetchall()
                        #print(id1, quantity)
                        quantity = quantity[0][4]-i[5]
                        if quantity>1:
                            cursor.execute(f'UPDATE Products SET Quantity = {quantity} WHERE ID = {id1}')
                        else: 
                            cursor.execute(f'DELETE FROM Products WHERE ID = {id1}')
                    print(cartData1)
                    
                    """INVOICE NUMBER GENERATION"""
                    today = date.today()
                    pur_date = today.strftime("%Y-%m-%d") #Changing format to YYYY-MM-DD (i.e 2021-10-31)
                    cursor.execute(f"SELECT COUNT(DISTINCT  Invoice_Number) FROM PURCHASE WHERE Purchase_Date = '{pur_date}'")
                    result = cursor.fetchone() #Basically returns number of entries in purchase table
                    today = pur_date.replace('-','') #changing 2021-10-31 to 20211031
                    c = str(result[0]+1).zfill(6)
                    inv_num = today+'-'+c#format is %d%m%Y-N where N is cardinality of purchase
                    print(inv_num)
                    
                    #print(query)
                    query = """INSERT INTO PURCHASE
                    VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                    final_data = cartData1
                    print(final_data)
                    for i in final_data:
                        idNow = i[0]
                        cursor.execute(f'SELECT Cost_Price FROM PRODUCTS WHERE ID = {idNow}')
                        priceNow = cursor.fetchone()[0]
                        profit = round(float(i[6]-priceNow*i[5]), 2)
                        i.append(profit)
                    print(final_data)
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


                    sg.popup_ok(f'Purchase Successful. Total Amount Spent = {price}')
                    window1.close()

                    return event1
        window1.close()

    def filter_menu(data):
        cursor.execute('select distinct category from products')
        categories=[]
        for i in cursor.fetchall():
            categories.append(i[0])
        cursor.execute('select distinct brand from products')
        brands=[]
        for i in cursor.fetchall():
                brands.append(i[0])
        txt=sg.Text('Filter or sort the data..',size=(35,1))
        layout=[[txt]]
        layout.append([sg.Text('Sort')])
        layout.append([sg.Radio('Name',1,default=True,key='R1')])
        layout.append([sg.Radio('High To Low',1,key='R2')])
        layout.append([sg.Radio('Low To High',1,key='R3')])
        layout.append([sg.Text('Categories')])
        for i in categories:
            elem=sg.Checkbox(i,default=True,key=i)
            layout.append([elem])
        layout.append([sg.Text('Brands')])
        layout.append([sg.Checkbox('All',key='BALL',enable_events=True)])
        for i in brands:
            elem=sg.Checkbox(i,default=False,key=i)
            layout.append([elem])
        layout2=[[sg.Column(layout,scrollable=True)]]
        layout2.append([sg.Btn('Apply Filters',key='AP')])

        window2=sg.Window('Filters',layout2)
        rng=True
        filters_applied=False
        while rng:
            events,values=window2.read()
            print(events,values)
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
                        print(brands_sel, cats_sel)
                    cmd="""SELECT ID,Name,Brand,Size, Category,Quantity,Selling_Price 
                    FROM PRODUCTS
                    WHERE Brand in {brand} and category in {category}
                    ORDER BY {sort}
                    """.format(brand=brands_sel,category=cats_sel,sort=sort_sel)
                    print(cmd)
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
    global price, cartData, cartDict, data
    sg.theme('DarkAmber')
    heading = ['Product ID', 'Product Name', 'Brand', 'Size', 'Category', 'Quantity', 'Price']
    msg = sg.Text('',size=(20,0))
    inp=sg.Input(key='-IN-', enable_events = True)
    spin=sg.Spin(1,initial_value=1,disabled=True, key = 'Spin', enable_events=True)
    table=sg.Table(data, headings = heading, justification = 'centre', key = '-TABLE1-',enable_events=True)
    atcButton = sg.Button('Add to Cart', disabled = True)
    gtcButton = sg.Button('Go to Cart', disabled = True)
    search=sg.Input(key='SB',enable_events=True)
    filterBtn = sg.Btn('Filters',key='FL')
    layout = [[sg.Text('Search'),search, filterBtn],
              [table],
              [sg.Text('Product ID:'), msg,sg.Text(size=(20, 1), key='-OUTPUT-')],
              [inp],
              [sg.Text('Quantity'),spin],
              [atcButton, gtcButton, sg.Button('Exit')]]

    window = sg.Window('Products', layout, finalize = True)

    if len(cartDict) != 0:
        gtcButton.update(disabled=False)
        filterBtn.update(disabled = True)
    prod=None
    flag = False
    flag2 = False
    searchFlag = False
    while True:
        event, values = window.read()
        #print(event, values)
        print(cartDict)
        #print(data)
        if event in (None, 'Exit'):
            print('Line 261')
            break
        if event=='SB':
            new_data=[]
            """cmd='''SELECT ID,Name,Brand,Size,Quantity,Selling_Price 
                                                FROM PRODUCTS
                                                WHERE NAME LIKE \'{name}%\'
                                                '''
                                                cmd=cmd.format(name=values['SB'])
                                                cursor.execute(cmd)
                                                data=cursor.fetchall()"""
            for i in data:
                if values['SB'] in i[1]:
                    new_data.append(i)
            table.update(new_data)
            searchFlag = True
        if values['-TABLE1-']==[] and values['-IN-']=='':
            atcButton.update(disabled = True)

        if event=='-TABLE1-' and values['-TABLE1-'] != []:
            spin.update(1)
            if searchFlag:
                dataUsing = new_data
            else:
                dataUsing = data
            #print(dataUsing)
            idSelected = values['-TABLE1-'][0]
            print(idSelected)
            prod=str(dataUsing[idSelected][0])
            inp.update(prod)
            quantity1 = dataUsing[idSelected][5]
            spin.update(values=tuple(range(1,quantity1+1)),disabled=False)
            atcButton.update(disabled = False)
            flag = True

        if event=='-IN-' and values['-IN-']!='':
            #atcButton.update(disabled=True)
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

        if event=='FL':
            window.Disable()
            filtered_data=filter_menu(data)
            window.Enable()
            window.Hide()
            window.UnHide()
            if filtered_data:
                data=filtered_data
                table.update(data)
            search.update('')


        if event =='Add to Cart' and flag:
            #search.update('')
            #print('312')
            search.update('')
            searchFlag = False
            for i in range(len(data)):
                data[i] = list(data[i])
            # Declared the variable for my convenience and ease of understanding
            prod_ID_selected = int(values['-IN-'])
            cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %(prod_ID_selected))
            proData = cursor.fetchall()
            #print(proData)
            temp = (proData[0][0], proData[0][1], proData[0][2], proData[0][3], proData[0][7], proData[0][6])
            cartData.append(temp)
            q = str(values['Spin'])
            if  (q.isdigit()==False) or ('.' in q) or (int(q)>proData[0][4]) or (int(q)<=0) or ((temp in cartDict) and (proData[0][4]-cartDict[temp][0]-int(q)<0)):
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
                #print(cartDict)
                # This part of the code is responsible for updating the table as we add items to cart
                quantity = proData[0][4]
                #print(data)
                #print(cartDict)
                for i in range(len(data)):
                    prod_searched = list(data[i])
                    prod_searched.pop(5)
                    if prod_searched[0] == prod_ID_selected:
                        data[i][5] = quantity-cartDict[tuple(prod_searched)][0]
                        #print(data)
                msg.update('Added to Cart')
                window['-IN-'].update('') #Clears the Input Window after we Add items to Cart
                table.update(data)
                spin.update(1,disabled = True)
                temp_table = []
                for i in range(len(data)):
                    if data[i][5] != 0:  #data[i][4] is the quantity
                        temp_table.append(data[i])
                #print("Data",data)
                table.update(temp_table)
                data = list(temp_table)
                spin.update(disabled = True)
                atcButton.update(disabled = True)
                #print(358)
        if len(cartDict)==0:
            gtcButton.update(disabled=True)
            filterBtn.update(disabled = False)
        else:
            gtcButton.update(disabled=False)

        if event == 'Go to Cart' and len(cartDict)!=0:
            cartDataFinal = []
            #print(cartDict)
            for i in cartDict:
                cartDataFinal.append(list(i)[:5]+cartDict[i])
            flag2 = True
            window.close()
            break


    if flag2:
        action = cart(cartDataFinal)
        msg.update('')
            #print(action)
        if action=='Buy':
            sg.popup_timed('Thank you for shopping with us')
            window.close()
        else:
            Main(email)

    mycon.commit()
mycon.commit()

price = 0
cartData = []
cartDict = {}
cursor.execute('SELECT ID,Name,Brand,Size,Category,Quantity,Selling_Price FROM PRODUCTS')
data = cursor.fetchall()
if __name__=='__main__':
    Main('gauravchanda@gmail.com')