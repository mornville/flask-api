# Flask-Api
- Contains a PUT API and a POST API for updating the delivery slab and giving order input to the server respectively.

## INSTALLATION
- `git clone https://github.com/mornville/flask-api.git`
- `cd flask-api`
- Make/Activate virtual environment
- `pip install -r requirements.txt`
-  `python api.py`
## USAGE
### POST Request for order total
- Send a POST request to `http://localhost:5000/` with a body:
````json
{
  "order_items": [
    {
      "name": "bread",
      "quantity": 2,
      "price": 2200
    },
    {
      "name": "butter",
      "quantity": 1,
      "price": 5900
    }
  ],
  "distance": 123,
  "offer": {
    "offer_type": "FLAT",
    "offer_val": 1000
  }
}
````
- Response:
````json
{
    "total": 14300
}
````
### PUT Api for updating Delivery Slab
- Request PUT with a body:
````json
 { 
        "delivery_cost": [[0,10, 50], [10, 20, 100], [20, 50, 50], [50, 100, 1000]]
 }
 ````
- Response
````json
{
    "status_code": 200,
    "message": "Updated Successfully"
}
````

## ASSUMPTIONS MADE
- Maximum Name length = 100
- Maximum item quantity = 50
- Maximum item price(paisa) = 1000000
- distance range(min, max) (metre) = (0, 500000)
- Initial Delivery Slab (lower, upper, cost) (lower and upper bound in Km) = [(0,10, 50), (10, 20, 100), (20, 50, 500), (50, DISTANCE_RANGE[1], 1000)]

## STATUS CODES USED
- `422: Unprocessable Entity`
- `500: Internal Server Error`
- `200: Update Success`
