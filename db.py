from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'postgresql://postgres:postgres@localhost/postgres'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> SessionLocal:
    """Создаем объект сессии."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Car(Base):
    """Схема."""
    __tablename__ = 'cars'
    id = Column(Integer, Sequence('car_id_seq'), primary_key=True)
    brand = Column(String(50))
    color = Column(String(50))
    body = Column(String(50))


def init_db() -> None:
    """Заполняем таблицу если пустая."""
    db = SessionLocal()
    try:
        if db.query(Car).count() == 0:
            initial_cars = [
                Car(color='red', brand='Toyota', body='sedan'),
                Car(color='blue', brand='Honda', body='coupe'),
                Car(color='black', brand='BMW', body='suv'),
            ]
            db.add_all(initial_cars)
            db.commit()
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
init_db()
