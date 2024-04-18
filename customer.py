import sqlite3
import yaml
import random
from hashlib import sha1
import ispositive # To check if user is done placing the order
from my_parser import Parser
import priority
import re
from flask import session
from map import Maps

'''
TODO:
>> Customer Annoyance Level and Customer Support implementation
>> Update the database with all the values [ done ]
>> Get user priority in a static variable [ done ]
>> Customer priority implementation [ done ]
>> Order Menu display with keeping Note of current category [ done ]
>> Time taken implementation [ done ]
>> Bill display [ done ]
'''

class Customer:
	def __init__(self):
		self.name = '' #
		self.priority = 'medium'
		self.curr_input = ''
		self.order_worth = 0 #
		self.referral_bonus_check = None
		self.referral_code = None
		self.phoneNo = '' #
		self.address = '' #
		self.drop_location = '' #
		self.curr_order_count = 0 #
		self.orders = [] #
		self.order_count = 0
		self.r_bill = 0 #
		self.givenDiscount = False #
		self.messages = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\welcome.yml"),Loader=yaml.Loader)
		self.last = '' #
		self.newUser = False
		self.flag = False # becomes True when it is time to store the order
		self.conn = sqlite3.connect('./customers.db')
		self.c = self.conn.cursor()
		self.no_of_orders = 1
		# Initialize an empty list for orders in the session
		if 'orders' not in session:
			session['orders'] = []

	def user_input(self, userInput, command_line=False):
		if command_line:
			if userInput is None:
				userInput = input(">> ")
			self.curr_input = userInput
			self.remove_punct()
			self.lower_case()
		else:
            # Handle the case when called from a web context (Flask)
			if userInput is not None:
				self.curr_input = userInput
				# self.remove_punct()
				# self.lower_case()
				return self.generate_order(userInput)
				
# def welcome_greeting(self,name):
	def welcome_greeting(self):
		welc_resp = self.messages['greet']
		# print(random.choice(welc_resp))
		return random.choice(welc_resp)
# return random.choice(welc_resp) +name
	
	def get_menu(self):
		menu_resp = self.messages['menu']
		# print(random.choice(welc_resp))
		return random.choice(menu_resp)
	
	def place_order_message(self):
		odr_msg = self.messages['conversations']
		return random.choice(odr_msg)
	
	def order_confirmed(self):
		placed = self.messages['order-placed']
		return random.choice(placed)
	
	def top_food(self):
		tf = self.messages['top-food']
		return tf

	def best_combos(self):
		bc = self.messages['best-combos']
		return bc

	def get_help(self):
		h = self.messages['help']
		return random.choice(h)

	def hello(self):
		x = self.messages['hello']
		return random.choice(x)

	def address_message(self):
		place = self.messages['address']
		return random.choice(place)

	def feed_back(self):
		fb = self.messages['feed-back']
		return random.choice(fb)
	
	def cancel_order(self):
		od = self.messages['cancel']
		return random.choice(od)
	
	def generate_order(self,input_str):
		# Clear the orders list at the start of each request
		# session['orders'] = []

		keywords = ["paneer tikka pizza", "veggie pizza", "margherita pizza", "egg pizza", "bbq chicken pizza", "tandoori chicken pizza", "keema pizza",
            "garlic bread", "choco cake", "burger", "pasta", "french fries",
            "coke", "fanta", "bisleri", "lime soda", "juice"]
		
		order = []

    	# Convert input string to lowercase for case-insensitive matching
		input_str_lower = input_str.lower()
		for keyword in keywords:
        	# Check if the keyword is present in the input string
				if keyword in input_str_lower:
					# Extract quantity using a simple regex pattern
					quantity_match = re.search(r'\b\d+\b', input_str_lower)
					quantity = int(quantity_match.group()) if quantity_match else 1
					# print(keyword,quantity)
					# Append the keyword and quantity to the order list
					order.append({keyword: quantity})
					session['orders'].append({keyword: quantity})
					# Remove the matched keyword and quantity from the input string
					input_str_lower = input_str_lower.replace(keyword, '', 1)
					input_str_lower = re.sub(r'\b\d+\b', '', input_str_lower, 1)
					
		self.orders.extend(order)
		return session['orders']
	
	# Example usage:
		# input_str = "I want 5 pizza capri, 2 choco cake, 3 pasta, 3 lime soda and 2 juice."
		# output_order = generate_order(input_str)
		# print(output_order)
	def get_delivery_time(self,destination):
		m = Maps()
		origin = 'Jntu, Hyderabad, India'
		result = m.estimate_time(origin,destination)
		return result

	def generate_bill(self, orders):
		prices = {
			'paneer tikka pizza': 500,
			'veggie pizza': 320,
			'margherita pizza': 350,
			'egg pizza': 450,
			'bbq chicken pizza': 620,
			'tandoori chicken pizza': 650,
			'keema pizza': 700,
			'garlic bread': 200,
			'choco cake': 100,
			'burger pizza': 150,
			'pasta': 140,
			'french fries': 70,
			'coke': 40,
			'fanta': 40,
			'bisleri': 20,
			'lime soda': 50,
			'juice': 40
		}

		total_bill = 0
		bill_items = []

		for order_item in orders:
			for food, quantity in order_item.items():
				if food in prices:
					item_cost = prices[food] * quantity
					total_bill += item_cost
					bill_items.append(f"{quantity} {food}(s) - Rs. {item_cost}")

		if total_bill < 300:
			bill_msg = "Sorry, delivery cannot be made for orders less than Rs. 300. <br>Please add more items to your cart.<br>what whould you like to have ?"
			return bill_msg
		else:
			bill_items.append(f"Total Bill: Rs. {total_bill}")
			return bill_items

if __name__ == '__main__':
	o = Customer()
	# str = "I want 3 pizza capri, 4 pasta and 6 juice"
	# m = o.generate_order(str)
	# print(m)
	# p = o.generate_bill(m)
	# print(p)
	# # # str2 = "I also want 2 choco cake"
	# n = o.get_menu()
	# # p = o.generate_order(str2)
	# # n = o.send_orders()
	# print(n)
	# print(m)
	# m= o.order_confirmed()
	# n= o.place_order_message()
	# o.getPrice()
	# o.bill_statement()
	# print(p)
	# # print(n)
	# print(n)
	# p = Parser()
	# o.execution_order()