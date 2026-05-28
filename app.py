from flask import Flask, render_template,request
import requests

import os

app=Flask(__name__)
API_KEY="https://api.weatherapi.com/v1/current.json?key=fd06a3c7618843e48fc122703260904&q"

@app.route("/", methods=["GET","POST"])
def index():
    weather =None
    if request.method == "POST":
        city=request.form.get("city")
        if city:
            url=f"https://api.weatherapi.com/v1/current.json?key=fd06a3c7618843e48fc122703260904&q={city}"
            response = requests.get(url)
            data=response.json()

            condition = data["current"]["condition"]["text"].lower()
            is_day = int(data["current"]["is_day"])
            
            animation = "default"

            if "sunny" in condition or "clear" in condition:
               animation = "sun_day" if is_day == 1 else "clear_night"
            elif "cloud" in condition:
               animation = "cloud_day" if is_day == 1 else "cloud_night"
            elif "overcast"in condition:
               animation = "overcast"   
            elif "rain" in condition:
               animation = "rain"
            elif "storm" in condition:
               animation = "storm"
            elif "snow" in condition:
               animation = "snow"

            weather={
                    "city": data["location"]["name"],
                    "temp": data["current"]["temp_c"],
                    "desc": data["current"]["condition"]["text"],
                    "humidity": data["current"]["humidity"],
                    "animation": animation
                }
        else:
            weather={
               "city": "City not found ",
               "temp": "--",
               "desc": "Try again",
               "humidity": "--"
            }  

    return render_template("index.html",
                           weather=weather)

@app.route("/location")
def location_weather():
   lat=request.args.get("lat")
   lon=request.args.get("lon")

   url=f"https://api.weatherapi.com/v1/current.json?key=fd06a3c7618843e48fc122703260904&q={lat},{lon}"
   response=requests.get(url)
   data=response.json()

   condition = data["current"]["condition"]["text"].lower()
   is_day = int(data["current"]["is_day"])

   animation = "default"

   if "sunny" in condition or "clear" in condition:
        animation = "sun_day" if is_day == 1 else "clear_night"
   elif "cloud" in condition:
        animation = "cloud_day" if is_day == 1 else "cloud_night"
   elif "rain" in condition:
        animation = "rain"

   weather = {
        "city": data["location"]["name"],
        "temp": data["current"]["temp_c"],
        "condition": data["current"]["condition"]["text"],
        "humidity": data["current"]["humidity"],
        "animation": animation
    }

   return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)

