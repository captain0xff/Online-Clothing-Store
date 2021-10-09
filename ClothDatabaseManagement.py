import PySimpleGUI as sg
import mysql.connector as sqltor
mycon = sqltor.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'clothes')
cursor = mycon.cursor()

sg.theme('DarkAmber')

heading = ['ProductID', 'ProductName', 'Price', 'Brand', 'Size']
cursor.execute('SELECT * FROM PRODUCTS')
data = cursor.fetchall()

layout = [[sg.Table(data, headings = heading, justification = 'left', key = '-TABLE-')],
          [sg.Text(' '),
           sg.Text(size=(50, 1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Buy'), sg.Button('Exit')]]

window = sg.Window('Employee', layout, margins=(100, 50))

price = 0
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        confirm = sg.popup_ok('Total Amount Paid = %.2f' %price)
        break
    if event == 'Buy':
        confirm = sg.popup_yes_no('Are you sure you want to buy this product?')
        if confirm=='Yes':
            for i in range(len(data)):
                if data[i][0] == int(values['-IN-']):
                    price += data[i][2]
                    upd = 'You just bought %s. Total Amount = %0.2f' %(data[i][1], price)
                    window['-OUTPUT-'].update(upd)
                    cursor.execute('DELETE FROM PRODUCTS WHERE PROID = %d' %data[i][0])
                    mycon.commit()
                    break
            else:
                window['-OUTPUT-'].update('Product Not Found')

    print(event, values)