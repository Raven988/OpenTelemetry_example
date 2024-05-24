import time

from flask import Flask, jsonify
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider

from db import get_db, Car, engine

# Создаем ресурс с атрибутом 'service.name'
resource = Resource(attributes={
    "service.name": 'server_programmatic'
})
# Устанавливаем TracerProvider с созданным ресурсом
set_tracer_provider(TracerProvider(resource=resource))
# Добавляем BatchSpanProcessor для отправки трассировок с использованием OTLPSpanExporter
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())
)

app = Flask(__name__)
# Инструментируем Flask приложение для автоматического сбора трассировок
FlaskInstrumentor().instrument_app(app, excluded_urls=None)  # excluded_urls исключает указанные URL
# Инструментируем SQLAlchemy приложение для автоматического сбора трассировок
SQLAlchemyInstrumentor().instrument(engine=engine)

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
