import requests
import itertools

modes = ["Flight", "Ship", "Road"]
priorities = ["low", "medium", "high"]
weights = [500, 2000, 4500, 6000]
costs = [50, 150, 250]

results = []

for m, p, w, c in itertools.product(modes, priorities, weights, costs):
    payload = {
        "Warehouse_block": "A",
        "packages": [{
            "Warehouse_block": "A",
            "Mode_of_Shipment": m,
            "Product_importance": p,
            "Weight_in_gms": w,
            "Cost_of_the_Product": c
        }]
    }
    try:
        resp = requests.post("http://127.0.0.1:8000/optimize-route", json=payload).json()
        prob = resp['optimal_route'][0]['delay_probability']
        results.append((prob, m, p, w, c))
    except Exception as e:
        pass

results.sort(key=lambda x: x[0])

# Get Min, Median, and Max
if results:
    min_res = results[0]
    mid_res = results[len(results)//2]
    max_res = results[-1]
    
    print(f"LOW DELAY (ON TIME): Mode={min_res[1]}, Priority={min_res[2]}, Weight={min_res[3]}g, Cost=${min_res[4]} -> Probability: {min_res[0]*100:.1f}%")
    print(f"MEDIUM DELAY: Mode={mid_res[1]}, Priority={mid_res[2]}, Weight={mid_res[3]}g, Cost=${mid_res[4]} -> Probability: {mid_res[0]*100:.1f}%")
    print(f"HIGH DELAY: Mode={max_res[1]}, Priority={max_res[2]}, Weight={max_res[3]}g, Cost=${max_res[4]} -> Probability: {max_res[0]*100:.1f}%")
