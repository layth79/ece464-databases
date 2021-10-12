# ECE-464 Assignment 1 Part 2: representing sailors and boats schema using an ORM
# Layth Yassin 
# Professor Sokolov

from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.selectable import subquery
# import pymysql
# import pytest

Base = declarative_base()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

engine = create_engine(
      "mysql+pymysql://layth79:@localhost/sailors?host=localhost", echo=True)

Base.metadata.create_all(engine)

conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

def test_1():
    orm_q = session.query(func.count(Boat.bid), Boat.bid, Boat.bname).join(Reservation).group_by(Boat.bid).all()
    sql_q = conn.execute("SELECT COUNT(B.bid), B.bid, B.bname FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY bid").fetchall()
    assert orm_q == sql_q

# def test2():
#     orm_q = session.query(Reservation.sid)
#     sql_q = conn.execute("SELECT R.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND B.bid = R.bid AND B.color = 'red' GROUP BY R.sid HAVING COUNT(R.sid) = (SELECT COUNT(*) AS numReds FROM boats B WHERE B.color = 'red')")
#     assert orm_q == sql_q

# def test3():
#     orm_q =
#     sql_q = conn.execute("SELECT S.sid, S.sname FROM sailors S WHERE S.sid IN (SELECT S.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red') AND S.sid NOT IN (SELECT S.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND R.bid = B.bid AND B.color != 'red')")
#     assert orm_q == sql_q

# def test4():
#     # orm_q =
#     sql_q = conn.execute("SELECT numRes, bid FROM (SELECT COUNT(*) AS numRes, B.bid FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY R.bid) AS freqTab WHERE numRes = (SELECT MAX(numRes) FROM (SELECT COUNT(*) AS numRes, B.bid FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY R.bid) AS freqTab2)")

# def test5():
#     orm_q =
#     sql_q = conn.execute("SELECT S.sid, S.sname FROM sailors S WHERE S.sid NOT IN (SELECT S.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red')")
#     assert orm_q == sql_q

def test6():
    orm_q = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).all()
    sql_q = conn.execute("SELECT AVG(S.age) FROM sailors S WHERE S.rating = 10").fetchall()
    assert orm_q == sql_q

def test7():
    sub_q = session.query(func.min(Sailor.age)).join(Sailor).group_by(Sailor.rating)
    orm_q = session.query(Sailor.sname, Sailor.sid, Sailor.rating, Sailor.age).join(Sailor).filter(Sailor.age.in_(sub_q)).all()
    sql_q = conn.execute("SELECT S.sname, S.sid, S.rating, S.age FROM sailors S WHERE S.age IN (SELECT MIN(S.age) FROM sailors S GROUP BY S.rating)").fetchall()
    assert orm_q == sql_q

# def test8():
#     orm_q =
#     sql_q = conn.execute("SELECT sid, sname, bid, numRes FROM (SELECT sid, sname, bid, numRes, RANK() OVER (PARTITION BY bid ORDER BY numRes DESC) AS ranking FROM (SELECT S.sid, S.sname, B.bid, COUNT(*) AS numRes FROM sailors S, reserves R, boats B WHERE B.bid = R.bid AND S.sid = R.sid GROUP BY B.bid, S.sid) AS tmp1) AS tmp2 WHERE ranking = 1")
#     assert orm_q == sql_q
