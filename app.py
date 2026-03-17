from flask import Flask, request, redirect
import random

app = Flask(__name__)

# -----------------
# PRODUCTS 10000+
# -----------------

products=[]
brands=["Maruti","Hyundai","Tata","Mahindra","Jeep"]

for i in range(1,10001):

    products.append({

    "id":i,
    "name":f"Car Spare Part {i}",
    "brand":random.choice(brands),
    "part":f"OEM{i}",
    "price":random.randint(500,5000)

    })

cart=[]
orders=[]
services=[]
users=[]

# -----------------
# LOGO (BASE64 IMAGE)
# -----------------

logo_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."


# -----------------
# HOME PAGE
# -----------------

@app.route("/")
def home():

    search=request.args.get("search","")

    html=f"""

<style>

body{{font-family:Arial;margin:0;background:#f1f3f6}}

header{{
background:#2874f0;
padding:15px;
display:flex;
align-items:center;
justify-content:space-between;
color:white
}}

.logo{{height:60px}}

.search{{padding:8px;width:400px}}

.products{{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:20px;
padding:20px
}}

.card{{
background:white;
padding:10px;
border-radius:6px;
box-shadow:0 0 5px gray
}}

button{{
background:#fb641b;
color:white;
border:none;
padding:8px;
}}

</style>

<header>

<div style="display:flex;align-items:center">

<img src="{logo_data}" class="logo">

<h2 style="margin-left:10px">Asian Motors Spares</h2>

</div>

<form>

<input name="search" class="search" placeholder="Search car parts">

</form>

<div>

<a href="/account">My Account</a> |
<a href="/cart">Cart</a> |
<a href="/settings">Settings</a>

</div>

</header>

<h2 style="padding:20px">

Welcome to our store (Asian Motors Spares)

</h2>

<div class="products">

"""

    for p in products[:80]:

        if search and search not in p["part"]:
            continue

        html+=f"""

<div class="card">

<h4>{p['name']}</h4>

Brand: {p['brand']}<br>

Part: {p['part']}<br>

<h3>₹{p['price']}</h3>

<a href="/add/{p['id']}">

<button>Add to Cart</button>

</a>

</div>

"""

    html+="</div>"

    return html


# -----------------
# CART
# -----------------

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

        oid=len(orders)+1

        orders.append({

        "id":oid,
        "status":"Shipped"

        })

        return f"Order placed. Order ID {oid}"

    html+=f"""

<h3>Total ₹{total}</h3>

<form method="post">

Name<br>
<input name="name"><br>

Address<br>
<textarea name="address"></textarea><br>

<button>Place Order</button>

</form>

"""

    return html


# -----------------
# ACCOUNT
# -----------------

@app.route("/account",methods=["GET","POST"])
def account():

    if request.method=="POST":

        users.append({

        "name":request.form["name"],
        "phone":request.form["phone"]

        })

        return redirect("/")

    return """

<h2>My Account</h2>

<form method="post">

Name<br>
<input name="name"><br>

Phone<br>
<input name="phone"><br>

<button>Save</button>

</form>

"""


# -----------------
# DELIVERY TRACKING
# -----------------

@app.route("/track",methods=["GET","POST"])
def track():

    if request.method=="POST":

        oid=int(request.form["id"])

        for o in orders:

            if o["id"]==oid:

                return """

<h2>Order Tracking</h2>

Order Placed ✔<br>
Packed ✔<br>
Shipped 🚚<br>
Out for Delivery<br>
Delivered

"""

        return "Order not found"

    return """

<h2>Track Order</h2>

<form method="post">

Order ID<br>
<input name="id"><br>

<button>Track</button>

</form>

"""


# -----------------
# MECHANIC BOOKING
# -----------------

@app.route("/mechanic",methods=["GET","POST"])
def mechanic():

    if request.method=="POST":

        services.append({

        "name":request.form["name"],
        "car":request.form["car"]

        })

        return "Mechanic booked"

    return """

<h2>Mechanic Service Booking</h2>

<form method="post">

Name<br>
<input name="name"><br>

Car Model<br>
<input name="car"><br>

<button>Book</button>

</form>

"""


# -----------------

if __name__=="__main__":

    app.run(host="0.0.0.0",port=10000)
