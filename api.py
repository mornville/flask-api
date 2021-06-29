from flask import Flask, request
from flask_restful import Resource, Api
import constants
from intervaltree import Interval, IntervalTree

app = Flask(__name__)
api = Api(app)
## Initial delivery slab 
DISTANCE_INTERVAL = IntervalTree(
    Interval(start*1000, end*1000, data=data) for start, end, data in constants.DELIVERY_COST
)

class Order(Resource):
    """ Helper function to return response messages """
    def status_code(self, status_code=422, message="Unprocessable Entity"):
        return {"status_code": status_code, "message":message}
    
    """ Function to calculate total from input response """
    def calculate(self, response):
        total = 0
        try:
            for order in response["order_items"]:
                total += order["price"]*order["quantity"]
            ## Getting delivery cost according to the distance in paisa
            delivery_cost = sorted(DISTANCE_INTERVAL[response["distance"]])[0].data * 100
            discount = 0
            if "offer" in response:
                if response["offer"]["offer_type"].lower() == "delivery":
                    discount = delivery_cost
                elif response["offer"]["offer_type"].lower() == "flat":
                    discount = min(total, response["offer"]["offer_val"])
            total += delivery_cost - discount
        except Exception as e:
            return self.status_code(status_code=500, message="Internal Server Error")
        return {"total":total}

    """ Helper function for Input Response Validation """
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

    """ Function for POST request to the server """
    def post(self):
        try:
            ## Taking input from body of response (raw/json)
            req = request.get_json()
            print(req)
            return self.validate_input(req)       
        except Exception as e:
            return {"status_code":500, "message":str(e)}

    """ PUT API for configuring delivery slab """
    def put(self):
        """
        { 
        "delivery_cost": [[0,10, 50], [10, 20, 100], [20, 50, 50], [50, 100, 1000]]
        }
        """
        try:
            req = request.get_json()
            distance_intervals = req["delivery_cost"]
            ## Updating the Delivery slab according to the put request
            for interval in distance_intervals:
                DISTANCE_INTERVAL.remove_overlap(interval[0], interval[1])
                ## Converting delivery slab distances to metre as distance is taken in metres in POST
                DISTANCE_INTERVAL[interval[0]*1000:interval[1]*1000] = interval[2]
        except Exception as e:
            return self.status_code(status_code=500, message="Incorrect input, Error-> " + str(e))

        return self.status_code(status_code=200, message="Updated Successfully")


api.add_resource(Order, '/')

if __name__=="__main__":
    app.run(debug=True)