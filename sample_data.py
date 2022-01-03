from datetime import date as dt
import random as rm
import mysql.connector as sql

file=open('settings.txt')
data=file.readlines()
file.close()
for i in range(len(data)):
    data[i]=data[i][:-1]
mycon = sql.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])
cursor=mycon.cursor()

def generate_customer():
	file=open('name.txt')
	data=file.readlines()
	file.close()
	customer_dict={}
	for i in data:
		name=i[:-1]
		phone_number=9876575438
		email_id=i[:-1].replace(' ','')+'@gmail.com'
		password=i[:-1].replace(' ','$')
		price=0.0
		customer_dict[name]=(name,phone_number,email_id,password,price)
	for i in customer_dict:
		cmd="""insert into customers values
('{}','{}','{}','{}',{})""".format(customer_dict[i][0],customer_dict[i][1],customer_dict[i][2],customer_dict[i][3],customer_dict[i][4])
		cursor.execute(cmd)
		mycon.commit()

def generate_purchase(y):
	year=y
	month=1
	day=1
	current_date=str(dt.today())
	cmd="select invoice_number from purchase"
	purchases=[]
	cursor.execute(cmd)
	invoices=list(cursor.fetchall())
	cmd="select * from products"
	cursor.execute(cmd)
	products=cursor.fetchall()
	cmd="select email_id from customers"
	cursor.execute(cmd)
	customers=cursor.fetchall()
	customer_sale_dict={}
	invoice_num=0
	date,invoice_date,year,month,day=get_date(year,month,day)
	while date!=current_date:
		for i in range(rm.randint(1,50)):
			invoice_num+=1
			invoice_str=(7-(len(str(invoice_num))))*'0'+str(invoice_num)
			full_invoice=invoice_date+invoice_str
			customer_email=rm.choice(customers)[0]
			product_bought=rm.choice(products)
			quantity=rm.randint(1,30)
			total_price=quantity*product_bought[6]
			if customer_email in customer_sale_dict:
				customer_sale_dict[customer_email]+=total_price
			else:
				customer_sale_dict[customer_email]=total_price
			purchases.append((full_invoice,customer_email,product_bought[0],product_bought[1],product_bought[2],product_bought[3],product_bought[7],quantity,round(float(total_price),2),date))
		invoice_num=0
		day+=1
		date,invoice_date,year,month,day=get_date(year,month,day)
	purchase_str=str(purchases)[1:-1]
	cmd="insert into purchase values {}".format(purchase_str)
	cursor.execute(cmd)
	for i in customer_sale_dict:
		cmd="update customers set total_price={} where email_id='{}'".format(customer_sale_dict[i],i)
		cursor.execute(cmd)
	mycon.commit()
	print('Sample data added!!!')



def get_date(y,m,d):
	day_month={
	28:[2],
	30:[4,6,9,11],
	31:[1,3,5,7,8,10,12]
	}
	for i in day_month:
		if m in day_month[i]:
			if d>i:
				d=1
				m+=1
				break
	if m>12:
		m=1
		y+=1
	ys=str(y)
	ms=str(m)
	ds=str(d)
	if len(ms)==1:
		ms='0'+ms
	if len(ds)==1:
		ds='0'+ds
	return '{year}-{month}-{day}'.format(year=ys,month=ms,day=ds),ys+ms+ds,y,m,d


if __name__ == '__main__':
	generate_customer()
	generate_purchase()