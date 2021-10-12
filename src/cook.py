'''
Get food-order for processing
Update prepared food to /distribution (dining hall POST endpoint)
Optional - use cooking aparatuses
'''
import json
import time

# f = open('./data/cooks.json', 'r')
cook_list = json.load(open('./data/cooks.json', 'r'))
food_list = json.load(open('./data/foods.json', 'r'))
TIME_UNIT = 0.1  # of a second


def prepare_food(food_id):
	start = time.time()
	# write code to optimize cooks selection
	cook = cook_list[3]  # bunica
	food = food_list[food_id - 1]
	time.sleep(food['preparation-time'] * TIME_UNIT)

	return cook['rank'], (time.time() - start) * 1/TIME_UNIT


# returns ready order /distribution json POST payload
def prepare_oder(order_body):
	# order_body['order_id'] = order_id
	order_body['cooking_time'] = 0
	order_body['cooking_details'] = []
	for item in order_body['items']:
		cook_id, prep_time = prepare_food(item)
		order_body['cooking_details'].append(dict(food_id=item, cook_id=cook_id))
		order_body['cooking_time'] += prep_time

	return order_body
