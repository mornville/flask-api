from flask import Flask, request
from flask.json import jsonify
from flask_restful import Resource, Api, reqparse, abort
import constants

app = Flask(__name__)
api = Api(app)

class Order(Resource):
    def status_code(self, status_code=422, message="Unprocessable Entity"):
        return {"status_code": status_code, "message":message}

    def calculate(self, response):
        return {"total":000}

    def validate_input(self, data):
        order_items = data['order_items']
        for order in order_items:
            try:
                if len(order["name"])<=0 or len(order["name"])>constants.MAX_NAME_LENGTH:
                    return self.status_code(message="Incorrect Name")
                if int(order["quantity"]) <= 0  or int(order["quantity"])>=constants.MAX_QUANT:
                    return self.status_code(message="Quantity not in permissable Range")
                if int(order["price"])<=0 or int(order["price"])>=constants.MAX_PRICE:
                    return self.status_code(message="Price not in permissable range")
            except Exception as e:
                return self.status_code(status_code=500,message="Intenal Server Error -> " + str(e))

        distance = data["distance"]
        if distance<constants.DISTANCE_RANGE[0] or distance>constants.DISTANCE_RANGE[1]:
            return self.status_code(message="Distance not in permissable range")

        if "offer" in data:
            if data["offer"]["offer_val"]<0:
                return self.status_code(message="Incorrect offer value")

        return   self.calculate(data)

    def post(self):
        try:
            req = request.get_json()
            print(req)
            return self.validate_input(req)       
        except Exception as e:
            return {"status_code":500, "message":str(e)}

api.add_resource(Order, '/')

if __name__=="__main__":
    app.run(debug=True)