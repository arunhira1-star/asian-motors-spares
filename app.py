from flask import Flask,request,redirect
import random

app = Flask(__name__)

# -----------------------
# ADMIN
# -----------------------

ADMIN_USER="admin"
ADMIN_PASS="AMS986412"

# -----------------------
# PRODUCTS DATABASE
# -----------------------

products=[]

brands=["Maruti","Hyundai","Tata","Mahindra","Jeep"]
models=["Swift","Baleno","i20","Nexon","Compass"]

categories=[
"Engine","Brake","Electrical",
"Suspension","Filter","Body"
]

for i in range(1,301):

    products.append({

    "id":i,
    "name":f"Auto Part {i}",
    "brand":random.choice(brands),
    "model":random.choice(models),
    "category":random.choice(categories),
    "part":f"OEM{i}",
    "price":random.randint(500,5000),
    "supplier":"Default Supplier",
    "commission":10

    })

cart=[]
orders=[]
reviews=[]
suppliers=[]

# -----------------------
# STORE
# -----------------------

@app.route("/")
def store():

    search=request.args.get("search","")
    brand=request.args.get("brand","")
    category=request.args.get("category","")
    price=request.args.get("price","")

    html="""

<h1>🚗 Asian Motors Spares</h1>

<a href="/cart">Cart</a> |
<a href="/upload">Upload Part Photo</a> |
<a href="/track">Track Order</a> |
<a href="/supplier">Supplier</a>

<br><br>

<form>

Search
<input name="search">

Brand
<select name="brand">
<option value="">All</option>
<option>Maruti</option>
<option>Hyundai</option>
<option>Tata</option>
<option>Mahindra</option>
<option>Jeep</option>
</select>

Category
<select name="category">
<option value="">All</option>
<option>Engine</option>
<option>Brake</option>
<option>Electrical</option>
<option>Suspension</option>
<option>Filter</option>
<option>Body</option>
</select>

Max Price
<input name="price">

<button>Search</button>

</form>

<hr>

"""

    for p in products:

        if search and search.lower() not in p["name"].lower() and search not in p["part"]:
            continue

        if brand and brand!=p["brand"]:
            continue

        if category and category!=p["category"]:
            continue

        if price and p["price"]>int(price):
            continue

        html+=f"""

<h3>{p['name']}</h3>

Brand: {p['brand']}<br>
Category: {p['category']}<br>

Part No: {p['part']}<br>

Price: ₹{p['price']}<br>

Supplier: {p['supplier']}<br>

<a href="/add/{p['id']}">Add to Cart</a>

<a href="/review/{p['id']}">Review</a>

<hr>

"""

    return html


# -----------------------
# CART
# -----------------------

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

        return f"Order placed. Order ID: {order_id}"

    html+=f"""

<h3>Total ₹{total}</h3>

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
<option>Card</option>
</select>

<button>Place Order</button>

</form>

"""

    return html


# -----------------------
# DELIVERY TRACKING
# -----------------------

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

<h2>Track Order</h2>

<form method="post">

Order ID<br>
<input name="id"><br>

<button>Track</button>

</form>

"""


# -----------------------
# REVIEW
# -----------------------

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


# -----------------------
# AI PART DETECTION DEMO
# -----------------------

@app.route("/upload",methods=["GET","POST"])
def upload():

    if request.method=="POST":

        return """

Photo received.

AI detection: Unknown part (demo)

Please call us:

📞 9864126916

"""

    return """

<h2>Upload Part Photo</h2>

<form method="post">

Image URL<br>
<input name="photo"><br>

<button>Upload</button>

</form>

"""


# -----------------------
# SUPPLIER MARKETPLACE
# -----------------------

@app.route("/supplier",methods=["GET","POST"])
def supplier():

    if request.method=="POST":

        suppliers.append({

        "name":request.form["name"],
        "commission":request.form["commission"]

        })

        return "Supplier added"

    html="""

<h2>Supplier Marketplace</h2>

<form method="post">

Supplier Name<br>
<input name="name"><br>

Commission %<br>
<input name="commission"><br>

<button>Add Supplier</button>

</form>

<h3>Suppliers</h3>

"""

    for s in suppliers:

        html+=f"{s['name']} Commission: {s['commission']}%<br>"

    return html


# -----------------------

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
