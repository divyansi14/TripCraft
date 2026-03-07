def weather_penalty(poi, weather):
    if weather["condition"] == "Rain":
        if poi["category"] in ["nature", "leisure"]:
            return 0.5
    if weather["temp"] > 35 and poi["category"] == "nature":
        return 0.6
    return 1.0