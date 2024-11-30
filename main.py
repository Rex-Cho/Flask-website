from flask import Flask, render_template, flash, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from datetime import datetime
import base64
from database import *
from forms import *
from sqlalchemy.orm import joinedload
from flask import jsonify
#from flask_migrate import Migrate

def query_toal_sale(product_id):
    total = 0
    product_list = OrderHaveProduct.query.filter_by(product_id = product_id).all()
    #print(product_list)
    for products in product_list:
        total += products.amount
    print(total)
    return total 

def query_order_have_product(order_id):
    product_list = []
    product_list_two = []
    products = OrderHaveProduct.query.filter_by(order_id = order_id).all()
    for product in products:
        product_list_two.append(Product.query.get(product.product_id))
        product_list_two.append(product.amount)
        product_list.append(product_list_two)
        product_list_two = []
    return product_list

def query_all_order():
    order_with_current_user = []
    if current_user.is_authenticated:
        orders = Order.query.filter_by(customer_id = current_user.member_id).all()
        for order in orders:
            order_with_current_user.append(order)
    return order_with_current_user

def query_all_products():
    # 查詢所有商品
    all_products = []
    all_products = Product.query.all()
    return all_products

def query_all_car():
    cart_with_product_info = []
    if current_user.is_authenticated:
        user_cart_items = CarHaveProduct.query.filter_by(customer_id=current_user.member_id).all()
        for cart_item in user_cart_items:
            product_info = {
                "product": Product.query.get(cart_item.product_id),
                "amount": cart_item.amount
            }
            cart_with_product_info.append(product_info)

    return cart_with_product_info

def calculate_total_price(cars_product):
    total_price = 0 
    total_amount = 0
    for cart_item in cars_product:
        product = cart_item["product"]
        amount = cart_item["amount"]
        total_price += product.money * amount
        total_amount += amount
    return total_price, total_amount

def query_all_customer():
    customer_list = Customer.query.all()
    return customer_list

def find_can_use_coupon():
    current_time = datetime.now()
    can_use_coupon_list = []
    coupon_list = CustomerHaveCoupon.query.filter_by(customer_id = current_user.member_id).all()
    print(coupon_list) #1
    #have_been_use_coupon = OrderUseCoupon.query.filter_by(customer_id = current_user.member_id).all()
    current_user_id = current_user.member_id  # 请将其替换为你实际的用户ID

    # 查找 OrderUseCoupon 中满足条件的记录
    orders_with_user_coupon = (
        db.session.query(OrderUseCoupon)
        .join(Order, OrderUseCoupon.order_id == Order.order_id)
        .filter(Order.customer_id == current_user_id)
        .all()
    )
    print(orders_with_user_coupon) #2
    used_coupon_ids = {coupon.coupon_id for coupon in orders_with_user_coupon}
    print(used_coupon_ids) #3
    can_use_coupon = [coupon for coupon in coupon_list if coupon.coupon_id not in used_coupon_ids]
    print (can_use_coupon) #4
    '''for item in can_use_coupon:
        coupons = Coupon.query.filter_by(coupon_id=item.coupon_id).all()
        if coupons:
            can_use_coupon_list.extend(coupons)
    '''
    for item in can_use_coupon:
        coupons = Coupon.query.filter_by(coupon_id=item.coupon_id).all()
        if coupons:
            for coupon in coupons:
                if coupon.expire_date > current_time.date():
                    can_use_coupon_list.append(coupon)
    print(can_use_coupon_list) #5
    return can_use_coupon_list


def query_coupon(use_coupon_order):
    coupon_list = []
    for item in use_coupon_order:
        coupons = Coupon.query.filter_by(coupon_id=item.coupon_id).all()
        if coupons:
            coupon_list.extend(coupons)
    print(coupon_list)
    return coupon_list

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wei110590055@localhost/database' #Aa0988156955的部分改成你自己資料庫的密碼
app.config['SECRET_KEY'] = "my secret key in my flask website"
app.config['UPLOAD_FOLDER'] = '/upload_files'

db.init_app(app)
#migrate =Migrate(app, db)
with app.app_context():
    db.create_all()

Login_Manager = LoginManager()
Login_Manager.init_app(app)
Login_Manager.login_view = 'login'
#Login_Manager.login_view = 'sign_in'

@Login_Manager.user_loader
def load_user(id):
    return Member.query.get(int(id))

@app.route("/")
def index():
    #random_products = query_all_products()
    products = query_all_products()
    # 假设这是要渲染的产品数量
    desired_length = 8
    if len(products) < desired_length:
        products += [None] * (desired_length - len(products))
    cart_with_product_info = query_all_car()
    car_count = len(cart_with_product_info)
    return render_template('index.html', products=products , count = car_count, base64 = base64)

