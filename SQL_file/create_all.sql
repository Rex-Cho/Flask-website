#生成一系列的 DROP TABLE 陳述句，每個陳述句都針對指定資料庫中的一個表格
SELECT CONCAT('DROP TABLE IF EXISTS `', table_name, '`;')
FROM information_schema.tables
WHERE table_schema = 'database'; -- 替换为你的数据库名称
#程式主體
DESCRIBE `members`;
DESCRIBE `customer`;
DESCRIBE `administrator`;
DESCRIBE `business`;
DESCRIBE `order`;
DESCRIBE `product`;
DESCRIBE `order_have_product`;
DESCRIBE `customer_comment_business`;
DESCRIBE `coupon`;
DESCRIBE `customer_have_coupon`;
DESCRIBE `order_use_coupon`;
DESCRIBE `shopping_car`;
SHOW COLUMNS FROM `coupon`;
SHOW COLUMNS FROM `product`;
create database `database`;
show databases;
use `database`;
SHOW TABLES;
DROP database `database`;
create table members(
	`member_id` int  AUTO_INCREMENT not null,
    `email` VARCHAR(30)  not null ,
    `password` VARCHAR(10) not null,
    `name` VARCHAR(10) not null,
    `birthday` date not null,
    primary key(`member_id`, `email`)
);

create table `customer`(
	`member_id` int not null UNIQUE,
    primary key(`member_id`),
    foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
);

create table `administrator`(
	`member_id` int not null UNIQUE,
    primary key(`member_id`),
    foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
);

create table `business`(
	`member_id` int not null,
    primary key(`member_id`),
    foreign key(`member_id`) references members(`member_id`) on update cascade on delete cascade
);

create table `order`(
	`order_id` int AUTO_INCREMENT not null,
    `customer_id` int not null,
    `date` date not null,
    primary key(`order_id`,`customer_id`),
    foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade
);

create table `product`(
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
);
create table `coupon`(
	`coupon_id` int AUTO_INCREMENT,
    `administrator_id` int,
	`expire_date` date not null,
    `discount` DECIMAL(3, 2) CHECK (discount >= 0.01 AND discount <= 1.00) not null,
    primary key(`coupon_id`,`administrator_id`),
    foreign key (`administrator_id`) references `administrator`(`member_id`) on update cascade on delete cascade
);
create table `order_have_product`(
	`order_id` int ,
    `product_id` int,
	`amount` int not null,
    primary key(`order_id`,`product_id`),
    foreign key (`order_id`) references `order`(`order_id`) on update cascade on delete cascade,
    foreign key (`product_id`) references `product`(`product_id`) on update cascade on delete cascade
);
create table `customer_comment_business`(
	`comment_id` int AUTO_INCREMENT,
    `customer_id` int ,
    `business_id` int,
	`date` date not null,
    `text` char(255) not null,
    primary key(`comment_id`,`customer_id`,`business_id`),
    foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade,
    foreign key (`business_id`) references `business`(`member_id`) on update cascade on delete cascade
);

create table `customer_have_coupon`( 
	`coupon_id` int ,#1 2 3    
    `customer_id` int, #1,2,3  0.9 0.9 0.9
    primary key(`customer_id`,`coupon_id`),
    foreign key (`coupon_id`) references `coupon`(`coupon_id`) on update cascade on delete cascade,
    foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade
);
create table `order_use_coupon`(
	`order_id` int ,
    `coupon_id` int,
    primary key(`order_id`,`coupon_id`),
    foreign key (`order_id`) references `order`(`order_id`) on update cascade on delete cascade,
    foreign key (`coupon_id`) references `coupon`(`coupon_id`) on update cascade on delete cascade
);
create table `shopping_car`(
	`customer_id` int ,
    primary key(`customer_id`),
    foreign key (`customer_id`) references `customer`(`member_id`) on update cascade on delete cascade
);