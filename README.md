# 🌦️ Real-Time Weather Prediction

![Weather Forecast UI](https://github.com/riyagarg11/Weather-Prediction-Real-Time/blob/main/Preview.jpg)

---

## 📌 Project Overview

**Real-Time Weather Prediction** is a web application that fetches live weather data for any city and displays a detailed weather forecast with a visually appealing UI. It uses real-time API integration and provides hourly temperature and humidity updates, along with additional environmental metrics like wind speed, pressure, and cloud coverage.

---

## 🚀 Features

- 🌍 Search for any city worldwide
- 🌡️ Live temperature & "feels like" display  
- 💧 Humidity, cloud, and pressure details  
- 🕐 Hourly forecast with temperature & humidity
- 🌦️ Predict weather based on input parameters 
- 🤖 Trained using a machine learning model from a Jupyter notebook  
- 🎨 Simple UI and live predictions   
- 🌬️ Wind speed & visibility metrics  
- 📅 Date and local time shown dynamically  
- 🎨 Intuitive and responsive UI  

---

## 🛠️ Tech Stack

| Technology      | Description                          |
|-----------------|--------------------------------------|
| **Frontend**    | HTML, CSS, JavaScript                |
| **Backend**     | Python (Django)                      |
| **API**         | [OpenWeatherMap API](https://openweathermap.org/api) |
| **Rendering**   | Dynamic weather rendering with CSS   |
| **Hosting**     | Localhost / Can be deployed on Heroku, Render, etc. |

---

## 📸 UI Preview

> The interface shows the forecast for Mumbai with real-time data:

- **Current Temp:** 28°C  
- **Feels Like:** 32°C  
- **Humidity:** 82%  
- **Cloud Coverage:** 100%  
- **Wind:** 5.58 km/h  
- **Pressure:** 1003 mb  
- **Hourly Breakdown:** Temperature and Humidity till 7:00 PM  

---

## 🧠 How It Works

1. **City Search**: User inputs a city name  
2. **API Call**: Backend fetches real-time data from OpenWeatherMap  
3. **Data Parsing**: Temperature, humidity, and other weather details are extracted  
4. **Frontend Display**: Weather metrics and hourly breakdown are rendered dynamically  

---


## 📂 Project Structure

```bash
Real-Time-Weather-Prediction/
│
├── weather_app/               
│   ├── migrations/            
│   ├── static/               
│   ├── templates/             
│   │   └── index.html        
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/                     
├── db.sqlite3                
├── manage.py                 
├── requirements.txt         
├── README.md                  
├── Preview.jpg                
└── Real_Time_Weather/        
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

