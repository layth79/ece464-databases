# ECE-464 Assignment 1 Part 2: representing sailors and boats schema using an ORM
# Layth Yassin 
# Professor Sokolov

from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.orm.session import Session

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

class Employee(Base):
    __tablename__ = 'employees'

    eid = Column(Integer, primary_key=True)
    ename = Column(String)
    job = Column(String)

    def __repr__(self):
        return "<Employee(eid=%s, name=%s, job=%s)>" % (self.eid, self.ename, self.job)

class Address(Base):
    __tablename__ = 'addresses'

    aid = Column(Integer, primary_key=True)
    eid = Column(Integer, ForeignKey('employees.eid'))
    zip = Column(Integer)
    line1 = Column(String)
    line2 = Column(String)
    city = Column(String)

    employee = relationship('Employee')

    def __repr__(self):
        return "<Address(aid=%s, eid=%s, line1=%s, line2=%s, city=%s, zip=%s)>" % (self.aid, self.eid, self.line1, self.line2, self.city, self.zip)

class Salary(Base):
    __tablename__ = 'salaries'

    salid = Column(Integer, primary_key=True)
    eid = Column(Integer, ForeignKey('employees.eid'))
    weeklyhrs = Column(Integer)
    hourlypay = Column(Integer)
    overtimehrs = Column(Integer)
    overtimepay = Column(Integer)

    employee = relationship('Employee')

    def __repr__(self):
        return "<Salary(salid=%s, eid=%s, weeklyhrs=%s, hourlypay=%s, overtimehrs=%s, overtimepay=%s)>" \
            % (self.salid, self.eid, self.weeklyhrs, self.hourlypay, self.overtimehrs, self.overtimepay)

engine = create_engine(
      "mysql+pymysql://layth79:@localhost/sailors?host=localhost", echo=True)

Base.metadata.create_all(engine)

conn = engine.connect()

Session = sessionmaker(bind=engine)
# part 2 tests
session = Session()

def test1():
    orm_q = session.query(func.count(Boat.bid), Boat.bid, Boat.bname).join(Reservation).group_by(Boat.bid).all()
    sql_q = conn.execute("SELECT COUNT(B.bid), B.bid, B.bname FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY bid").fetchall()
    assert orm_q == sql_q

def test2():
    sub = session.query(func.count(Boat.bid).label("numReds")).filter(Boat.color == "red").scalar()
    orm_q = session.query(Reservation.sid).join(Sailor).join(Boat).filter(Boat.color == "red") \
        .group_by(Reservation.sid).having(func.count(Reservation.sid) == sub).all()
    sql_q = conn.execute("SELECT R.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND B.bid = R.bid AND B.color = 'red' \
        GROUP BY R.sid HAVING COUNT(R.sid) = (SELECT COUNT(*) AS numReds FROM boats B WHERE B.color = 'red')").fetchall()
    assert orm_q == sql_q

def test3():
    sub1 = session.query(Sailor.sid).join(Reservation).join(Boat).filter(Boat.color == "red")
    sub2 = session.query(Sailor.sid).join(Reservation).join(Boat).filter(Boat.color != "red")
    orm_q = session.query(Sailor.sid, Sailor.sname).filter(and_(Sailor.sid.in_(sub1), Sailor.sid.not_in(sub2))).all()
    sql_q = conn.execute("SELECT S.sid, S.sname FROM sailors S WHERE S.sid IN \
        (SELECT S.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND R.bid = B.bid AND B.color = 'red') \
            AND S.sid NOT IN (SELECT S.sid FROM sailors S, reserves R, boats B WHERE S.sid = R.sid AND R.bid = B.bid AND B.color != 'red')").fetchall()
    assert orm_q == sql_q

