import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'database',
    passwd = 'database110590025',
    database= 'database'
)
cursor = mydb.cursor()

sql_commands = [
    "DROP TABLE IF EXISTS `members`;",
    "DROP TABLE IF EXISTS `customer`;",
    "DROP TABLE IF EXISTS `administrator`;",
    "DROP TABLE IF EXISTS `business`;",
    "DROP TABLE IF EXISTS `order`;",
    "DROP TABLE IF EXISTS `product`;",
    "DROP TABLE IF EXISTS `order_have_product`;",
    "DROP TABLE IF EXISTS `customer_comment_business`;",
    "DROP TABLE IF EXISTS `coupon`;",
    "DROP TABLE IF EXISTS `customer_have_coupon`;",
    "DROP TABLE IF EXISTS `order_use_coupon`;",
    "CREATE DATABASE IF NOT EXISTS `database`;",
    "SHOW DATABASES;",
    "USE `database`;",
    "SHOW TABLES;",
    "DROP DATABASE IF EXISTS `database`;",
    """CREATE TABLE `members`(
        `member_id` int AUTO_INCREMENT not null,
        `email` VARCHAR(30) not null,
        `password` VARCHAR(10) not null,
        `name` VARCHAR(10) not null,
        `birthday` date not null,
        primary key(`member_id`, `email`)
    );""",
    """CREATE TABLE `customer`(
        `member_id` int not null UNIQUE,
        primary key(`member_id`),
        foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `administrator`(
        `member_id` int not null UNIQUE,
        primary key(`member_id`),
        foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `business`(
        `member_id` int not null,
        primary key(`member_id`),
        foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `order`(
        `order_id` int AUTO_INCREMENT not null,
        `customer_id` int not null,
        `date` date not null,
        primary key(`order_id`,`customer_id`),
        foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `product`(
        `product_id` int AUTO_INCREMENT,
        `business_id` int,
        `name` VARCHAR(10) not null,
        `image` Blob not null,
        `detail` VARCHAR(255) not null,
        `money` int not null,
        `quantity` int not null,
        `publish_date` date not null,
        primary key(`product_id`,`business_id`),
        foreign key (`business_id`) references `business`(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `coupon`(
        `coupon_id` int AUTO_INCREMENT,
        `administrator_id` int,
        `expire_date` date not null,
        `discount` DECIMAL(3, 2) CHECK (discount >= 0.01 AND discount <= 1.00) not null,
        primary key(`coupon_id`,`administrator_id`),
        foreign key (`administrator_id`) references `administrator`(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `order_have_product`(
        `order_id` int ,
        `product_id` int,
        `amount` int not null,
        primary key(`order_id`,`product_id`),
        foreign key (`order_id`) references `order`(`order_id`) on update cascade on delete cascade,
        foreign key (`product_id`) references `product`(`product_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `customer_comment_business`(
        `comment_id` int AUTO_INCREMENT,
        `customer_id` int ,
        `business_id` int,
        `date` date not null,
        `text` char(255) not null,
        primary key(`comment_id`,`customer_id`,`business_id`),
        foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade,
        foreign key (`business_id`) references `business`(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `customer_have_coupon`(
        `coupon_id` int ,
        `customer_id` int,
        primary key(`customer_id`,`coupon_id`),
        foreign key (`coupon_id`) references `coupon`(`coupon_id`) on update cascade on delete cascade,
        foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade
    );""",
    """CREATE TABLE `order_use_coupon`(
        `order_id` int ,
        `coupon_id` int,
        primary key(`order_id`,`coupon_id`),
        foreign key (`order_id`) references `order`(`order_id`) on update cascade on delete cascade,
        foreign key (`coupon_id`) references `coupon`(`coupon_id`) on update cascade on delete cascade
    );"""
]

try:
    '''
    for command in sql_commands:
        print(command)
        cursor.execute(command)
    '''
    cursor.execute("create database tempdatabase")
    mydb.commit()
except:
    mydb.rollback()
    print("an error has occured")
finally:
    cursor.close()
    mydb.close()