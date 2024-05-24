import time

from flask import Flask, request, jsonify
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.propagate import extract
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import (
    SpanKind,
    get_tracer_provider,
    set_tracer_provider,
)

from db import get_db, Car

app = Flask(__name__)

# Создаем ресурс с атрибутом 'service.name'
resource = Resource(attributes={
    'service.name': 'server_manual'
})
# Устанавливаем TracerProvider с созданным ресурсом
set_tracer_provider(TracerProvider(resource=resource))
# Получаем экземпляр трассировщика (tracer)
tracer = get_tracer_provider().get_tracer(__name__)
# Добавляем BatchSpanProcessor для отправки трассировок с использованием OTLPSpanExporter
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())
)

@app.route('/cars')
def server_request():
    # Создаем и начинаем новую span для текущего запроса
    with tracer.start_as_current_span(
        'server_request',                        # Имя span
        context=extract(request.headers),       # Извлекаем контекст из заголовков запроса
        kind=SpanKind.SERVER,                   # Указываем, что span типа SERVER
        attributes=collect_request_attributes(request.environ),  # Добавляем атрибуты запроса
    ):
        db = next(get_db())
        cars = db.query(Car).all()
        some_func_one()  # Имитируем стек вызовов
        return jsonify([{"id": car.id, "brand": car.brand, "color": car.color, "body": car.body} for car in cars])


def some_func_one() -> None:
    # Создаем и начинаем новую span для текущего запроса
    with tracer.start_as_current_span("some_func_one"):
        time.sleep(0.5)
        some_func_two()


def some_func_two() -> None:
    # Создаем и начинаем новую span для текущего запроса
    with tracer.start_as_current_span("some_func_two"):
        time.sleep(0.5)


if __name__ == '__main__':
    app.run(port=8082)
