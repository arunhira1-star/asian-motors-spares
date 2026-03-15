from flask import Flask,request,redirect
import random

app = Flask(__name__)

ADMIN_USER="admin"
ADMIN_PASS="AMS986412"

products=[]
brands=["Maruti","Hyundai","Tata","Mahindra","Jeep"]
models=["Swift","Baleno","i20","Nexon","Compass"]

for i in range(1,301):

    products.append({

    "id":i,
    "name":f"Car Spare Part {i}",
    "brand":random.choice(brands),
    "model":random.choice(models),
    "part":f"OEM{i}",
    "price":random.randint(500,5000)

    })

cart=[]
orders=[]
users=[]
services=[]

theme="light"
language="English"

# ---------------- STORE ----------------

@app.route("/")
def store():

    html=f"""

<h1>🚗 Asian Motors Spares</h1>

<a href="/cart">Cart</a> |
<a href="/login">Customer Login</a> |
<a href="/settings">Settings</a> |
<a href="/track">Track Order</a> |
<a href="/dashboard">Admin</a>

<br><br>

<form>

Search Part
<input name="search">

<button>Search</button>

</form>

"""

    search=request.args.get("search","")

    for p in products:

        if search and search not in p["part"]:
            continue

        html+=f"""

<hr>

<h3>{p['name']}</h3>

Brand: {p['brand']}<br>
Model: {p['model']}<br>
Part: {p['part']}<br>

Price: ₹{p['price']}<br>

<a href="/add/{p['id']}">Add to Cart</a>

"""

    return html


# ---------------- CART ----------------

@app.route("/add/<int:id>")
def add(id):

    for p in products:
        if p["id"]==id:
            cart.append(p)

    return redirect("/cart")


@app.route("/cart",methods=["GET","POST"])
def cart_page():

    total=0
    html="<h2>Cart</h2>"

    for c in cart:

        html+=f"{c['name']} ₹{c['price']}<br>"
        total+=c["price"]

    if request.method=="POST":

        order_id=len(orders)+1

        orders.append({

        "id":order_id,
        "name":request.form["name"],
        "phone":request.form["phone"],
        "address":request.form["address"],
        "payment":request.form["payment"],
        "status":"Processing"

        })

        return f"Order placed successfully. Your Order ID: {order_id}"

    html+=f"""

<h3>Total ₹{total}</h3>

<form method="post">

Name<br>
<input name="name"><br>

Phone<br>
<input name="phone"><br>

Address<br>
<textarea name="address"></textarea><br>

Payment Method<br>

<select name="payment">

<option>UPI</option>
<option>Cash on Delivery</option>
<option>Card</option>

</select>

<button>Place Order</button>

</form>

"""

    return html


# ---------------- LOGIN ----------------

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        users.append({

        "name":request.form["name"],
        "phone":request.form["phone"]

        })

        return redirect("/")

    return """

<h2>Customer Login</h2>

<form method="post">

Name<br>
<input name="name"><br>

Phone<br>
<input name="phone"><br>

<button>Login</button>

</form>

"""


# ---------------- DELIVERY TRACKING ----------------

@app.route("/track",methods=["GET","POST"])
def track():

    if request.method=="POST":

        oid=int(request.form["id"])

        for o in orders:

            if o["id"]==oid:

                return f"""

Order ID: {o['id']}<br>
Status: {o['status']} 🚚

"""

        return "Order not found"

    return """

<h2>Track Delivery</h2>

<form method="post">

Order ID<br>
<input name="id"><br>

<button>Track</button>

</form>

"""


# ---------------- SETTINGS ----------------

@app.route("/settings",methods=["GET","POST"])
def settings():

    global theme
    global language

    if request.method=="POST":

        theme=request.form["theme"]
        language=request.form["language"]

        return "Settings updated"

    return f"""

<h2>Settings</h2>

<form method="post">

Theme<br>

<select name="theme">

<option>light</option>
<option>dark</option>

</select>

Language<br>

<select name="language">

<option>English</option>
<option>Hindi</option>

</select>

<button>Save</button>

</form>

"""


# ---------------- SERVICE ----------------

@app.route("/service",methods=["GET","POST"])
def service():

    if request.method=="POST":

        services.append({

        "name":request.form["name"],
        "phone":request.form["phone"],
        "car":request.form["car"],
        "service":request.form["service"]

        })

        return "Service booked"

    return """

<h2>Mechanic Service Booking</h2>

<form method="post">

Name<br>
<input name="name"><br>

Phone<br>
<input name="phone"><br>

Car Model<br>
<input name="car"><br>

Service<br>

<select name="service">

<option>General Service</option>
<option>Engine Repair</option>
<option>Brake Repair</option>

</select>

<button>Book Service</button>

</form>

"""


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():

    if request.method=="POST":

        if request.form["user"]==ADMIN_USER and request.form["pass"]==ADMIN_PASS:

            html="<h1>Admin Dashboard</h1>"

            html+=f"Total Orders: {len(orders)}<br>"
            html+=f"Customers: {len(users)}<br>"
            html+=f"Service Bookings: {len(services)}<br>"

            html+="<h3>Orders</h3>"

            for o in orders:

                html+=f"{o['id']} | {o['name']} | {o['status']}<br>"

            return html

        else:

            return "Wrong password"

    return """

<h2>Admin Login</h2>

<form method="post">

User<br>
<input name="user"><br>

Password<br>
<input name="pass"><br>

<button>Login</button>

</form>

"""


if __name__=="__main__":

    app.run(host="0.0.0.0",port=10000)
