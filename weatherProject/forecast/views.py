from django.shortcuts import render

# Create your views here.
import requests #Library for fetching data from API
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder #To convert categorical data into numerical values
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta #To handle date and time
import pytz
import os

API_KEY= '69d00c5241d81109680af78ea9926066'
BASE_URL='https://api.openweathermap.org/data/2.5/'

def get_current_weather(city):
  url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric" #API Request URL
  response = requests.get(url)

  if response.status_code != 200:
        return None  # or return {"error": "City not found"}
      
  data = response.json()

  if 'name' not in data or 'main' not in data:
        return None

  return{
      'city' : data['name'],
      'current_temperature' : round(data['main']['temp']),
      'feels_like' : round(data['main']['feels_like']),
      'temp_min' : round(data['main']['temp_min']),
      'temp_max' : round(data['main']['temp_max']),
      'humidity' : round(data['main']['humidity']),
      'description' : data['weather'][0]['description'],
      'country' : data['sys']['country'],
      'wind_gust_dir' : data['wind']['deg'],
      'pressure' : data['main']['pressure'],
      'Wind_Gust_Speed' : data['wind']['speed'],

      'clouds' : data['clouds']['all'],
      'visibility': data['visibility']
  }

def read_historical_data(filename):
  df=pd.read_csv(filename)
  df=df.dropna()
  df=df.drop_duplicates()
  return df

def prepare_data(data):
  le = LabelEncoder() #Create a label encoder
  data['WindGustDir'] = le.fit_transform(data['WindGustDir'])
  data['RainTomorrow'] = le.fit_transform(data['RainTomorrow'])

  X = data[['MinTemp', 'MaxTemp', 'WindGustDir', 'WindGustSpeed','Humidity', 'Pressure', 'Temp']] #Feature Variable
  y = data['RainTomorrow'] #Target Variable

  return X, y, le

def train_rain_model(X, y):
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
  model = RandomForestClassifier(n_estimators=100, random_state = 42)
  model.fit(X_train, y_train) #Training the model

  y_pred = model.predict(X_test)

  accuracy = mean_squared_error(y_test, y_pred)
  print(f"Mean Squared Error for rain model: {accuracy}")

  return model

def prepare_regreession_data(data, feature):
  X, y = [], [] #Lists for feature and target values

  for i in range(len(data) - 1):
    X.append(data[feature].iloc[i])

    y.append(data[feature].iloc[i + 1])

  X = np.array(X).reshape(-1, 1)
  y = np.array(y)
  return X, y

def train_regression_model(X, y):
  model = RandomForestRegressor(n_estimators=100, random_state=42)
  model.fit(X, y) #Train the model

  return model

def predict_future(model, current_value):
  predictions = [current_value]

  for i in range(5):
    next_value = model.predict(np.array([[predictions[-1]]]))

    predictions.append(next_value[0])

  return predictions[1:]



def weather_view(request):
  if request.method=='POST':
    city=request.POST.get('city')
    current_weather = get_current_weather(city)

    #load historical data
    csv_path=os.path.join('C:\\Users\\Riya Garg\\OneDrive\\Desktop\\ml-project\\weather.csv')
    historical_data = read_historical_data(csv_path)

    #prepare and train the rain prediction model
    X, y, le = prepare_data(historical_data)

    rain_model = train_rain_model(X, y)

    #Map wind direction to compass points(because the API provides numerical values only)

    wind_deg = current_weather['wind_gust_dir'] % 360
    compass_points = [
        ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25), ("ENE", 56.25, 78.75),
        ("E", 78.75, 101.25), ("ESE", 101.25, 123.75), ("SE", 123.75, 146.25), ("SSE",146.25, 168.75),
        ("S", 168.75, 191.25), ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
        ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25), ("NNW", 326.25, 348.75)
    ]
    compass_direction = next(direction for direction, start, end in compass_points if start <= wind_deg < end)

    compass_direction_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1


    current_data = {
        'MinTemp' : current_weather['temp_min'],
        'MaxTemp' : current_weather['temp_max'],
        'WindGustDir' : compass_direction_encoded,
        'WindGustSpeed' : current_weather['Wind_Gust_Speed'],
        'Humidity' : current_weather['humidity'],
        'Pressure' : current_weather['pressure'],
        'Temp' : current_weather['current_temperature']
    }

    current_df = pd.DataFrame([current_data])

    #Rain Prediction

    rain_prediction = rain_model.predict(current_df)[0]

    #Prepare regression model for temperature and humididty

    X_temp, y_temp = prepare_regreession_data(historical_data, 'Temp')
    X_hum, y_hum = prepare_regreession_data(historical_data, 'Humidity')

    temp_model = train_regression_model(X_temp, y_temp)
    hum_model = train_regression_model(X_hum, y_hum)

    #Predict future temperature and Himidity

    future_temp = predict_future(temp_model, current_weather['temp_min'])

    future_hum = predict_future(hum_model, current_weather['humidity'])

    #Prepare time for future predictions
    timezone = pytz.timezone('Asia/Kolkata')
    now = datetime.now(timezone)
    next_hour = now + timedelta(hours=1)
    next_hour = next_hour.replace(minute=0, second=0, microsecond=0)

    future_times = [(next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)]
    
    #store each data separately
    time1, time2, time3, time4, time5=future_times
    temp1, temp2, temp3, temp4, temp5 = future_temp
    hum1, hum2, hum3, hum4,hum5= future_hum

    #pass data to template
    context={
      'location': city,
      'current_temperature': current_weather['current_temperature'],
      'MinTemp': current_weather['temp_min'],
      'MaxTemp': current_weather['temp_max'],
      'feels_like': current_weather['feels_like'],
      'humidity': current_weather['humidity'],
      'clouds': current_weather['clouds'],
      'description': current_weather['description'],
      'city': current_weather['city'],
      'country': current_weather['country'],

      'time': datetime.now(),
      'date': datetime.now().strftime("%B %d, %Y"),

      'wind': current_weather['Wind_Gust_Speed'],
      'pressure': current_weather['pressure'],
      'visibility': current_weather['visibility'],

      'time1':time1,
      'time2':time2,
      'time3':time3,
      'time4':time4,
      'time5':time5,

      'temp1':f"{round(temp1,1)}",
      'temp2':f"{round(temp2,2)}",
      'temp3':f"{round(temp3,3)}",
      'temp4':f"{round(temp4,4)}",
      'temp5':f"{round(temp5,5)}",

      'hum1':f"{round(hum1,1)}",
      'hum2':f"{round(hum2,2)}",
      'hum3':f"{round(hum3,3)}",
      'hum4':f"{round(hum4,4)}",
      'hum5':f"{round(hum5,5)}",

    }
    return render(request,'weather.html',context)
  return render(request,'weather.html')