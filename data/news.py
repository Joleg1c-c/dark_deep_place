import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    Dict_Month = {1: "Января", 2: "Февраля", 3: "Марта", 4: "Апреля", 5: "Мая", 6: "Июня",
                  7: "Июля", 8: "Августа", 9: "Сентября", 10: "Октября", 11: "Ноября", 12: "Декабря"}
    DATA = datetime.datetime.now()
    MIN = DATA.minute
    if len(str(MIN)) == 1:
        MIN = "0" + str(DATA.minute)
    HOU = DATA.hour
    if len(str(HOU)) == 1:
        HOU = "0" + str(DATA.hour)
    DATA2 = f"{HOU}:{MIN} {str(DATA.day)} {Dict_Month[DATA.month]} {DATA.year} года"

    created_date = sqlalchemy.Column(sqlalchemy.String,
                                     default=DATA2)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    imgs = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    categories = orm.relation("Category",
                              secondary="association",
                              backref="news")
    user = orm.relation('User')
