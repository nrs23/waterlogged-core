from functools import reduce
import requests

size_of_watering_can_in_liters = 5
liters_to_mm_per_square_meter = 1

url = "https://api.open-meteo.com/v1/forecast"
payload = {"latitude": 50.83,
           "longitude": -0.14,
           "daily": ["precipitation_sum", "et0_fao_evapotranspiration"],
           "timezone": "auto",
           "past_days": 7}
response = requests.get(url, params=payload)
response_json = response.json()

for key in response_json:
    print(key, response_json[key])

precipitation_observation = response_json["daily"]["precipitation_sum"][:7]
precipitation_prediction = response_json["daily"]["precipitation_sum"][7:]
et0_observation = response_json["daily"]["et0_fao_evapotranspiration"][:7]
et0_prediction = response_json["daily"]["et0_fao_evapotranspiration"][7:]

observations = zip(precipitation_observation, et0_observation)
observed_balance = reduce(lambda x, y: x + y,
                          [precipitation - et0
                           for (precipitation, et0)
                           in observations])

predictions = zip(precipitation_prediction, et0_prediction)
predicted_balance = reduce(lambda x, y: x + y,
                           [precipitation - et0
                            for (precipitation, et0)
                            in predictions])

print(observed_balance)
print(predicted_balance)

total_balance = observed_balance + predicted_balance
print(total_balance)

mm_per_can = liters_to_mm_per_square_meter * size_of_watering_can_in_liters
print(mm_per_can)
suggested_cans = - total_balance / mm_per_can if total_balance < 0 else 0
print(suggested_cans)
