import requests

payload = {
  "Warehouse_block": "A",
  "packages": [
    {
      "Warehouse_block": "A",
      "Mode_of_Shipment": "Flight",
      "Product_importance": "high",
      "Weight_in_gms": 1500,
      "Cost_of_the_Product": 250,
      "Discount_offered": 10
    },
    {
      "Warehouse_block": "A",
      "Mode_of_Shipment": "Road",
      "Product_importance": "low",
      "Weight_in_gms": 5000,
      "Cost_of_the_Product": 50,
      "Discount_offered": 0
    },
    {
      "Warehouse_block": "A",
      "Mode_of_Shipment": "Ship",
      "Product_importance": "medium",
      "Weight_in_gms": 2000,
      "Cost_of_the_Product": 100,
      "Discount_offered": 5
    }
  ]
}

try:
    response = requests.post("http://127.0.0.1:8000/optimize-route", json=payload)
    print("STATUS:", response.status_code)
    
    # Print nice compact JSON
    import json
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("FAILED TO CONNECT OR PARSE:", e)
