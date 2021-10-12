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
	# print('test', flush=True)
	s = json.dumps(cook.prepare_oder(order_list.pop()))
	requests.post('http://localhost:5050/distribution', json=s)

	return s


if __name__ == '__main__':
	kitchen.run(host='localhost', port=5000)
