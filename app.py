
from flask import Flask, request

app = Flask(__name__)

ADMIN_PASSWORD = "asian123"

products = [
{"name":"Jeep Headlight","part":"68214344AA","brand":"Jeep","model":"Compass","price":"7500","stock":"5"},
{"name":"Brake Pad","part":"68192451AB","brand":"Jeep","model":"Compass","price":"3200","stock":"10"},
{"name":"Air Filter","part":"51977574","brand":"Fiat","model":"Punto","price":"900","stock":"15"}
]

cart=[]
orders=[]
requests=[]

@app.route("/")
def store():

    search=request.args.get("search","")
    brand=request.args.get("brand","")
    model=request.args.get("model","")

    html="""

<style>

body{font-family:Arial;margin:0;background:#f1f3f6}

header{
background:#2874f0;
color:white;
padding:15px;
display:flex;
align-items:center;
gap:15px
}

.products{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:20px;
padding:20px
}

.card{
background:white;
padding:15px;
border-radius:8px;
box-shadow:0 0 10px rgba(0,0,0,0.1)
}

button{
background:#fb641b;
color:white;
border:none;
padding:10px;
cursor:pointer
}

a{color:white;margin-left:10px}

</style>

<header>

<img src="logo.png" height="50">

<h2>Asian Motors Spares</h2>

<form>

<input name="search" placeholder="Search part number">

<select name="brand">

<option value="">Brand</option>
<option>Jeep</option>
<option>Fiat</option>

</select>

<select name="model">

<option value="">Model</option>
<option>Compass</option>
<option>Punto</option>

</select>

<button>Search</button>

</form>

<div>

<a href="/cart">Cart</a>
<a href="/upload">Upload</a>
<a href="/login">Admin</a>
<a href="/dashboard">Dashboard</a>

</div>

</header>

<div class="products">

"""

    for p in products:

        if search and search not in p["part"]:
            continue

        if brand and brand!=p["brand"]:
            continue

        if model and model!=p["model"]:
            continue

        html+=f"""

<div class="card">

<h3>{p['name']}</h3>

<p>Brand: {p['brand']}</p>

<p>Model: {p['model']}</p>

<p>Part: {p['part']}</p>

<p>₹{p['price']}</p>

<a href="/add/{p['part']}"><button>Add to Cart</button></a>

</div>

"""

    html+="</div>"

    return html


@app.route("/add/<part>")
def add(part):

    for p in products:
        if p["part"]==part:
            cart.append(p)

    return "Added to cart <br><a href='/'>Back</a>"


@app.route("/cart")
def view_cart():

    total=0
    html="<h1>Cart</h1>"

    for c in cart:
        html+=f"{c['name']} ₹{c['price']}<br>"
        total+=int(c["price"])

    html+=f"<h3>Total ₹{total}</h3>"

    html+=f"""

<a href="upi://pay?pa=9864126916@upi&pn=AsianMotorsSpares&am={total}&cu=INR">

Pay with UPI

</a>

"""

    return html


@app.route("/upload",methods=["GET","POST"])
def upload():

    if request.method=="POST":

        requests.append({

        "name":request.form["name"],
        "part":request.form["part"],
        "image":request.form["image"]

        })

        return "Request sent"

    return """

<h2>Upload Part Photo</h2>

<form method="post">

Name<br>
<input name="name"><br>

Part Number<br>
<input name="part"><br>

Image URL<br>
<input name="image"><br><br>

<button>Submit</button>

</form>

"""


@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        if request.form["password"]==ADMIN_PASSWORD:
            return admin()

        else:
            return "Wrong password"

    return """

<h2>Admin Login</h2>

<form method="post">

Password<br>
<input type="password" name="password"><br><br>

<button>Login</button>

</form>

"""


@app.route("/admin",methods=["GET","POST"])
def admin():

    if request.method=="POST":

        products.append({

"name":request.form["name"],
"part":request.form["part"],
"brand":request.form["brand"],
"model":request.form["model"],
"price":request.form["price"],
"stock":request.form["stock"]

})

    html="""

<h1>Admin Panel</h1>

<form method="post">

Name<br>
<input name="name"><br>

Part No<br>
<input name="part"><br>

Brand<br>
<input name="brand"><br>

Model<br>
<input name="model"><br>

Price<br>
<input name="price"><br>

Stock<br>
<input name="stock"><br><br>

<button>Add Product</button>

</form>

"""

    html+="<h2>Customer Requests</h2>"

    for r in requests:

        html+=f"{r['name']} - {r['part']} - {r['image']}<br>"

    return html


@app.route("/dashboard")
def dashboard():

    return f"""

<h1>Sales Dashboard</h1>

Total Products: {len(products)}<br>

Orders: {len(orders)}<br>

Cart Items: {len(cart)}<br>

<a href="/">Back</a>

"""


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
