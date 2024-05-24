import time
from flask import Flask, jsonify
from db import get_db, Car

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Определяем маршрут (endpoint) для обработки запросов на '/server_request'
@app.route("/cars")
def server_request():
    db = next(get_db())
    cars = db.query(Car).all()
    some_func_one()  # Имитируем стек вызовов
    return jsonify([{"id": car.id, "brand": car.brand, "color": car.color, "body": car.body} for car in cars])


def some_func_one() -> None:
    time.sleep(0.5)
    some_func_two()


def some_func_two() -> None:
    time.sleep(0.5)


if __name__ == "__main__":
    app.run(port=8082)