def test4():
    sub1 = session.query(func.count(Boat.bid).label("numRes"), Boat.bid).join(Reservation).group_by(Reservation.bid).subquery()
    sub2 = session.query(func.max(sub1.c.numRes)).scalar()
    orm_q = session.query(sub1.c.numRes, sub1.c.bid).filter(sub1.c.numRes == sub2).all()
    sql_q = conn.execute("SELECT numRes, bid FROM (SELECT COUNT(*) AS numRes, B.bid FROM boats B, reserves R WHERE B.bid = R.bid GROUP BY R.bid) \
        AS freqTab WHERE numRes = (SELECT MAX(numRes) FROM (SELECT COUNT(*) AS numRes, B.bid FROM boats B, \
            reserves R WHERE B.bid = R.bid GROUP BY R.bid) AS freqTab2)").fetchall()
    assert orm_q == sql_q

def test5():
    sub = session.query(Reservation.sid).join(Boat).filter(Boat.color == "red")
    orm_q = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.not_in(sub)).all()
    sql_q = conn.execute("SELECT S.sid, S.sname FROM sailors S WHERE S.sid NOT IN \
        (SELECT R.sid FROM reserves R, boats B WHERE R.bid = B.bid AND B.color = 'red')").fetchall()
    assert orm_q == sql_q

def test6():
    orm_q = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).all()
    sql_q = conn.execute("SELECT AVG(S.age) FROM sailors S WHERE S.rating = 10").fetchall()
    assert orm_q == sql_q

def test7():
    sub_q = session.query(Sailor.rating, func.min(Sailor.age).label('minAge')).group_by(Sailor.rating).subquery()
    orm_q = session.query(Sailor.sname, Sailor.sid, Sailor.rating, Sailor.age).filter(and_(Sailor.age == sub_q.c.minAge, \
        Sailor.rating == sub_q.c.rating)).all()
    sql_q = conn.execute("SELECT S.sname, S.sid, S.rating, S.age FROM sailors S WHERE S.age IN \
        (SELECT MIN(S.age) FROM sailors S GROUP BY S.rating)").fetchall()
    assert orm_q == sql_q

def test8():
    sub1 = session.query(Sailor.sid, Sailor.sname, Boat.bid, func.count(Boat.bid).label("numRes")).filter(Reservation.sid == Sailor.sid, Reservation.bid == Boat.bid).group_by(Boat.bid, Sailor.sid).subquery()
    sub2 = session.query(sub1.c.sid, sub1.c.sname, sub1.c.bid, sub1.c.numRes, func.rank().over(partition_by=sub1.c.bid, order_by=sub1.c.numRes.desc()).label("ranking")).subquery()
    orm_q = session.query(sub2.c.sid, sub2.c.sname, sub2.c.bid, sub2.c.numRes).filter(sub2.c.ranking == 1).all()
    sql_q = conn.execute("SELECT sid, sname, bid, numRes FROM \
        (SELECT sid, sname, bid, numRes, RANK() OVER (PARTITION BY bid ORDER BY numRes DESC) AS ranking FROM \
            (SELECT S.sid, S.sname, B.bid, COUNT(*) AS numRes FROM sailors S, reserves R, boats B \
                WHERE B.bid = R.bid AND S.sid = R.sid GROUP BY B.bid, S.sid) AS tmp1) AS tmp2 WHERE ranking = 1").fetchall()
    assert orm_q == sql_q

session.close()

# # part 3 tests
session = Session()

def test9():
    # counts the number of employees
    orm_q = session.query(func.count(Employee.eid)).scalar()
    assert orm_q == 7

def test10():
    # finds the employee with the highest hourly pay
    sub = session.query(func.max(Salary.hourlypay)).scalar()
    orm_q = session.query(Salary.eid).filter(Salary.hourlypay == sub).scalar()
    assert orm_q == 204

def test11():
    # finds all employees who live in Greenport
    orm_q = session.query(Address.eid).filter(Address.city == 'greenport').all()
    correct = [204, 206]
    assert all(correct[i] == tmp[0] for i, tmp in enumerate(orm_q))

def test12():
    # computes how much business owes each employee for the week
    orm_q = session.query(Salary.eid, Salary.weeklyhrs * Salary.hourlypay + Salary.overtimehrs * Salary.overtimepay).all()
    correct = [(200, 700), (201, 640), (202, 1000), (203, 1750), (204, 2325), (205, 300), (206, 750)]
    assert all(correct[i] == tmp for i, tmp in enumerate(orm_q))

session.close()
