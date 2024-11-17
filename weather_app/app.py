from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
                weather_data = None
                error_message = None

                if request.method == "POST":
                    city = request.form.get("city")
                    if city:
                        try:
                            api_key = "f531c2fb8dfe9f73b8cb22fd6a08f419"
                            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                            response = requests.get(url)
                            data = response.json()

                            if response.status_code == 200: 
                                weather_data = {
                                    "city": city,
                                    "temperature": data["main"]["temp"],
                                    "description": data["weather"][0]["description"],
                                    "humidity": data["main"]["humidity"],
                                    "wind_speed": data["wind"]["speed"],
                                    "icon": data["weather"][0]["icon"],
                                }
                            else:
                                error_message = "City not found. Please try again."
                        except Exception as e:
                            error_message = "Unable to fetch data. Please check your connection or API key."
                html_content = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Weather App</title>
                    <link rel="stylesheet" type="text/css" href="static/style.css">
                </head>
                <body>
                    <h1>Weather App</h1>
                    <form method="POST" action="/">
                        <input type="text" name="city" placeholder="Enter city name" required>
                        <button type="submit">Get Weather</button>
                    </form>
                """

                if weather_data:
                    html_content += f"""
                    <div class="weather-info">
                        <h2>Weather in {weather_data['city']}:</h2>
                        <p>Temperature: {weather_data['temperature']}°C</p>
                        <p>Description: {weather_data['description']}</p>
                        <p>Humidity: {weather_data['humidity']}%</p>
                        <p>Wind Speed: {weather_data['wind_speed']} m/s</p>
                        <img src="http://openweathermap.org/img/wn/{weather_data['icon']}.png" alt="Weather icon">
                    </div>
                    """
                elif error_message:
                    html_content += f'<p class="error">{error_message}</p>'

                html_content += """
                </body>
                </html>
                """

                return html_content

if __name__ == "__main__":
                app.run(debug=True, host='0.0.0.0')