@app.route("/sign_up", methods = ['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    isSignUp = False
    if form.validate_on_submit():
        sign_up = Customer.query.filter_by(email = form.email.data).first()
        if sign_up == None:
            sign_up = Customer(name = form.name.data, email = form.email.data, birthday = form.birthday.data, password = form.password.data)
            db.session.add(sign_up)
            db.session.commit()
            sign_up_car = Car(customer_id = sign_up.member_id)
            db.session.add(sign_up_car)
            db.session.commit()
            flash(f"Account sign up successfully. Hello! {form.name.data}.")
            isSignUp = True
        else:
            flash("This account is already exist, try to sign in.")
        form.name.data = ''
        form.email.data = ''
        form.birthday.data = ''
        form.password.data = ''
        form.password_check.data = ''
    return render_template('sign_up.html', form = form, isSignUp = isSignUp)

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    isLogIn = False
    form = SignInForm()
    if form.validate_on_submit():
        user_data = Member.query.filter_by(email = form.email.data).first()
        if user_data == None:
            flash("The email does'n exist, please try again")
            return redirect(url_for('sign_in'))
        else:
            passed = user_data.verify_password(form.password.data)
            if not passed:
                flash('Password is incorrect, please try again.')
                return redirect(url_for('sign_in'))
            else:
                #account_type = user_data.account_type
                login_user(user_data) 
                #flash('sign in successfully.') 
                return redirect(url_for('index'))
    return render_template('sign_in.html', form = form, isLogIn = isLogIn)

@app.route("/sign_out", methods=['GET', 'POST'])
@login_required
def sign_out():
    logout_user()
    flash("You've been Sign out successfully.")
    return redirect(url_for('sign_in'))

@app.route("/business_sign_up", methods = ['GET', 'POST'])
def bussiness_sign_up():
    form = BusinessSignUpForm()
    isSignUp = False
    if form.validate_on_submit():
        sign_up = Business.query.filter_by(email = form.email.data).first()
        if sign_up == None:
            sign_up = Business(name = form.name.data, email = form.email.data, birthday = form.birthday.data, password = form.password.data)
            db.session.add(sign_up)
            db.session.commit()
            flash(f"Account sign up successfully. Hello! {form.name.data}.")
            isSignUp = True
        else:
            flash("This account is already exist, try to sign in.")
        form.name.data = ''
        form.email.data = ''
        form.birthday.data = ''
        form.password.data = ''
        form.password_check.data = ''
    return render_template('business_sign_up.html', form = form, isSignUp = isSignUp)

@app.route("/delete_user")
@login_required
def delete_user():
    return render_template('delete_user.html')

@app.route("/delete")
@login_required
def delete():
    try:
        user_id = current_user.member_id
        logout_user()
        user = Member.query.filter_by(member_id = user_id).first()
        #delete error
        if user != None:
            db.session.delete(user)
            db.session.commit()
            flash("Account delete successfully.")
    except:
        flash("Delete Account error.")
    return redirect(url_for("index"))

#Feng Change
@app.route("/item_page/<int:id>", methods = ['GET', 'POST'])
def item(id):
    item = Product.query.get_or_404(id)
    total_sale = query_toal_sale(id)
    #path_for_html = item.image.decode("utf-8").replace("\\", "/")
    return render_template('item_page.html', id = id, item = item, base64 = base64 , total_sale = total_sale)
#, seller = seller上一行的

@app.route("/add_to_cart/<int:item_id>", methods=['GET'])
def add_to_cart(item_id):
    # 創建一個 ShoppingCart 物件並將商品ID添加到購物車
    new_cart_item = CarHaveProduct.query.filter_by(product_id=item_id , customer_id = current_user.member_id).first()
    if new_cart_item == None:
        new_cart_item = CarHaveProduct(product_id=item_id , customer_id = current_user.member_id, amount = 1)
        db.session.add(new_cart_item)
    else:
        new_cart_item.amount += 1
    db.session.commit()
    return redirect('/car')  # 將用戶重定向到購物車頁面

@app.route("/car", methods=['GET', 'POST'])
def car():
    # ... 其他逻辑 ...
    cars_product = query_all_car()
    car_price , car_amount = calculate_total_price(cars_product)
    can_use_coupon_list = find_can_use_coupon()
    # 在这里将 current_user 传递给模板
    return render_template('car.html', cars = cars_product, car_price = car_price, car_amount = car_amount, base64 = base64, can_use_coupon_list = can_use_coupon_list)

@app.route("/update_amount/<int:product_id>/<int:change>", methods=['GET', 'POST'])
def update_amount(product_id, change):
    if current_user.is_authenticated:
        total_sale = query_toal_sale(product_id)
        product_amount = Product.query.filter_by(product_id = product_id).first().quantity
        cart_item = CarHaveProduct.query.filter_by(
            product_id=product_id, customer_id=current_user.member_id).first()
        print(f"cart_item: {cart_item}")
        if cart_item:
            print(f"Current amount: {cart_item.amount}, Change: {change}")
            if change == 1:
                cart_item.amount += change
                if (product_amount - total_sale) < cart_item.amount:
                    cart_item.amount = product_amount - total_sale
            else:
                cart_item.amount -= 1
                if cart_item.amount == 0:
                    db.session.delete(cart_item)
            db.session.commit()
            print(f"Updated amount: {cart_item.amount}")
            return "OK", 200
    print("Error: Cart item not found or user not authenticated")
    return "Error", 400

@app.route("/delete_amount/<int:product_id>", methods=['GET', 'POST'])
def delete_amount(product_id):
    print(f"Attempting to delete product with ID: {product_id}")
    if current_user.is_authenticated:
        print(f"User authenticated: {current_user}")
        cart_item = CarHaveProduct.query.filter_by(product_id=product_id, customer_id=current_user.member_id).first()
        print(f"Cart item found: {cart_item}")
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            print("Item deleted successfully")
            return "ok", 200
        else:
            print("Cart item not found")
    else:
        print("User not authenticated")
    print("Error: Cart item not found or user not authenticated")
    return "Error", 400

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    selected_coupon = request.args.get('coupon')
    print(selected_coupon)
    cars_product = query_all_car()
    current_date = datetime.now()
    new_order = Order(customer_id = current_user.member_id, date = current_date)
    db.session.add(new_order)
    db.session.commit()
    if selected_coupon and selected_coupon != '-1':
        use_coupon = OrderUseCoupon(order_id = new_order.order_id , coupon_id = selected_coupon)
        db.session.add(use_coupon)
        db.session.commit()
    for cart_item in cars_product:
        product = cart_item["product"]
        amount = cart_item["amount"]
        new_Order_Have_Product = OrderHaveProduct(order_id = new_order.order_id , product_id = product.product_id , amount = amount)
        db.session.add(new_Order_Have_Product)
        db.session.commit()
    # 清空购物车数据
    CarHaveProduct.query.filter_by(customer_id=current_user.member_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/orderHistory", methods=['GET', 'POST'])
def orderHistory():
    order_list = query_all_order()
    print(order_list)
    order_have_product_list = []
    for order in order_list:
        order_have_product_list.append(query_order_have_product(order.order_id))
    price = 0
    amount = 0
    car_price = [] 
    car_amount = []
    for i in range(0, len(order_list)):
        for j in range(0, len(order_have_product_list[i])):
            price += order_have_product_list[i][j][0].money * order_have_product_list[i][j][1]
            amount += order_have_product_list[i][j][1]
        car_amount.append(amount)
        car_price.append(price)
        amount = 0
        price = 0
    use_coupon_order = (db.session.query(OrderUseCoupon)
    .join(Order, OrderUseCoupon.order_id == Order.order_id) 
    .join(Coupon, OrderUseCoupon.coupon_id == Coupon.coupon_id) 
    .filter(Order.customer_id == current_user.member_id) 
    .all()
    )
    print(use_coupon_order)
    coupon_list = query_coupon(use_coupon_order)
    return render_template('orderHistory.html', order_list = order_list, order_have_product_list = order_have_product_list, car_price = car_price , car_amount = car_amount, base64 = base64, use_coupon_order = use_coupon_order, coupon_list = coupon_list)

@app.context_processor
def inject_data():
    account_type = None
    if current_user.is_authenticated:
        member_id = Member.query.filter(Member.name == current_user.name).first().member_id
        account_type = Member.query.filter(Member.name == current_user.name).first().account_tpye
    return dict(current_user_account_type=account_type)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/add_product", methods=['GET', 'POST'])
@login_required
def add_product():
    user = current_user
    if(user.account_tpye != 1):
        return redirect(url_for('index'))
    form = ProductForm()
    if form.validate_on_submit() and form.image.data:
        product = Product(business_id = current_user.member_id, name = form.name.data, money = form.money.data, quantity = form.quantity.data, detail = form.detail.data, image = form.image.data.read(), publish_date = datetime.now())
        db.session.add(product)
        db.session.commit()
        form.name.data = ''
        form.money.data = 0
        form.quantity.data = 0
        form.detail.data = ''
        form.image.data = ''
        flash("Add Product successfully.")
    else:
        flash("Add Product failed, please try again.")
    return render_template("add_product.html", form = form)

@app.route("/product_list", methods=['GET', 'POST'])
@login_required
def product_list():
    user_id = current_user.member_id
    products = Product.query.filter_by(business_id = user_id).all()
    return render_template("product_list.html", products = products, base64 = base64)

@app.route("/edit_product/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.filter_by(product_id = id).first()
    if not product:
        return redirect(url_for('page_not_found'))
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.money = form.money.data
        product.quantity = form.quantity.data
        product.detail = form.detail.data
        if form.image.data:
            product.image = form.image.data.read()
        print(f"from money:{form.money.data}")
        print(f"product money:{product.money}")
        db.session.commit()
        flash("Edit Product successfully.")
        return redirect(url_for('product_list'))
    else:
        flash("Edit Product failed.")
    form.name.data = product.name
    form.money.data = product.money
    form.quantity.data = product.quantity
    form.detail.data = product.detail
    return render_template("edit_product.html", form = form, id = id)

@app.route("/delete_product/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = Product.query.filter_by(product_id = id).first()
    if not product:
        return redirect(url_for('page_not_found'))
    else:
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('product_list'))

@app.route("/start_chat/<int:id>", methods=['GET', 'POST'])
@login_required
def start_chat(id):
    '''
    business = Business.query.filter_by(member_id = id).first()
    user = Customer.query.filter_by(member_id = current_user.member_id).first()
    if user == None or business == None:
        return redirect(url_for('page_not_found'))
    '''
    business = Business.query.get_or_404(id)
    user = Customer.query.get_or_404(current_user.member_id)
    have_chat = ChatContainer.query.filter(and_(ChatContainer.business_id == business.member_id, ChatContainer.customer_id == user.member_id)).first()
    if have_chat != None:
        return redirect(url_for('chat_list', id = have_chat.chat_id))
    else:
        chat_container = ChatContainer(customer_id = user.member_id, business_id = id)
        db.session.add(chat_container)
        db.session.commit()
    return redirect(url_for('chat_list', id = chat_container.chat_id))

'''
'''
class chat_user_info():
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id

@app.route("/chat_list/<int:id>", methods=['GET', 'POST'])
@login_required
def chat_list(id):
    #return render_template("chat_list_old.html")
    user = current_user
    chat_users = ChatContainer.query.filter(or_(ChatContainer.customer_id == user.member_id, ChatContainer.business_id == user.member_id)).all()
    users_info = []
    form = ChatForm()
    if form.validate_on_submit():
        new_chat = Chat(container_id = id, owner_id = user.member_id, date = datetime.now(), text = form.message.data)
        db.session.add(new_chat)
        db.session.commit()
        form.message.data = ''
    chats = Chat.query.filter_by(container_id = id).all()
    if user.member.account_tpye == 0:
        for chat_user in chat_users:
            temp_business = Business.query.filter_by(member_id = chat_user.business_id).first()
            users_info.append(chat_user_info(name = temp_business.name, chat_id = chat_user.chat_id))
    else:
        for chat_user in chat_users:
            temp_customer = Customer.query.filter_by(member_id = chat_user.customer_id).first()
            users_info.append(chat_user_info(name = temp_customer.name, chat_id = chat_user.chat_id))

    return render_template("chat_list.html", form = form, users_info = users_info, user = user, messages = chats, chat_id = id)

@app.route("/admin/singup")
def admins_sing_up():
    admin_password = '123456'
    hashed_password = generate_password_hash(admin_password)
    
    admin = Administrator(
        email='admin@shop.com',
        password_hash=hashed_password,
        name='Admin',
        birthday=date(1990, 1, 1),
        account_tpye=2
    )
    
    # 其他代码...
    
    db.session.add(admin)
    db.session.commit()
    return render_template('index.html')

@app.route("/create_coupon", methods=['GET', 'POST'])
def create_coupon():
    form = CreateCouponForm()
    if form.validate_on_submit():
        new_coupon = Coupon(expire_date = form.expire_date.data , discount = form.discount.data, administrator_id = current_user.member_id)
        db.session.add(new_coupon)
        db.session.commit()
        customer_list = query_all_customer()
        for customer in customer_list:
            add_to_customer = CustomerHaveCoupon(coupon_id = new_coupon.coupon_id, customer_id = customer.member_id)
            db.session.add(add_to_customer)
            db.session.commit()
        return redirect('/')
    else:
        print(form.errors)  # 打印验证失败的信息
    return render_template('create_coupon.html', form = form)

@app.route('/get_discount/<int:coupon_id>')
def get_discount(coupon_id):
    # 假设 Coupon 是你的优惠券模型，discount 是优惠券的折扣属性
    coupon = Coupon.query.filter_by(coupon_id=coupon_id).first()
    if coupon:
        return jsonify({'discount': coupon.discount})
    else:
        return jsonify({'discount': 0})  # 如果未找到优惠券，可以返回默认的折扣值或其他信息

if __name__ == '__main__':
    app.run(debug=True)