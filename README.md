# 🍱 Meal Order System

A simple and efficient **Meal Order System** built with:

- 🧑‍💻 **Frontend**: Pure HTML/CSS (no frameworks)
- 🐍 **Backend**: Python Flask
- 📡 **Communication**: MQTT protocol to interact with the delivery robot

## 💡 Features

- Users can browse and place meal orders through a clean web interface
- Orders are processed via a Flask backend server
- Uses **MQTT** to communicate with an autonomous meal delivery bot for dispatching meals

## 🛠️ Tech Stack

| Layer       | Technology        |
|-------------|-------------------|
| Frontend    | HTML, CSS         |
| Backend     | Python Flask      |
| Communication | MQTT (paho-mqtt) |

## 🚀 How It Works

1. User places a meal order via the web interface
2. Flask receives the request and processes the order
3. The system publishes an MQTT message to notify the delivery bot
4. The delivery bot receives the message and dispatches the meal

## 🎥 Demo Video
[Video](https://youtu.be/KhfookRuu8A)
