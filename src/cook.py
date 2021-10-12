'''
Get food-order for processing
Update prepared food to /distribution (dining hall POST endpoint)
Optional - use cooking aparatuses
'''
import json, time

# f = open('./data/cooks.json', 'r')
cooks = json.load(open('./data/cooks.json', 'r'))


def prepare_food(food_id):
	start = time.time()

	return cook_id, time.time()-start


# returns ready order /distribution json POST payload
def prepare_oder(order_id, order_body):
	order_body['order_id'] = order_id

	order_body['cooking_time'] = 0
	order_body['cooking_details'] = []
	for item in order_body['items']:
		cook_id, prep_time = prepare_food(item)
		order_body['cooking_details'].append(dict(food_id=item, cook_id=cook_id))
		order_body['cooking_time'] += prep_time
	return order_body


