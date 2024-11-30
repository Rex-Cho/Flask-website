from datetime import date
from sqlalchemy import create_engine, BLOB, Column, Text, Integer, String, Date, ForeignKey, Float, DECIMAL, CheckConstraint, LargeBinary
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash

#Base = declarative_base()
db = SQLAlchemy()
Base = db.Model

class Member(Base, UserMixin):
    __tablename__ = 'members'
    #__abstract__ = True

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    name = Column(String(128), nullable=False)
    birthday = Column(Date, nullable=False)
    customer = relationship('Customer', uselist=False, back_populates='member', cascade='all, delete-orphan')
    administrator = relationship('Administrator', uselist=False, back_populates='member', cascade='all, delete-orphan')
    business = relationship('Business', uselist=False, back_populates='member', cascade='all, delete-orphan')
    account_tpye = Column(Integer)
    __mapper_args__ = { 'polymorphic_on': account_tpye }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<Name %r>' % self.name
    #flask login
    def get_id(self):
        return str(self.member_id)


class Customer(Member):
    __tablename__ = 'customer'
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, unique=True)
    member = relationship('Member', back_populates='customer', cascade='all')
    customer_have_coupon = relationship('CustomerHaveCoupon', back_populates='customer', cascade='all')
    orders = relationship('Order', back_populates='customer', cascade='all')
    #comments = relationship('CustomerCommentBusiness', back_populates='customer', cascade='all, delete-orphan')
    __mapper_args__ = { 'polymorphic_identity': 0 }

class Business(Member):
    __tablename__ = 'business'

    member_id = Column(Integer, ForeignKey('members.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    member = relationship('Member', back_populates='business', cascade='all')
    #products = relationship('Product', back_populates='business', cascade='all, delete-orphan')
    #comments = relationship('CustomerCommentBusiness', back_populates='business', cascade='all, delete-orphan')
    __mapper_args__ = { 'polymorphic_identity': 1 }

class Administrator(Member):
    __tablename__ = 'administrator'
    '''
    '''
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True, unique=True)
    member = relationship('Member', back_populates='administrator', cascade='all')
    coupons = relationship('Coupon', back_populates='administrator', cascade='all, delete-orphan')
    __mapper_args__ = { 'polymorphic_identity': 2 }

class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.member_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    customer = relationship('Customer', back_populates='orders', cascade='all')
    order_have_product = relationship('OrderHaveProduct', back_populates='order', cascade='all')
    order_use_coupon = relationship('OrderUseCoupon', back_populates='order', cascade='all')

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    business_id = Column(Integer, ForeignKey('business.member_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)
    image = Column(BLOB(102400), nullable=False)
    detail = Column(Text, nullable=False)
    money = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    publish_date = Column(Date, nullable=False)
    #business = relationship('Business', back_populates='products', cascade='all')
    order_have_product = relationship('OrderHaveProduct', back_populates='product', cascade='all, delete-orphan')

class Coupon(Base):
    __tablename__ = 'coupon'
    coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    administrator_id = Column(Integer, ForeignKey('administrator.member_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    expire_date = Column(Date, nullable=False)
    discount = Column(DECIMAL(3, 2), CheckConstraint('discount >= 0.01 AND discount <= 1.00'), nullable=False)
    administrator = relationship('Administrator', back_populates='coupons', cascade='all')
    customer_have_coupon = relationship('CustomerHaveCoupon', back_populates='coupon', cascade='all, delete-orphan')
    order_use_coupon = relationship('OrderUseCoupon', back_populates='coupon', uselist=False, cascade='all, delete-orphan')

class OrderHaveProduct(Base):
    __tablename__ = 'order_have_product'
    order_id = Column(Integer, ForeignKey('order.order_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    amount = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='order_have_product', cascade='all')
    product = relationship('Product', back_populates='order_have_product', cascade='all')

'''
class CustomerCommentBusiness(Base):
    __tablename__ = 'customer_comment_business'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.member_id'), nullable=False)
    business_id = Column(Integer, ForeignKey('business.member_id'), nullable=False)
    date = Column(Date, nullable=False)
    text = Column(Text, nullable=False)
    customer = relationship('Customer', back_populates='comments', cascade='all')
    business = relationship('Business', back_populates='comments', cascade='all')
'''

class CustomerHaveCoupon(Base):
    __tablename__ = 'customer_have_coupon'
    coupon_id = Column(Integer, ForeignKey('coupon.coupon_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    customer = relationship('Customer', back_populates='customer_have_coupon', cascade='all')
    coupon = relationship('Coupon', back_populates='customer_have_coupon', cascade='all')

class OrderUseCoupon(Base):
    __tablename__ = 'order_use_coupon'
    order_id = Column(Integer, ForeignKey('order.order_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    coupon_id = Column(Integer, ForeignKey('coupon.coupon_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    order = relationship('Order', back_populates='order_use_coupon', cascade='all')
    coupon = relationship('Coupon', back_populates='order_use_coupon', cascade='all')

class Car(Base):
    __tablename__ = 'car'
    customer_id = Column(Integer, ForeignKey('customer.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

class CarHaveProduct(Base):
    customer_id = Column(Integer, ForeignKey('car.customer_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.product_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    amount = Column(Integer, nullable=False)

class ChatContainer(Base):
    __tablename__ = 'chat_container'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    business_id = Column(Integer, ForeignKey('business.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    chats = relationship('Chat', uselist=True, back_populates='container', cascade='all, delete-orphan')

class Chat(Base):
    __tablename__ = 'chat'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    container_id = Column(Integer, ForeignKey('chat_container.chat_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    owner_id = Column(Integer, ForeignKey('members.member_id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    date = Column(Date, nullable=False)
    text = Column(Text, nullable=False)
    container = relationship('ChatContainer', back_populates='chats')

'''

# 創建資料庫引擎
engine = create_engine('mysql+mysqlconnector://your_username:your_password@your_host/your_database')

# 創建資料表
Base.metadata.create_all(engine)
'''