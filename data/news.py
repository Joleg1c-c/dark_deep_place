import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    Dict_Month = {1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля", 5: "Мая", 6: "Июня",
                  7: "Июля", 8: "Августа", 9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"}
    DATA = datetime.datetime.now()
    DATA2 = " ".join([str(i) for i in [str(DATA.hour) + ":" + str(DATA.minute),
                                       DATA.day, Dict_Month[DATA.month], DATA.year, "года"]])

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # created_date = sqlalchemy.Column(sqlalchemy.DateTime,
    #                                  DATA2)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    categories = orm.relation("Category",
                              secondary="association",
                              backref="news")
    user = orm.relation('User')