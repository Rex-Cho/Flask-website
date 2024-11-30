#insert data時確保AUTO_INCREMENT從1開始產生
ALTER TABLE `members` AUTO_INCREMENT = 1;
ALTER TABLE `order` AUTO_INCREMENT = 1;
ALTER TABLE `product` AUTO_INCREMENT = 1;
ALTER TABLE `coupon` AUTO_INCREMENT = 1;
ALTER TABLE `customer_comment_business` AUTO_INCREMENT = 1; #error
#刪除,新增或修改 table 和 table裡的attribute
DROP TABLE  `members`;
DROP TABLE  `order`;
DROP TABLE  `order_have_product`;
DROP TABLE  `customer_comment_business`;
ALTER TABLE `order`
DROP PRIMARY KEY,
DROP COLUMN `order_id`;

ALTER TABLE `order`
ADD primary key(`order_id`,`buyer_id`);

ALTER TABLE `customer_have_coupon`
CHANGE COLUMN `coupons_id` `coupon_id` INT;
ALTER TABLE `coupon`
CHANGE COLUMN `business_id` `administrator_id` INT;
#篩選資料
SELECT * 
FROM `members`;
SELECT * 
FROM `customer`;
SELECT * 
FROM `administrator`;
SELECT * 
FROM `business`;
SELECT * 
FROM `order`;#刪除又加入新的id時，自動產生的id會將被刪除的也參照進去。可在產生完表格後更改
SELECT * 
FROM `order_have_product`;
SELECT * 
FROM `product`;
SELECT * 
FROM `coupon`;
SELECT * 
FROM `customer_comment_business`;
SELECT * 
FROM `customer_have_coupon`;
SELECT * 
FROM `order_use_coupon`;
#刪除資料
DELETE FROM `customer_comment_business`;
#加入資料

INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('t1234567@yahoo.com','B#3212','阿明','1998-03-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('t1234568@yahoo.com','B#a45212','阿剛','1998-04-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('t12345s8@yahoo.com','B#a45ds12','大貓','1921-04-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('t12345s9@yahoo.com','B#wds12','阿葉','1967-04-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('t1fhfs5s9@yahoo.com','ashdeifje','阿高','1988-06-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('h1fhfs5s9@yahoo.com','dfjwqwje','阿威','1978-08-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('h13828949@gmail.com','sjdfgh45','阿文','1989-09-21');
INSERT INTO `members` (`email`,`password`,`name`,`birthday`) VALUES('dfgehwi28@gmail.com','furhvb23','阿咒','1978-07-21');
INSERT INTO `customer` (`member_id`) VALUES(3);
INSERT INTO `customer` (`member_id`) VALUES(4);
INSERT INTO `customer` (`member_id`) VALUES(5);
INSERT INTO `customer` (`member_id`) VALUES(6);
INSERT INTO `customer` (`member_id`) VALUES(7);
INSERT INTO `customer` (`member_id`) VALUES(8);
INSERT INTO `administrator` (`member_id`) VALUES(1);
INSERT INTO `administrator` (`member_id`) VALUES(2);
INSERT INTO `business` (`member_id`) VALUES(3);
INSERT INTO `business` (`member_id`) VALUES(4);
INSERT INTO `business` (`member_id`) VALUES(5);
INSERT INTO `business` (`member_id`) VALUES(6);
INSERT INTO `order` (`customer_id`,`date`) VALUES(3,'2023-11-21');
INSERT INTO `order` (`customer_id`,`date`) VALUES(3,'2023-11-22');
INSERT INTO `order` (`customer_id`,`date`) VALUES(4,'2023-11-23');
INSERT INTO `order` (`customer_id`,`date`) VALUES(5,'2023-11-24');
INSERT INTO `order` (`customer_id`,`date`) VALUES(6,'2023-11-24');
INSERT INTO `order` (`customer_id`,`date`) VALUES(7,'2023-11-25');
INSERT INTO `order` (`customer_id`,`date`) VALUES(7,'2023-11-25');
INSERT INTO `order` (`customer_id`,`date`) VALUES(8,'2023-11-26');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(5,'清潔劑',"clean.jpg",'2分鐘內打擊所有浴廁汙垢',299,8500,'2022-01-15');#填圖片路徑
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(5,'馬桶刷',"brush.jpg",'2分鐘內打擊所有馬桶汙垢',59,9500,'2022-01-16');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(6,'電視',"tv.jpg",'超清晰',10000,500,'2023-05-15');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(6,'電池',"battery.jpg",'長久好用',59,1500,'2022-05-16');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(3,'Switch',"switch.jpg",'超好玩',9780,800,'2023-08-15');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(4,'短素T',"Tshirt.jpg",'透氣好穿',399,500,'2022-11-16');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(4,'牛仔褲',"jeans.jpg",'修飾腿型',1000,600,'2022-12-15');
INSERT INTO `product` (`business_id`,`name`,`image`,`detail`,`money`,`quantity`,`publish_date`) VALUES(3,'玩具車',"toycar.jpg",'小孩都愛玩',80,3000,'2022-09-16');
INSERT INTO `coupon` (`administrator_id`,`expire_date`,`discount`) VALUES(1,'2023-11-25',0.75);
INSERT INTO `coupon` (`administrator_id`,`expire_date`,`discount`) VALUES(1,'2023-11-27',0.80);
INSERT INTO `coupon` (`administrator_id`,`expire_date`,`discount`) VALUES(2,'2023-12-03',0.90);
INSERT INTO `coupon` (`administrator_id`,`expire_date`,`discount`) VALUES(2,'2023-12-01',0.70);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(1,2,1);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(2,2,2);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(3,1,3);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(4,4,4);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(5,1,5);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(6,2,6);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(7,1,7);
INSERT INTO `order_have_product` (`product_id`,`amount`,`order_id`) VALUES(8,3,8);
INSERT INTO `customer_comment_business` (`customer_id`,`business_id`,`date`,`text`) VALUES(3,5,'2023-11-27','好好刷');
INSERT INTO `customer_comment_business` (`customer_id`,`business_id`,`date`,`text`) VALUES(4,6,'2023-11-28','負評看到眼睛快瞎了');
INSERT INTO `customer_comment_business` (`customer_id`,`business_id`,`date`,`text`) VALUES(6,3,'2023-11-28','好頂');
INSERT INTO `customer_comment_business` (`customer_id`,`business_id`,`date`,`text`) VALUES(7,4,'2023-11-29','乾白素T泛黃');
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(3,1);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(3,2);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(3,3);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(3,4);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(4,1);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(4,4);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(5,2);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(5,3);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(6,4);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(7,4);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(8,1);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(8,2);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(8,3);
INSERT INTO `customer_have_coupon` (`customer_id`,`coupon_id`) VALUES(8,4);
INSERT INTO `order_use_coupon` (`order_id`,`coupon_id`) VALUES(1,1);
INSERT INTO `order_use_coupon` (`order_id`,`coupon_id`) VALUES(2,4);
INSERT INTO `order_use_coupon` (`order_id`,`coupon_id`) VALUES(5,4);
INSERT INTO `order_use_coupon` (`order_id`,`coupon_id`) VALUES(8,2);
#INSERT INTO `shopping_car` (`customer_id`) VALUES('3');
#INSERT INTO `shopping_car` (`customer_id`) VALUES('4');
#INSERT INTO `shopping_car` (`customer_id`) VALUES('6');
#INSERT INTO `shopping_car` (`customer_id`) VALUES('7');
#INSERT INTO `shopping_car_have_product` (`customer_id`,`product_id`,`Amount`) VALUES('3','2','2');
#INSERT INTO `shopping_car_have_product` (`customer_id`,`product_id`,`Amount`) VALUES('4','3','1');
#INSERT INTO `shopping_car_have_product` (`customer_id`,`product_id`,`Amount`) VALUES('6','5','1');
#INSERT INTO `shopping_car_have_product` (`customer_id`,`product_id`,`Amount`) VALUES('7','5','1');