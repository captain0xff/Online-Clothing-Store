'''Create the database if not created'''
import mysql.connector as sqltor
from mysql.connector.locales.eng import client_error
import sample_data

#establishing the connection
file=open('settings.txt')
data=file.readlines()
file.close()
for i in range(len(data)):
    data[i]=data[i][:-1]
mycon = sqltor.connect(host=data[0], user=data[1], passwd=data[2])
cursor = mycon.cursor()

cursor.execute("DROP database IF EXISTS denim_destination_db")
sql_create = "CREATE database denim_destination_db"
cursor.execute(sql_create)
cursor.execute("USE denim_destination_db")
print("Database Created Succesfully....")
print("Creating tables now....")
sql_products = """create table PRODUCTS(
    ID INT NOT NULL PRIMARY KEY,
    Name VARCHAR(50),
    Brand VARCHAR(50),
    Size VARCHAR(4) CHECK(Size = 'S' OR Size = 'M' OR SIZE = 'L' OR SIZE = 'XL' OR SIZE = 'XXL' OR SIZE = 'XXXL' OR SIZE='NA'),
    Quantity INTEGER,
    Cost_Price DECIMAL(8,2),
    Selling_Price DECIMAL(8,2),
    Category VARCHAR(5) CHECK(Category = 'Kids' OR Category = 'Men' OR Category = 'Women' ))"""


cursor.execute(sql_products)
print("Relation product created successfully....")

sql_employees = """CREATE TABLE EMPLOYEES(
    ID int primary key,
    Name VARCHAR(50),
    Username VARCHAR(25),
    Password VARCHAR(90) CHECK(LENGTH(Password) > 7))"""

cursor.execute(sql_employees)
print("Relation employees created successfully....")

sql_customer = """create table CUSTOMERS(
    Name varchar(50),
    Phone_Number varchar(10) check(length(phone_number)=10),
    Email_ID varchar(200) primary key,
    Password varchar(200),
    Total_Price decimal(10,2))"""

cursor.execute(sql_customer)
print("Relation customer created successfully....")

sql_purchase = """create table PURCHASE(
    Invoice_Number varchar(15) not null,
    Customer_Email varchar(200),
    Product_ID INT REFERENCES PRODUCTS(ID),
    Product_Name VARCHAR(50),
    Product_Brand VARCHAR(50),
    Product_Size VARCHAR(4),
    Product_Category VARCHAR(5),
    Quantity_Purchased INTEGER,
    Product_tot_cost decimal(8,2),
    Purchase_Date date,
    Purchase_profit decimal(8,2),
    foreign key(Customer_Email) references CUSTOMERS(Email_ID))"""

"""INVOICE-NUMBER   EMAIL-ID   PRODUCT-ID     NAME   BRAND    SIZE   QUANTITY    CATEGORY    COST    PURCHASE-DATE 
"""
cursor.execute(sql_purchase)
print("Relation purchase created successfully....")

cursor.execute("""INSERT INTO EMPLOYEES
VALUES(1,'Pratyush Prashob', 'pratyushprashob27', 'arandompassword'),
(2,'Siddhartha Mondal', 'witty-30-06', 'iamimmortal'),
(3,'Sayantan Deb', 'captain1947', 'rajnikanth');""")
print("Data of Employees added...")

cursor.execute("""INSERT INTO CUSTOMERS
VALUES('Gaurav Chanda', 9674354867, 'gauravchanda@gmail.com', 'gauravchanda', 0),
('Arunansh Barai', 9833965591, 'arunanshbarai@gmail.com', 'phtkknhs', 0),
('Devarshi Ray', 9030657890, 'devarshiray@gmail.com', 'ilovemanga', 0);""")
sample_data.generate_customer()
print("Data of Customers added...")


cursor.execute('''insert into PRODUCTS
values('1','Jeans','Wrangler','XL','23','425.23','699.56','Men'),
('2','Shirt','Peter England','L','56','256.25','352.23','Women'),
('3','T Shirt','Lewis','S','15','230.50','299.99','Men'),
('4','Coat','Peter England','M','25','12000.00','17999.99','Men'),
('5','T Shirt','Peter England','S','43','230.56','325.99','Men'),
('6','Chinos','Buffalo','M','25','325.69','399.99','Men'),
('7','Jacket','Denim & Jeans','L','13','254.69','350.00','Men'),
('8','Jumper','Pepe Jeans','XL','25','789.69','850.90','Women'),
('9','Hat','Peter England','S','156','109.50','159.99','Kids'),
('10','Sherwani','Manyavar','XL','14','7890.40','13330.90','Men'),
('11','Lehenga','Manish Malhotra','XL','15','589.36','650.99','Women'),
('12','Kurti','Meow','XL','42','250.63','499.99','Women'),
('13','Salwar Kameez','Shristhi','XL','26','569.63','899.99','Women'),
('14','Lungi','Anmol','NA','20','250.00','350.00','Men'),
('15','Kurta','Anmol','NA','14','355.00','450.00','Men'),
('16','Jeans','Anmol','XL','16','750.99','799.99','Men'),
('17','Gamcha','Raju','NA','189','100.00','150.00','Men'),
('18','T Shirt','Raju','XXL','103','330.00','350.00','Men'),
('19','Baniyaan','Raju','L','34','150.00','200.00','Men'),
('20','Jumpsuit','Hopscoth','S','23','850.00','950.00','Kids'),
('21','Lahenga Choli','Fashion Dream','M','25','1050.00','1250.00','Women'),
('22','Hoodie','Hopscoth','S','13','2250.00','2400.00','Kids'),
('23','Sweatshirt','Fashion Dream','S','10','1350.00','1790.00','Kids'),
('24','Coat','Hopscoth','M','35','7300.00','7300.00','Kids'),
('25','Jacket','Fashion Dream','M','42','2250.00','2550.00','Kids'),
('26','Waistcoat','Hopscoth','S','58','1250.00','1350.00','Kids'),
('27','Joggers','Diamo','S','20','250.00','350.00','Kids'),
('28','Track Pants','Hopscoth','S','100','250.00','350.00','Kids'),
('29','Sweater','Diamo','M','12','250.00','350.00','Kids'),
('30','Knitwear','Anmol','M','6','250.00','350.00','Kids'),
('31','Mascot Costume','Diamo','M','11','250.00','350.00','Kids');
''')
print('Products added...')

mycon.commit()

sample_data.generate_purchase(2020)

mycon.close()
print('Successful!!!')