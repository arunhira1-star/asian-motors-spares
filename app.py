
from flask import Flask,request,redirect
import random

app = Flask(__name__)

# -------------------------
# ADMIN LOGIN
# -------------------------

ADMIN_USER="admin"
ADMIN_PASS="AMS986412"

# -------------------------
# SAMPLE PARTS DATABASE
# -------------------------

products=[]

brands={
"Maruti":["Swift","Baleno","Alto"],
"Hyundai":["i20","Creta","Verna"],
"Tata":["Nexon","Harrier","Punch"],
"Mahindra":["Scorpio","XUV700"],
"Jeep":["Compass"]
}

# generate 1000+ demo parts
for i in range(1,1001):

    brand=random.choice(list(brands.keys()))
    model=random.choice(brands[brand])

    products.append({

    "id":i,
    "name":f"{brand} {model} Part {i}",
    "brand":brand,
    "model":model,
    "part":f"OEM{i}XYZ",
    "price":random.randint(500,5000),
    "stock":random.randint(1,20),
    "rating":round(random.uniform(3,5),1)

    })

cart=[]
orders=[]
reviews=[]
users=[]

# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():

    brand=request.args.get("brand","")
    model=request.args.get("model","")
    search=request.args.get("search","")

    html="""

<style>

body{font-family:Arial;background:#f1f3f6;margin:0}

header{
background:#2874f0;
color:white;
padding:15px;
display:flex;
gap:10px;
align-items:center
}

.products{
display:grid;
grid-template-columns:repeat(4,1fr);
gap:20px;
padding:20px
}

.card{
background:white;
padding:10px;
border-radius:8px;
box-shadow:0 0 10px rgba(0,0,0,0.1)
}

button{
background:#fb641b;
color:white;
border:none;
padding:8px;
cursor:pointer
}

</style>

<header>

<h2>🚗 Asian Motors Spares</h2>

<form>

<input name="search" placeholder="Part number search">

<select name="brand">
<option value="">Brand</option>
<option>Maruti</option>
<option>Hyundai</option>
<option>Tata</option>
<option>Mahindra</option>
<option>Jeep</option>
</select>

<select name="model">
<option value="">Model</option>
<option>Swift</option>
<option>Baleno</option>
<option>i20</option>
<option>Nexon</option>
<option>Compass</option>
</select>

<button>Search</button>

</form>

<a href="/cart">Cart</a>
<a href="/login">Login</a>
<a href="/admin">Admin</a>
<a href="/dashboard">Dashboard</a>

</header>

<div class="products">

"""

    for p in products:

        if brand and brand!=p["brand"]:
            continue

        if model and model!=p["model"]:
            continue

        if search and search not in p["part"]:
            continue

        html+=f"""

<div class="card">

<h4>{p['name']}</h4>

<p>Brand: {p['brand']}</p>
<p>Model: {p['model']}</p>
<p>Part No: {p['part']}</p>

<p>⭐ {p['rating']}</p>

<h3>₹{p['price']}</h3>

<a href="/add/{p['id']}"><button>Add to Cart</button></a>

<a href="/review/{p['id']}"><button>Review</button></a>

</div>

"""

    html+="</div>"

    return html

# -------------------------
# CART
# -------------------------

@app.route("/add/<int:id>")
def add(id):

    for p in products:
        if p["id"]==id:
            cart.append(p)

    return redirect("/cart")

@app.route("/cart",methods=["GET","POST"])
def view_cart():

    total=0
    html="<h1>Cart</h1>"

    for c in cart:

        html+=f"{c['name']} ₹{c['price']}<br>"
        total+=c["price"]

    if request.method=="POST":

        orders.append({

        "name":request.form["name"],
        "phone":request.form["phone"],
        "address":request.form["address"],
        "payment":request.form["payment"],
        "status":"Processing"

        })

        return "Order placed successfully"

    html+=f"""

<h2>Total ₹{total}</h2>

<form method="post">

Name<br>
<input name="name"><br>

Phone<br>
<input name="phone"><br>

Address<br>
<textarea name="address"></textarea><br>

Payment<br>

<select name="payment">
<option>UPI</option>
<option>Cash on Delivery</option>
</select>

<button>Place Order</button>

</form>

"""

    html+=f"""

<h3>UPI Payment</h3>

<a href="upi://pay?pa=9864126916@upi&pn=AsianMotors&am={total}&cu=INR">
Pay via UPI
</a>

"""

    return html

# -------------------------
# CUSTOMER LOGIN
# -------------------------

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        users.append({
        "email":request.form["email"]
        })

        return redirect("/")

    return """

<h2>Customer Login</h2>

<form method="post">

Email<br>
<input name="email"><br>

<button>Login</button>

</form>

"""

# -------------------------
# REVIEW SYSTEM
# -------------------------

@app.route("/review/<int:id>",methods=["GET","POST"])
def review(id):

    if request.method=="POST":

        reviews.append({
        "product":id,
        "text":request.form["text"]
        })

        return "Review submitted"

    return """

<h2>Write Review</h2>

<form method="post">

<textarea name="text"></textarea>

<button>Submit</button>

</form>

"""

# -------------------------
# ADMIN PANEL
# -------------------------

@app.route("/admin",methods=["GET","POST"])
def admin():

    if request.method=="POST":

        if request.form["user"]==ADMIN_USER and request.form["pass"]==ADMIN_PASS:

            html="<h1>Admin Panel</h1>"

            html+=f"Total Orders: {len(orders)}<br>"
            html+=f"Total Users: {len(users)}<br>"

            html+="<h3>Orders</h3>"

            for o in orders:

                html+=f"{o['name']} | {o['address']} | {o['payment']} | {o['status']}<br>"

            return html

    return """

<h2>Admin Login</h2>

<form method="post">

User<br>
<input name="user"><br>

Pass<br>
<input name="pass"><br>

<button>Login</button>

</form>

"""

# -------------------------
# SALES DASHBOARD
# -------------------------

@app.route("/dashboard")
def dashboard():

    revenue=sum([p["price"] for p in cart])

    return f"""

<h1>Sales Dashboard</h1>

Total Products: {len(products)}<br>
Orders: {len(orders)}<br>
Users: {len(users)}<br>
Revenue: ₹{revenue}<br>

"""

# -------------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
