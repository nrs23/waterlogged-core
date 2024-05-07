from functools import reduce
import requests


def water_balance(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"
    payload = {"latitude": latitude,
               "longitude": longitude,
               "daily": ["precipitation_sum", "et0_fao_evapotranspiration"],
               "timezone": "auto",
               "past_days": 7}
    response = requests.get(url, params=payload)
    response_json = response.json()

    precipitation = response_json["daily"]["precipitation_sum"]
    et0 = response_json["daily"]["et0_fao_evapotranspiration"]

    data = list(zip(precipitation, et0))
    observations = data[:7]
    predictions = data[7:]

    observed_balance = reduce(lambda x, y: x + y,
                              [precipitation - et0
                               for (precipitation, et0)
                               in observations])

    predicted_balance = reduce(lambda x, y: x + y,
                               [precipitation - et0
                                for (precipitation, et0)
                                in predictions])

    water_balance = observed_balance + predicted_balance
    return {"observed": observed_balance,
            "predicted": predicted_balance,
            "total": water_balance}


if __name__ == "__main__":
    # Brighton coordinates
    latitude = 50.83
    longitude = -0.14
    size_of_watering_can = 5  # Litres
    mm_per_litre = 1  # Number of mm of water per litre applied

    water_balance = water_balance(latitude, longitude)

    print(f'Observed mm of water in or out of the soil in last week: '
          f'{water_balance["observed"]:.0f}')
    print(f'Predicted mm of water in or out of the soil over next week: '
          f'{water_balance["predicted"]:.0f}')
    suggested_litres = (- water_balance['total'] / mm_per_litre
                        if water_balance['total'] < 0 else 0)
    suggested_cans = suggested_litres/size_of_watering_can
    print(f'Suggest applying {suggested_litres:.0f} litres of water '
          'to your garden '
          f'(or {suggested_cans:.0f}x {size_of_watering_can}L cans) '
          'per square meter over the coming week')
