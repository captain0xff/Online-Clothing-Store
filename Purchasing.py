import PySimpleGUI as sg
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'denim_destination_db')
cursor = mycon.cursor()


def purchaseMenu():
    def cart(cartData1, price1):
        sg.theme('DarkAmber')
        heading1 = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']
        layout1 = [[sg.Text('YOUR CART')],
                  [sg.Table(cartData1, headings=heading1, justification='left', key='-TABLE-')],
                  [sg.Text('Total Amount {}'.format(price1))],
                  [sg.Button('Buy'), sg.Button('Go Back')]]
        window1 = sg.Window('Your Cart', layout1, margins=(100, 50), finalize=True)
        while True:
            #print(cartData)
            event1, values1 = window1.read()
            if event1 in (None, 'Go Back'):
                break
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
                    sg.popup_ok('Purchase Successful. Total Amount Spent = {}'.format(price1))
                    break
        window1.close()
        return event

    sg.theme('DarkAmber')

    heading = ['Product ID', 'Product Name', 'Brand', 'Size', 'Quantity', 'Price']
    cursor.execute('SELECT ID,Name,Brand,Size,Quantity,Selling_Price FROM PRODUCTS')
    #Converted everything into list just to make things easier :)
    data = list(cursor.fetchall())
    for i in range(len(data)):
        data[i] = list(data[i])
    msg = sg.Text('                    ')
    layout = [[sg.Table(data, headings = heading, justification = 'centre', key = '-TABLE-')],
              [sg.Text('Enter the Product ID:'), msg,
               sg.Text(size=(50, 1), key='-OUTPUT-')],
              [sg.Input(key='-IN-')],
              [sg.Button('Add to Cart'), sg.Button('Exit'), sg.Button('Go to Cart')]]

    window = sg.Window('Products', layout, finalize = True)

    price = 0
    cartData = []
    cartDict = {}
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event =='Add to Cart':
            # Declared the variable for my convenience and ease of understanding
            prod_ID_selected = int(values['-IN-'])
            cursor.execute('SELECT * FROM PRODUCTS WHERE ID = %d' %(prod_ID_selected))
            proData = cursor.fetchall()
            temp = (proData[0][0], proData[0][1], proData[0][2], proData[0][3], proData[0][6])
            cartData.append(temp)
            price+=proData[0][5]
            i = temp
            if i in cartDict:
                cartDict[i][1] += i[4]
                cartDict[i][0] += 1
            else:
                cartDict[i] = [1, i[4]]
            print(cartDict)
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
            window['-TABLE-'].update(data)

        if event == 'Go to Cart':
            cartDataFinal = []
            for i in cartDict:
                cartDataFinal.append(list(i)[:4]+cartDict[i])
            action = cart(cartDataFinal, price)
            if action=='Buy':
                sg.popup_timed('Thank you for shopping with us')
                window.close()
                break
        print(event, values)
    mycon.commit()

purchaseMenu()


