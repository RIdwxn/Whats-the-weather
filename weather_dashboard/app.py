import webbrowser
from threading import Timer
from flask import Flask, render_template, request
import requests

app = Flask(__name__)



def get_weather(city, api_key):
    # Construct the API URL with the desired parameters

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url, timeout=5)
        # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()  
        data = response.json()

        # Check if the API indicates an error (e.g., incorrect city name)
        if data.get("cod") != 200:
            # Log the error message from the API (e.g., city not found)
            print("API error:", data.get("message"))
            return None

        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None 
    error = None 
    if request.method == 'POST':
        city = request.form.get('city')
        api_key = "f466702d14034c7db118243d26c54fb9"
        weather = get_weather(city, api_key)
        if weather is None:
            error = "City not found or unable to retrieve data. Please enter a valid city name."
    return render_template('index.html', weather=weather, error=error)

def open_browser():
    print("Opening browser...")
    webbrowser.open_new("http://127.0.0.1:5000/")
    
if __name__ == "__main__":
    from threading import Timer
    import webbrowser

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000/")

    Timer(1, open_browser).start()
    app.run(debug=True)



