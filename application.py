from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

#initialize the application
app = Flask(__name__)

#showing debug messages
app.config["DEBUG"] = True

#initiliaze the SQL DATABASE connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


#user model
class User( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    address = db.Column(db.String(100))
    bio = db.Column(db.Text())
    username = db.Column(db.String(10))
    password = db.Column(db.String(20))
    # relationships
    orders = db.relationship( "Order", backref="user" )
    reviews = db.relationship( "Reviews", backref="user" )

    def __init__(self, fname, lname, address, bio, username, password):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.bio = bio
        self.username = username
        self.password = password

 #order model
class Order( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    order_type = db.Column(db.String(100))
    status = db.Column(db.String(100))

    # relationships
    users = db.relationship( "User", backref="order" )
    products = db.relationship( "Proudct", backref="order" )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, quantity, order_type, status):
        self.quantity = quantity
        self.order_type = order_type
        self.status = status


class Product( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    flavor = db.Column(db.Text())
    price = db.Column(db.Float)

    # relationships
    orders = db.relationship( "Order", backref="product" )
    reviews = db.relationship( "Reviews", backref="product" )

    def __init__(self, name, description, flavor, price):
        self.name = name
        self.description = description
        self.flavor = flavor
        self.price = price

class Reviews( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(100))
    comment = db.Column(db.String(100))
    stars = db.Column(db.Text())

    # relationships
    users = db.relationship( "User", backref="reviews" )
    products = db.relationship( "Proudct", backref="reviews" )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __init__(self, tittle, comment, stars):
        self.tittle = tittle
        self.comment = comment
        self.stars = stars

#MAIN ROUTES

@app.route("/")
def home():
    return render_template("index.html")









# CRUDI - Users Controller

@app.route("/users")
def all_users():
    allUsers = User.query.all()
    return render_template("users.html", users = allUsers)

@app.route("/users/create", methods=["POST"])
def create_user():
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    address = request.form.get('address', "")
    bio = request.form.get('bio', "")
    username = request.form.get('username', "")
    password = request.form.get('password', "")

    newUser = User(fname, lname, address, bio, username, password)
    db.session.add(newUser)
    db.session.commit()

    return redirect("/users/")

@app.route("/users/<id>")
def get_user(id):
    user = User.query.get( int(id) )
    return render_template("user.html", user = user)

@app.route("/users/<id>/edit", methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get( int(id) )

    if request == "Post":
        user.fname = request.form.get('fname', "")
        user.lname = request.form.get('lname', "")
        user.address = request.form.get('address', "")
        user.bio = request.form.get('bio', "")
        user.password = request.form.get('password', "")
        db.session.commit()
        return render_template("user.html", user = user)
    else:
        return render_template("edit_user.html", user = user)

@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get( int(id) )
    db.session.delete(user)
    db.session.commit()
    return redirect("users")

#C.R.U.D.I -Orders Controller

@app.route("/orders")
def all_orders():
    allOrders = Order.query.all()
    return render_template("orders.html", orders = allOrders)

@app.route("/orders/create", methods=["POST"])
def create_order():
    quantity = request.form.get('quantity', "")
    order_type = request.form.get('order_type', "")
    status = request.form.get('status', "")


    newOrder = Order(quantity, order_type, status)
    db.session.add(newOrder)
    db.session.commit()

    return redirect("/orders/")

@app.route("/orders/<id>")
def get_order(id):
    order = Order.query.get( int(id) )
    return render_template("order.html", order = order)

@app.route("/orders/<id>/edit", methods=["GET", "POST"])
def edit_order(id):
    order = Order.query.get( int(id) )

    if request == "Post":
        order.quantity = request.form.get('quantity', "")
        order.order_type = request.form.get('order_type', "")
        order.status = request.form.get('status', "")
        db.session.commit()
        return render_template("order.html", order = order)
    else:
        return render_template("edit_order.html", order = order)

@app.route("/orders/<id>/delete", methods=["POST"])
def delete_order(id):
    order = Order.query.get( int(id) )
    db.session.delete(order)
    db.session.commit()
    return redirect("orders")

#C.R.U.D.I - Product controller

@app.route("/products")
def all_products():
    allProducts = Product.query.all()
    return render_template("products.html", products = allProducts)

@app.route("/products/create", methods=["POST"])
def create_product():
    name = request.form.get('name', "")
    description = request.form.get('description', "")
    flavor = request.form.get('flavor', "")
    price = request.form.get('price', "")

    newProduct = Product(name, description, flavor, price)
    db.session.add(newProduct)
    db.session.commit()

    return redirect("/products/")

@app.route("/products/<id>")
def get_product(id):
    product = Product.query.get( int(id) )
    return render_template("product.html", product = product)

@app.route("/products/<id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get( int(id) )

    if request == "Post":
        product.name = request.form.get('name', "")
        product.description = request.form.get('description', "")
        product.flavor = request.form.get('flavor', "")
        product.price = request.form.get('price', "")
        db.session.commit()
        return render_template("product.html", product = product)
    else:
        return render_template("edit_product.html", product = product)

@app.route("/products/<id>/delete", methods=["POST"])
def delete_product(id):
    product = Product.query.get( int(id) )
    db.session.delete(product)
    db.session.commit()
    return redirect("product")

#C.R.U.D.I - Reviews Controller

@app.route("/reviews")
def all_reviews():
    allReviews = Reviews.query.all()
    return render_template("reviews.html", reviews = allReviews)

@app.route("/reviews/create", methods=["POST"])
def create_review():
    tittle = request.form.get('fname', "")
    comment = request.form.get('lname', "")
    stars = request.form.get('bio', "")


    newReview = Reviews(tittle, comment, stars)
    db.session.add(newReview)
    db.session.commit()

    return redirect("/reviews/")

@app.route("/reviews/<id>")
def get_review(id):
    review = Reviews.query.get( int(id) )
    return render_template("review.html", review = review)

@app.route("/reviews/<id>/edit", methods=["GET", "POST"])
def edit_review(id):
    review = Reviews.query.get( int(id) )

    if request == "Post":
        review.tittle = request.form.get('tittle', "")
        review.comment = request.form.get('comment', "")
        review.stars = request.form.get('stars', "")
        db.session.commit()
        return render_template("review.html", review = review)
    else:
        return render_template("edit_user.html", review = review)

@app.route("/reviews/<id>/delete", methods=["POST"])
def delete_review(id):
    review = Reviews.query.get( int(id) )
    db.session.delete(review)
    db.session.commit()
    return redirect("reviews")




if __name__ == "__main__":
    app.run()
