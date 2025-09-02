#backend/app/shared/db/base.py
from sqlalchemy.orm import DeclarativeBase, declared_attr




class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Convierte el nombre de la clase 'UserModel' a 'users'
        return cls.__name__.lower().replace("model", "") + "s"
