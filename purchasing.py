import PySimpleGUI as sg
import mysql.connector as sqltor
import settings as st
from datetime import date
import csv
import os
current = os.getcwd()
mycon = sqltor.connect(host=st.host,user=st.user,passwd=st.password,database=st.database)
cursor = mycon.cursor()


def Main(email):
    def cart(cartData1):
        global price,data
        sg.theme('DarkAmber')
        heading1 = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']
        table=sg.Table(cartData1, headings=heading1,key='-TABLE2-',enable_events=True)
        priceMsg = sg.Text('{}'.format(price))
        buyButton = sg.Button('Buy')
        layout1 = [[sg.Text('YOUR CART')],
                  [table],
                  [sg.Text('Total Amount = '), priceMsg],
                  [buyButton, sg.Button('Go Back'),sg.Button('Clear',key='CLR'),sg.Button('Remove',key='RM')]]
        window1 = sg.Window('Your Cart', layout1, margins=(100, 50), finalize=True)
        remove_from_cart=None
        while True:
            #print(cartData)
            event1, values1 = window1.read()
            #print(event1)
            if event1 in (None, 'Go Back'):
                break
            if event1=='CLR':
                cartData1=[]
                cartDict.clear()
                table.update(cartData1)
                price = 0.0
                priceMsg.update('{}'.format(price))
                cursor.execute('SELECT ID,Name,Brand,Size,Quantity,Selling_Price FROM PRODUCTS')
                data = list(cursor.fetchall())
                sg.popup_timed('The cart has been cleared!')
                window1.close()

            if event1=='-TABLE2-':
                remove_from_cart=values1['-TABLE2-'][0]
            print(remove_from_cart)
            if event1=='RM' and remove_from_cart!=None and len(cartData1)>remove_from_cart:
                print(cartData1)
                dat = cartData1[remove_from_cart]
                quan=dat[4]
                for i in data:
                    if i[0]==dat[0]:
                        i[4]+=dat[4]
                price-=float(dat[5])
                var = 0
                for i in cartDict:
                    if var==remove_from_cart:
                        cartDict.pop(i)
                        cartData1.pop(remove_from_cart)
                        break
                    var+=1
                table.update(cartData1)
                priceMsg.update('{}'.format(price))

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
                        quantity = quantity[0][4]-i[4]
                        if quantity>1:
                            cursor.execute('UPDATE Products SET Quantity = {} WHERE ID = {}'.format(quantity, id1))
                        else: 
                            cursor.execute('DELETE FROM Products WHERE ID = {}'.format(id1))
                    print(cartData1)
                    
                    """INVOICE NUMBER GENERATION"""
                    today = date.today()
                    pur_date = today.strftime("%Y-%m-%d") #Changing format to YYYY-MM-DD (i.e 2021-10-31)
                    cursor.execute(f"SELECT COUNT(*) FROM PURCHASE WHERE Purchase_Date = '{pur_date}'")
                    result = cursor.fetchone() #Basically returns number of entries in purchase table
                    today = pur_date.replace('-','') #changing 2021-10-31 to 20211031
                    c = str(result[0]+1).zfill(6)
                    inv_num = today+'-'+c#format is %d%m%Y-N where N is cardinality of purchase
                    #print(inv_num)
                    query = f"""INSERT INTO PURCHASE VALUES('{inv_num}','{pur_date}',{price},'{email}')"""
                    #print(query)
                    cursor.execute(query)
                    cursor.execute(f"SELECT Total_Price FROM CUSTOMERS WHERE Email_ID = '{email}'")
                    pri = cursor.fetchone()[0]
                    pri = int(pri)+price
                    cursor.execute(f"UPDATE CUSTOMERS SET Total_Price = {pri} WHERE Email_ID = '{email}'")
                    sg.popup_ok('Purchase Successful. Total Amount Spent = {}'.format(price))
                    window1.close()
                    """----Beginning of CSV part----"""
                    def export(cd,mail):
                        fname = f"Customer data//{mail}.csv"
                        with open(fname,'a',newline='') as fh:
                            write = csv.writer(fh)
                            for i in range(len(cd)):
                                cd[i].append(pur_date)
                                print(pur_date)
                            cd = [['Prod_ID','Name','Brand','Size','Quantity','Cost','Pur Date']]+cd
                            write.writerows(cd)
                    try:
                        os.mkdir("Customer data")
                        export(cartData1,email)
                    except FileExistsError:
                        export(cartData1,email)
                    """----End of CSV part----"""
                    return event1
        window1.close()

    global price
    global cartData
    global cartDict
    global data
    sg.theme('DarkAmber')
    heading = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']

    print(data)
    for i in range(len(data)):
        data[i] = list(data[i])
    msg = sg.Text('',size=(20,0))
    inp=sg.Input(key='-IN-')
    spin=sg.Spin(1,initial_value=1,disabled=True, key = 'Spin', enable_events=True)
    layout = [[sg.Table(data, headings = heading, justification = 'centre', key = '-TABLE1-',enable_events=True)],
              [sg.Text('Product ID:'), msg,sg.Text(size=(20, 1), key='-OUTPUT-')],
              [inp],
              [sg.Text('Quantity'),spin],
              [sg.Button('Add to Cart'), sg.Button('Exit'), sg.Button('Go to Cart')]]

    window = sg.Window('Products', layout, finalize = True)

    prod=None
    flag = False
    while True:
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break
        if event=='-TABLE1-':
            idSelected = values['-TABLE1-'][0]
            prod=str(data[idSelected][0])
            inp.update(prod)
            spin.update(values=tuple(range(1,data[idSelected][4]+1)),disabled=False)

        if event =='Add to Cart':
            # Declared the variable for my convenience and ease of understanding
            prod_ID_selected = int(values['-IN-'])
            cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %(prod_ID_selected))
            proData = cursor.fetchall()
            #print(proData)
            temp = (proData[0][0], proData[0][1], proData[0][2], proData[0][3], proData[0][6])
            cartData.append(temp)
            q = str(values['Spin'])
            if  (q.isdigit()==False) or ('.' in q) or (int(q)>proData[0][4]) or (int(q)<=0) or ((temp in cartDict) and (proData[0][4]-cartDict[temp][0]-int(q)<0)):
                msg.update('Invalid Quantity')
            else:
                q = int(q)
                if temp not in cartDict:
                    cartDict[temp] = [q, temp[4]*q]
                else:
                    cartDict[temp][0] += q
                    cartDict[temp][1] += temp[4]*q
                price+=float(temp[4]*q)
                #print(cartDict)
                # This part of the code is responsible for updating the table as we add items to cart
                quantity = proData[0][4]
                for i in range(len(data)):
                    prod_searched = list(data[i])
                    prod_searched.pop(4)
                    if prod_searched[0] == prod_ID_selected:
                        data[i][4] = quantity-cartDict[tuple(prod_searched)][0]
                        #print(data)
                msg.update('Added to Cart')
                window['-IN-'].update('') #Clears the Input Window after we Add items to Cart
                window['-TABLE1-'].update(data)
                spin.update(1,disabled = True)
        if event == 'Go to Cart' and len(cartDict)==0:
            msg.update('Empty Cart...')

        if event == 'Go to Cart' and len(cartDict)!=0:
            cartDataFinal = []
            #print(cartDict)
            for i in cartDict:
                cartDataFinal.append(list(i)[:4]+cartDict[i])
            flag = True
            window.close()
            break
    if flag:
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
cursor.execute('SELECT ID,Name,Brand,Size,Quantity,Selling_Price FROM PRODUCTS')
data = list(cursor.fetchall())
if __name__=='__main__':
    Main(ID)

#Main('gauravchanda@gmail.com')