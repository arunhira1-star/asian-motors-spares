
from flask import Flask, request

app = Flask(__name__)

ADMIN_PASSWORD = "asian123"

products = [
{"name":"Jeep Headlight","part":"68214344AA","price":"7500","stock":"5"},
{"name":"Jeep Brake Pad","part":"68192451AB","price":"3200","stock":"10"},
{"name":"Fiat Air Filter","part":"51977574","price":"900","stock":"15"}
]

requests=[]

cart=[]


@app.route("/")
def store():

    search=request.args.get("search","")

    html="""

    <h1>🚗 Asian Motors Spares</h1>

    <a href="/cart">Cart</a> |
    <a href="/upload">Upload Part Photo</a> |
    <a href="/login">Admin</a>

    <br><br>

    <form>

    <input name="search" placeholder="Search Part Number">

    <button>Search</button>

    </form>

    <h2>Parts Catalogue</h2>

    """

    for p in products:

        if search and search not in p["part"]:
            continue

        html+=f"""

        <div style="border:1px solid #ddd;padding:10px;margin:10px">

        <h3>{p['name']}</h3>

        <p>Part No: {p['part']}</p>

        <p>Price: ₹{p['price']}</p>

        <a href="/add/{p['part']}">Add to Cart</a>

        </div>

        """

    return html


@app.route("/add/<part>")
def add(part):

    for p in products:
        if p["part"]==part:
            cart.append(p)

    return "Added to cart <br><a href='/'>Back</a>"


@app.route("/cart")
def cart_page():

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
        "phone":request.form["phone"],
        "part":request.form["part"],
        "image":request.form["image"]

        })

        return "Request sent for verification"

    return """

    <h2>Upload Part Photo</h2>

    <form method="post">

    Your Name<br>
    <input name="name"><br>

    Phone<br>
    <input name="phone"><br>

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


@app.route("/admin")
def admin():

    html="<h1>Admin Panel</h1>"

    html+="<h2>Customer Requests</h2>"

    for r in requests:

        html+=f"""

        <div style="border:1px solid #ddd;padding:10px;margin:10px">

        Name: {r['name']}<br>
        Phone: {r['phone']}<br>
        Part: {r['part']}<br>
        Image: {r['image']}<br>

        </div>

        """

    html+="<br><a href='/'>Back</a>"

    return html


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
