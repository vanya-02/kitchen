import cook
import json
import requests
from flask import Flask, request

kitchen = Flask(__name__)


from cook import kitchen_obj



# 1. Add new order to order list
# 2. Send order to chefs/preparation
# 3. Register receive time and prepared order time
@kitchen.route('/order', methods=['POST'])
def order():
	data = request.json
	print('\nReceived order:', flush=False)
	print(data,'\n', flush=False)
	# r_order = json.dumps(cook.prepare_oder(order_list.pop()))
	print('Sending prepared ready order back:')
	# print(r_order, flush=False)
	# requests.post('http://localhost:5050/distribution', json=r_order)
	_ = kitchen_obj.prepare_order(data)
	print(_, flush=False)
	return _


# import time
# @kitchen.route('/test', methods=['POST'])
# def test():
# 	print('post', flush=False)
# 	time.sleep(10)
# 	return 'return'


if __name__ == '__main__':
	kitchen.run(host='localhost', port=5000, threaded=True)
