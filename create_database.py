'''Create the database if not created'''

import mysql.connector as sqltor
#establishing the connection
psswd = input("Enter the password of ur db: ")
conn = sqltor.connect(user='root', password=psswd, host='localhost')
cursor = conn.cursor()
cursor.execute("DROP database IF EXISTS denim_destination_db")
sql_create = "CREATE database denim_destination_db"
cursor.execute(sql_create)
cursor.execute("USE denim_destination_db")
print("Database Created Succesfully....")
print("Creating tables now....")
sql_products = """create table products(
    ID INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(50),
    BRAND VARCHAR(50),
    SIZE VARCHAR(4) CHECK(SIZE = 'S' OR SIZE = 'M' OR SIZE = 'L' OR SIZE = 'XL' OR SIZE = 'XXL' OR SIZE = 'XXXL'),
    QUANTITY INTEGER,
    COST_PRICE DECIMAL(8,2),
    SELLING_PRICE DECIMAL(8,2))"""

cursor.execute(sql_products)
print("Relation product created successfully....")

sql_employees = """CREATE TABLE EMPLOYEES(
    ID integer NOT NULL PRIMARY KEY,
    NAME VARCHAR(50),
    USERNAME VARCHAR(10),
    PASSWORD VARCHAR(90) CHECK(LENGTH(PASSWORD) > 7))"""

cursor.execute(sql_employees)
print("Relation employees created successfully....")

sql_customer = """create table customer(
    id integer not null primary key,
    name varchar(50),
    phone_number integer,
    email_id varchar(200),
    total_price decimal(10,2))"""

cursor.execute(sql_customer)
print("Relation customer created successfully....")

sql_purchase = """create table purchase(
    Invoice_number varchar(15) not null primary key,
    product_id int,
    purchase_date date,
    purchase_amount decimal(8,2),
    customer_ID integer,
    foreign key(product_ID) references products(id),
    foreign key(customer_ID) references customer(id))"""

cursor.execute(sql_purchase)
print("Relation purchase created successfully....")