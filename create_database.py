'''Create the database if not created'''

import mysql.connector as sqltor
#establishing the connection
psswd = input("Enter the password of ur db: ")
mycon = sqltor.connect(user='root', password=psswd, host='localhost')
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
    Size VARCHAR(4) CHECK(Size = 'S' OR Size = 'M' OR SIZE = 'L' OR SIZE = 'XL' OR SIZE = 'XXL' OR SIZE = 'XXXL'),
    Quantity INTEGER,
    Cost_Price DECIMAL(8,2),
    Selling_Price DECIMAL(8,2))"""


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
    Invoice_Number varchar(15) not null primary key,
    Purchase_Date date,
    Purchase_Amount decimal(8,2),
    Customer_Email varchar(200),
    foreign key(Customer_Email) references CUSTOMERS(EMAIL_ID))"""

cursor.execute(sql_purchase)
print("Relation purchase created successfully....")

cursor.execute("""INSERT INTO EMPLOYEES
VALUES(1,'Pratyush Prashob', 'pratyushprashob27', 'arandompassword'),
(2,'Siddhartha Mondal', 'witty-30-06', 'iamimmortal'),
(3,'Sayantan Deb', 'captain1947', 'rajnikanth');""")
print("Data of Employees added...")

cursor.execute("""INSERT INTO CUSTOMERS
VALUES('Gaurav Chanda', 1123978046, 'gauravchanda@gmail.com', 'gauravchanda', 10000),
('Arunansh Barai', 9833965591, 'arunanshbarai@gmail.com', 'phtkknhs', 9000),
('Devarshi Ray', 1110010993, 'devarshiray@gmail.com', 'ilovemanga', 100000);""")
print("Data of Customers added...")

cursor.execute('''insert into products(ID,Name,Brand,Size,Quantity,Cost_Price,Selling_Price) values
('1','Jeans','Wrangler','XL','23','425.23','699.56'),
('2','Shirt','Peter England','L','56','256.25','352.23'),
('3','T Shirt','Lewis','S','15','230.50','299.99'),
('4','Coat','Peter England','M','25','12000.00','17999.99'),
('5','T Shirt','Peter England','S','43','230.56','325.99'),
('6','Chinos','Buffalo','M','25','325.69','399.99'),
('7','Jacket','Denim & Jeans','L','13','254.69','350.00'),
('8','Jumper','Pepe Jeans','XL','25','789.69','850.90'),
('9','Hat','Peter England','S','156','109.50','159.99'),
('10','Sherwani','Manyavar','XL','15','7890.40','13330.90'),
('11','Lehenga','Manish Malhotra','XL','15','589.36','650.99'),
('12','Kurti','Meow','XL','42','250.63','499.99'),
('13','Salwar Kameez','Shristhi','XL','26','569.63','899.99')''')
print('Products added...')

mycon.commit()
mycon.close()
print('Successful!!!')
