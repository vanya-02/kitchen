import cook
import json

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

	return json.dumps(order_list)


if __name__ == '__main__':
	kitchen.run()
