import cook
import json
import requests
from flask import Flask, request

kitchen = Flask(__name__)

order_list = []


# 1. Add new order to order list
# 2. Send order to chefs/preparation
# 3. Register receive time and prepared order time
@kitchen.route('/order', methods=['POST'])
def order():
	# Parse and add incoming POST orders to order_list
	data = request.json
	order_list.append(data)
	print('Received order:', flush=False)
	print(data, flush=False)
	r_order = json.dumps(cook.prepare_oder(order_list.pop()))
	print('Sending prepared ready order back:')
	print(r_order, flush=False)
	requests.post('http://localhost:5050/distribution', json=r_order)

	return r_order


# import time
# @kitchen.route('/test', methods=['POST'])
# def test():
# 	print('post', flush=False)
# 	time.sleep(10)
# 	return 'return'


if __name__ == '__main__':
	kitchen.run(host='localhost', port=5000, threaded=True)
