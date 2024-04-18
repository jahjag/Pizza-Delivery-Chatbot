import string
import yaml
import random
import ispositive
from tabulate import tabulate
import trending
import nltk
# nltk.download()
from nltk.corpus import stopwords
from sys import exit

"""
TODO: 
>> connect "change.py" for change menu ( add menu changes to change.py )
>> add "trending" food items using trending.py [ done ]
>> bring in botprofile.yml, food.yml, greetings.yml, humor.yml [ done ]
>> ADD menu universal [ done ]
>> ADD the place order parsing [ done ]
"""

class Parser:
	def __init__(self):
		self.curr_input = ""
		self.printCk = False
		self.universals = [
			"cancel",
			"top",
			"hot",
			"hungry",
			"help",
			"about",
			"change",
			"menu",
			"thirsty",
			"quit",
		]
		self.curse_words = None
		self.annoyance = 5
		self.menu = list()
		self.orders = list()
		self.stopwords = stopwords.words("english")
		self.generic_dict = dict()
		self.messages = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\welcome.yml"),Loader=yaml.Loader)
		self.load_curse()
		self.generic_responses()
		self.menu_items()

	def load_curse(self):
		with open(r"C:\Users\shoeb\Downloads\My major project\datasets\curse_words.txt") as file:
			self.curse_words = file.readlines()
		index = 0
		for curse in self.curse_words:
			curse = self.lower_case(inp=True, sent=curse)
			curse = self.remove_punct(inp=True, sent=curse)
			self.curse_words[index] = curse
			index += 1

	# def user_input(self, command_line=True):
	# 	if command_line == True:
	# 		self.curr_input = input(">> ")
	# 		self.remove_punct()
	# 		self.lower_case()
	# 	else:
	# 		pass
			
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
				self.remove_punct()
				self.lower_case()
				return self.level_one_parse()

	def remove_punct(self, sent="", inp=False):
		remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
		if inp == False:
			self.curr_input = self.curr_input.translate(remove_punct_dict)
		elif inp == True:
			return sent.translate(remove_punct_dict)

	def lower_case(self, sent="", inp=False):
		if inp == False:
			self.curr_input = self.curr_input.strip().lower()
		elif inp == True:
			return sent.lower().strip()

	def universal_parse(self, words):
		"""
		"universals" are : 'cancel', 'top', 'hot', 'hungry', 'help', 'about', '@change', '@menu', 'thirsty'
		"words" are: list of user entered words
		"""
		key = [word for word in words if (word in self.universals)]
		key = key[0]
		if key == "cancel":
			cancel_resp = self.messages["cancel"]
			self.printCk = True
			return random.choice(cancel_resp)

		elif key == "menu":
			pizzas = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\pizzas.yml"),Loader=yaml.Loader)
			sides = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\sides.yml"),Loader=yaml.Loader)
			beves = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\beverages.yml"),Loader=yaml.Loader)
			data_pizzas= [(k, pizzas[k]["ingredients"], pizzas[k]["price"]) for k in pizzas]
			# self.printCk = True
			# print(
			# 	tabulate(
			# 		data, headers=("Pizza", "ingredients", "Price"), tablefmt="grid"
			# 	)
			# )
			data_sides= [
				(side, sides[side]["ingredients"], sides[side]["price"])
				for side in sides
			]
			# print(
			# 	tabulate(
			# 		data, headers=("Sides", "ingredients", "Price"), tablefmt="grid"
			# 	)
			# )
			data_beves= [(beve, beves[beve]["price"]) for beve in beves]
			# print(tabulate(data, headers=("Beverages", "Price"), tablefmt="grid"))
			result = {
                "type": "menu",
                "data_pizzas": tabulate(data_pizzas, headers=("Pizza", "Ingredients", "Price"), tablefmt="html"),
                "data_sides": tabulate(data_sides, headers=("Sides", "Ingredients", "Price"), tablefmt="html"),
                "data_beves": tabulate(data_beves, headers=("Beverages", "Price"), tablefmt="html")
            }

			# Add line gaps in HTML tables
			for key in result.keys():
				if key.startswith("data_"):
					result[key] = result[key].replace('<table>', '<table cellspacing="10">')

			return result

		elif key == "pizza" or key == "pizzas":
			# Trending food method will come here
			top_food = trending.read_csv_file(r"C:\Users\shoeb\Downloads\My major project\datasets\menu.csv")
			food_resp = self.messages["top-food"]
			self.printCk = True
			return (
				random.choice(food_resp)
				+ top_food[0][0]
				+ ", "
				+ top_food[0][1]
				+ ", "
				+ top_food[1][0]
			)

		elif key == "beverages" or key == "drinks" or key == "refreshing" or key == "refreshments" or key == "beverage" or key == "drink":
			# Trending beverages will come here
			top_beve = trending.read_csv_file(r"C:\Users\shoeb\Downloads\My major project\datasets\menu.csv")
			beve_resp = self.messages["top-beve"]
			self.printCk = True
			return (
				random.choice(beve_resp)
				+ top_beve[2][0]
				+ ", "
				+ top_beve[2][1]
				+ ", "
				+ top_beve[2][2]
			)

		elif key == "help" or key == "about":
			help_resp = self.messages["help"]
			self.annoyance -= 2
			self.printCk = True
			return random.choice(help_resp)

		elif key == "quit":
			quit_resp = self.messages["quit"]
			self.printCk = True
			# print(random.choice(quit_resp))
			return random.choice(quit_resp)
			exit(0)

	def generic_responses(self):
		greet = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\greetings.yml"),Loader=yaml.Loader)["conversations"]
		humor = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\humor.yml"),Loader=yaml.Loader)["conversations"]
		food = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\food.yml"),Loader=yaml.Loader)["conversations"]
		botprofile = yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\botprofile.yml"),Loader=yaml.Loader)["conversations"]
		self.generic_resp_store(greet)
		self.generic_resp_store(humor)
		self.generic_resp_store(food)
		self.generic_resp_store(botprofile)

	def generic_resp_store(self, conversations):
		for conv in conversations:
			conv[0] = self.remove_punct(inp=True, sent=conv[0])
			conv[0] = self.lower_case(inp=True, sent=conv[0])
			if conv[0] in self.generic_dict:
				self.generic_dict[conv[0]].append(conv[1])
			else:
				self.generic_dict[conv[0]] = [conv[1]]

	def curse_parse(self):
		curse_resp = self.messages["curse"]
		self.annoyance -= 4
		self.printCk = True
		return random.choice(curse_resp)

	def level_one_parse(self):
		words = self.curr_input.split()
		if self.curr_input in self.generic_dict:
			self.printCk = True
			print(random.choice((self.generic_dict[self.curr_input])))
			return random.choice((self.generic_dict[self.curr_input]))
		elif any(word in words for word in self.curse_words):
			self.printCk = True
			print(self.curse_parse())
			return self.curse_parse()
		elif any(word in words for word in self.universals):
			val = self.universal_parse(words)
			if val != None:
				self.printCk = True
				print(val)
				return val
		else:
			pos_check = ispositive.is_positive(self.curr_input)
			if pos_check == False:
				help_resp = self.messages["help"]
				self.printCk = True
				# print(random.choice(help_resp))
				return random.choice(help_resp)
			elif pos_check == True:
				self.order_parse(words)

	def menu_items(self):
		pizza = [food for food in list(yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\pizzas.yml"),Loader=yaml.Loader).keys())]
		sides = [food for food in list(yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\sides.yml"),Loader=yaml.Loader).keys())]
		beve = [
			food for food in list(yaml.load(open(r"C:\Users\shoeb\Downloads\My major project\datasets\beverages.yml"),Loader=yaml.Loader).keys())
		]
		self.menu = pizza + sides + beve
		index = 0
		for food in self.menu:
			self.menu[index] = self.remove_punct(inp=True, sent=food)
			self.menu[index] = self.lower_case(sent=self.menu[index], inp=True)
			index += 1

	def order_parse(self, words):
		"""
		words : list containing words which contains the order
		This is the level two parser
		"""
		order_placed_resp = self.messages["order-placed"]
		restricted_words = ["for", "have", "give"]
		for word in words:
			if word in self.stopwords and word not in restricted_words:
				words.remove(word)

		order_words = ["want", "get", "for", "order", "have", "give"]
		order_no_w = {
			"one": 1,
			"two": 2,
			"three": 3,
			"four": 4,
			"five": 5,
			"six": 6,
			"seven": 7,
			"eight": 8,
			"nine": 9,
		}
		order_no = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

		notPlaced = True

		if len(words) == 1 or len(words) == 2 or len(words) == 3:
			if len(words) == 2:
				if words[0] + " " + words[1] in self.menu:
					self.printCk = True
					print(
						random.choice(order_placed_resp)
						+ " : "
						+ words[0]
						+ " "
						+ words[1]
					)
					self.orders.append([words[0] + " " + words[1], 1])
					notPlaced = False
				elif ((words[0] in order_no) or (words[0] in order_no_w)) and words[1] in self.menu:
					self.printCk = True
					print(random.choice(order_placed_resp) + " : " + words[1])
					if words[0] in order_no:
						self.orders.append([words[1], words[0]])
						notPlaced = False
					else:
						self.orders.append([words[1], order_no_w[words[0]]])
						notPlaced = False

			elif len(words) == 1:
				if words[0] in self.menu:
					self.printCk = True
					print(random.choice(order_placed_resp) + " : " + words[0])
					self.orders.append([words[0], 1])
					notPlaced = False

			elif len(words) == 3:
				if words[0] in order_no or words[0] in order_no_w:
					if words[1] + " " + words[2] in self.menu:
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[1]
							+ " "
							+ words[2]
						)
						if words[0] in order_no:
							self.orders.append([words[1] + " " + words[2], words[0]])
							notPlaced = False
						else:
							self.orders.append(
								[words[1] + " " + words[2], order_no_w[words[0]]]
							)
							notPlaced = False
		elif notPlaced == True:
			for word in order_words:
				if word in words:
					if words[words.index(word) + 1] in self.menu:
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 1]
						)
						self.orders.append([words[words.index(word) + 1], 1])

					elif (
						words[words.index(word) + 2] in self.menu
						and words[words.index(word) + 1] in order_no_w
					):
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 2]
						)
						self.orders.append(
							[
								words[words.index(word) + 2],
								order_no_w[words[words.index(word) + 1]],
							]
						)

					elif (
						words[words.index(word) + 2] in self.menu
						and words[words.index(word) + 1] in order_no
					):
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 2]
						)
						self.orders.append(
							[words[words.index(word) + 2], words[words.index(word) + 1]]
						)

					elif (
						words[words.index(word) + 1]
						+ " "
						+ words[words.index(word) + 2]
						in self.menu
					):
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 1]
							+ " "
							+ words[words.index(word) + 2]
						)
						self.orders.append(
							[
								words[words.index(word) + 1]
								+ " "
								+ words[words.index(word) + 2],
								1,
							]
						)

					elif (
						words[words.index(word) + 2]
						+ " "
						+ words[words.index(word) + 3]
						in self.menu
						and words[words.index(word) + 1] in order_no_w
					):
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 2]
							+ " "
							+ words[words.index(word) + 3]
						)
						self.orders.append(
							[
								words[words.index(word) + 2]
								+ " "
								+ words[words.index(word) + 3],
								order_no_w[words[words.index(word) + 1]],
							]
						)

					elif (
						words[words.index(word) + 2]
						+ " "
						+ words[words.index(word) + 3]
						in self.menu
						and words[words.index(word) + 1] in order_no
					):
						self.printCk = True
						print(
							random.choice(order_placed_resp)
							+ " : "
							+ words[words.index(word) + 2]
							+ " "
							+ words[words.index(word) + 3]
						)
						self.orders.append(
							[
								words[words.index(word) + 2]
								+ " "
								+ words[words.index(word) + 3],
								words[words.index(word) + 1],
							]
						)
		if self.printCk == False:
			print("Sorry didn't get you there!, To get help type 'help'!")

if __name__ == "__main__":
	o = Parser()
	# o.user_input('menu')
	# # o.level_one_parse()
	# o.user_input('help')
	# # o.level_one_parse()
	# o.user_input('cancel')
	o.user_input('what are the best pizzas?')
	o.level_one_parse()