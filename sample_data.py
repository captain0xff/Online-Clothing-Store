import mysql.connector as sql

def generate_customer():
	file=open('settings.txt')
	data=file.readlines()
	file.close()
	for i in range(len(data)):
	    data[i]=data[i][:-1]
	mycon = sql.connect(host=data[0], user=data[1], passwd=data[2],database=data[3])
	cursor=mycon.cursor()
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

def generate_purchase():
	pass


if __name__ == '__main__':
	generate_customer()
	generate_purchase()