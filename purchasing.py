import PySimpleGUI as sg
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root', passwd = 'sayantan@sql', database = 'denim_destination_db')
cursor = mycon.cursor()


def Main():
    def cart(cartData1):
        nonlocal price
        sg.theme('DarkAmber')
        heading1 = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']
        table=sg.Table(cartData1, headings=heading1,key='-TABLE2-',enable_events=True)
        priceMsg = sg.Text('{}'.format(price))
        buyButton = sg.Button('Buy')
        layout1 = [[sg.Text('YOUR CART')],
                  [table],
                  [sg.Text('Total Amount = '), priceMsg],
                  [buyButton, sg.Button('Go Back',key='GB'),sg.Button('Clear',key='CLR'),sg.Button('Remove',key='RM')]]
        window1 = sg.Window('Your Cart', layout1, margins=(100, 50), finalize=True)
        remove_from_cart=None
        while True:
            #print(cartData)
            event1, values1 = window1.read()
            if event1 in (None, 'Go Back'):
                break
            if event1=='GB':
                break
            if event1=='CLR':
                cartData1=[]
                cartDict.clear()
                table.update(cartData1)
                price = 0.0
                priceMsg.update('{}'.format(price))
                buyButton.update(disabled = True)
            if event1=='-TABLE2-':
                remove_from_cart=values1['-TABLE2-'][0]
                print(remove_from_cart)
            print(remove_from_cart)
            if event1=='RM' and remove_from_cart!=None and len(cartData1)>remove_from_cart:
                dat = cartData1[remove_from_cart]
                price-=dat[5]
                var = 0
                for i in cartDict:
                    if var==remove_from_cart:
                        cartDict.pop(i)
                        cartData1.pop(remove_from_cart)
                        break
                    var+=1
                table.update(cartData1)
                priceMsg.update('{}'.format(price))


            if event1=='Buy':
                confirm = sg.popup_yes_no('Are you sure you want to buy these products?')
                if confirm == 'Yes':
                    for i in cartData1:
                        id1 = i[0]
                        cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %id1)
                        quantity = cursor.fetchall()
                        print(id1, quantity)
                        quantity = quantity[0][4]-i[4]
                        if quantity>1:
                            cursor.execute('UPDATE Products SET Quantity = {} WHERE ID = {}'.format(quantity, id1))
                        else: 
                            cursor.execute('DELETE FROM Products WHERE ID = {}'.format(id1))
                        mycon.commit()
                    sg.popup_ok('Purchase Successful. Total Amount Spent = {}'.format(price))
        window1.close()
        return event1



    sg.theme('DarkAmber')

    heading = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']
    cursor.execute('SELECT ID,Name,Brand,Size,Quantity,Selling_Price FROM PRODUCTS')
    #Converted everything into list just to make things easier :)
    data = list(cursor.fetchall())
    for i in range(len(data)):
        data[i] = list(data[i])
    msg = sg.Text('',size=(20,0))
    inp=sg.Input(key='-IN-')
    layout = [[sg.Table(data, headings = heading, justification = 'centre', key = '-TABLE1-',enable_events=True)],
              [sg.Text('Product ID:'), msg,
               sg.Text(size=(20, 1), key='-OUTPUT-')],
              [inp],
              [sg.Button('Add to Cart'), sg.Button('Exit'), sg.Button('Go to Cart')]]

    window = sg.Window('Products', layout, finalize = True)

    price = 0
    cartData = []
    cartDict = {}
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event=='-TABLE1-':
            idSelected = values['-TABLE1-'][0]
            prod=str(data[idSelected][0])
            inp.update(prod)
        if event =='Add to Cart':
            # Declared the variable for my convenience and ease of understanding
            prod_ID_selected = int(values['-IN-'])
            cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %(prod_ID_selected))
            proData = cursor.fetchall()
            #print(proData)
            temp = (proData[0][0], proData[0][1], proData[0][2], proData[0][3], proData[0][6])
            cartData.append(temp)
            price+=temp[4]
            if temp in cartDict:
                cartDict[temp][1] += temp[4]
                cartDict[temp][0] += 1
            else:
                cartDict[temp] = [1, temp[4]]
            #print(cartDict)
            # This part of the code is responsible for updating the table as we add items to cart
            quantity = proData[0][4]
            for i in range(len(data)):
                prod_searched = list(data[i])
                prod_searched.pop(4)
                if prod_searched[0] == prod_ID_selected:
                    data[i][4] = quantity-cartDict[tuple(prod_searched)][0]
                    print(data)
            msg.update('Added to Cart')
            window['-IN-'].update('') #Clears the Input Window after we Add items to Cart
            window['-TABLE1-'].update(data)

        if event == 'Go to Cart' and len(cartDict)==0:
            msg.update('Empty Cart...')

        if event == 'Go to Cart' and len(cartDict)!=0:
            cartDataFinal = []
            print(cartDict)
            for i in cartDict:
                cartDataFinal.append(list(i)[:4]+cartDict[i])
            action = cart(cartDataFinal)
            msg.update('')
            print(action)
            if action=='Buy':
                sg.popup_timed('Thank you for shopping with us')
                window.close()
                break

        print(event, values)
    mycon.commit()

if __name__=='__main__':
    Main()
