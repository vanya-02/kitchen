'''
Get food-order for processing
Update prepared food to /distribution (dining hall POST endpoint)
Optional - use cooking aparatuses
'''
# import json
# import time

# # f = open('./data/cooks.json', 'r')

# TIME_UNIT = 0.1  # of a second


# def prepare_food(food_id):
# 	start = time.time()
# 	# write code to optimize cooks selection
# 	cook = cook_list[3]  # bunica
# 	food = food_list[food_id - 1]
# 	time.sleep(food['preparation-time'] * TIME_UNIT)

# 	return cook['rank'], (time.time() - start) * 1/TIME_UNIT


# # returns ready order /distribution json POST payload
# def prepare_oder(order_body):
# 	# order_body['order_id'] = order_id
# 	order_body['cooking_time'] = 0
# 	order_body['cooking_details'] = []
# 	for item in order_body['items']:
# 		cook_id, prep_time = prepare_food(item)
# 		order_body['cooking_details'].append(dict(food_id=item, cook_id=cook_id))
# 		order_body['cooking_time'] += prep_time

# 	return order_body




import json
from concurrent import futures
import threading
import time


cook_list = json.load(open('./data/cooks.json', 'r'))
food_list = json.load(open('./data/foods.json', 'r'))

class Cook:
	def __init__(self, cook_id, rank, proficiency, name, catch_phrase):
		self.id = cook_id
		self.rank = rank
		self.proficiency = proficiency
		self.name = name
		self.catch_phrase = catch_phrase



class Kitchen:
	def __init__(self, cooks, menu) -> None:
		# constructs a Cook object for each cook from cooks.json
		for i in range(len(cooks)):
			cook = cooks[i]
			cooks[i] = Cook(
				cook_id=i,
				rank=cook['rank'],
				proficiency=cook['proficiency'],
				name=cook['name'],
				catch_phrase=cook['catch-phrase']
			)
		
		# nr of 1-3 proeficiencies
		# with current config => [1, 2, 6]
		self.cooks = cooks
		self.complexity_totals = [0, 0, 0] 
		for cook in self.cooks:

			self.complexity_totals[cook.rank-1] += cook.proficiency
		self.n_cooks = sum(self.complexity_totals)

		self.menu = menu
		self.order_list = []
		self.TIME_UNIT = 0.1


	def cook_item(self, ttime, complexity):
		ttime = ttime * self.TIME_UNIT
		while True:
			if complexity == 1 and sum(self.complexity_totals) > 0:
				for i in range(3):
					if self.complexity_totals[i] > 0:
						self.complexity_totals[i] -=1
						time.sleep(ttime)
						self.complexity_totals[i] +=1
						break
				break
			elif complexity == 2 and sum(self.complexity_totals[1:]) > 0:
				for i in range(1, 3):
					if self.complexity_totals[i] > 0:
						self.complexity_totals[i] -=1
						time.sleep(ttime)
						self.complexity_totals[i] +=1
						break
				break
			elif complexity == 3 and self.complexity_totals[2] > 0:
				self.complexity_totals[2] -=1
				time.sleep(ttime)
				self.complexity_totals[2] +=1
				break

	def prepare_order(self, order_body):
		pool = []
		cooking_time = time.time()
		with futures.ThreadPoolExecutor(max_workers=self.n_cooks) as executor:
			for food_id in order_body['items']:
				for menu_item in self.menu:
					if menu_item['id'] == food_id:
						x = executor.submit(self.cook_item, menu_item['preparation-time'], menu_item['complexity'])
						pool.append(x)
						break
			# waits for the order to be ready
			for i in pool:
				i.result()
		cooking_time = time.time() - cooking_time
		order_body['cooking_time'] = cooking_time

		return order_body



	def process_order(self, order_body) -> None:
		order_body['cooking_time'] = time.time()
		self.order_list.append(order_body)

		new_thread = threading.Thread(target='prepare_order', args=order_body)
		self.order_list.append(new_thread)
		new_thread.start()


kitchen_obj = Kitchen(cook_list, food_list)

