
from flask import Flask, request

app = Flask(__name__)

products = [
{"name":"Jeep Headlight","part":"68214344AA","brand":"Jeep","model":"Compass","price":"7500","stock":"5"},
{"name":"Jeep Brake Pad","part":"68192451AB","brand":"Jeep","model":"Compass","price":"3200","stock":"10"},
{"name":"Fiat Air Filter","part":"51977574","brand":"Fiat","model":"Punto","price":"900","stock":"15"},
{"name":"Fiat Oil Filter","part":"55224598","brand":"Fiat","model":"Linea","price":"650","stock":"20"},
]

cart = []
orders = []

@app.route("/")
def store():

    search = request.args.get("search","")
    brand = request.args.get("brand","")
    model = request.args.get("model","")

    html = """

    <h1>🚗 Asian Motors Spares</h1>

    <a href="/admin">Admin Panel</a> |
    <a href="/dashboard">Sales Dashboard</a> |
    <a href="/cart">Cart</a>

    <br><br>

    <form>

    Search Part Number <br>
    <input name="search"><br><br>

    Brand <br>
    <select name="brand">
    <option value="">All</option>
    <option>Jeep</option>
    <option>Fiat</option>
    </select><br><br>

    Model <br>
    <select name="model">
    <option value="">All</option>
    <option>Compass</option>
    <option>Punto</option>
    <option>Linea</option>
    </select><br><br>

    <button>Search</button>

    </form>

    <h2>Spare Parts Catalogue</h2>

    """

    for p in products:

        if search and search not in p["part"]:
            continue

        if brand and brand != p["brand"]:
            continue

        if model and model != p["model"]:
            continue

        html += f"""

        <div style="border:1px solid #ddd;padding:10px;margin:10px;">

        <h3>{p['name']}</h3>

        <p>Brand: {p['brand']}</p>

        <p>Model: {p['model']}</p>

        <p>Part Number: {p['part']}</p>

        <p>Price: ₹{p['price']}</p>

        <p>Stock: {p['stock']}</p>

        <a href="/add/{p['part']}">Add to Cart</a>

        </div>

        """

    html += "<p>📞 Contact: 9864126916</p>"

    return html


@app.route("/add/<part>")
def add(part):

    for p in products:
        if p["part"] == part:
            cart.append(p)

    return "Added to cart <br><a href='/'>Back</a>"


@app.route("/cart")
def cart_page():

    html = "<h1>🛒 Cart</h1>"

    total = 0

    for c in cart:
        html += f"{c['name']} - ₹{c['price']}<br>"
        total += int(c["price"])

    html += f"<h3>Total: ₹{total}</h3>"

    html += "<a href='/checkout'>Checkout</a>"

    return html


@app.route("/checkout")
def checkout():

    total = 0

    for c in cart:
        total += int(c["price"])

    return f"""

    <h1>UPI Payment</h1>

    <p>Total Amount: ₹{total}</p>

    <a href="upi://pay?pa=9864126916@upi&pn=AsianMotorsSpares&am={total}&cu=INR">

    <button style="padding:10px;font-size:18px;">Pay with UPI</button>

    </a>

    <br><br>

    <a href="/">Back</a>

    """


@app.route("/admin", methods=["GET","POST"])
def admin():

    if request.method == "POST":

        name = request.form["name"]
        part = request.form["part"]
        brand = request.form["brand"]
        model = request.form["model"]
        price = request.form["price"]
        stock = request.form["stock"]

        products.append({

        "name":name,
        "part":part,
        "brand":brand,
        "model":model,
        "price":price,
        "stock":stock

        })

    return """

    <h1>👨‍💼 Admin Panel</h1>

    <form method="post">

    Product Name <br>
    <input name="name"><br>

    Part Number <br>
    <input name="part"><br>

    Brand <br>
    <input name="brand"><br>

    Model <br>
    <input name="model"><br>

    Price <br>
    <input name="price"><br>

    Stock <br>
    <input name="stock"><br><br>

    <button>Add Product</button>

    </form>

    <br>

    <a href="/">Back to Store</a>

    """


@app.route("/dashboard")
def dashboard():

    return f"""

    <h1>📊 Sales Dashboard</h1>

    <p>Total Products: {len(products)}</p>

    <p>Total Orders: {len(orders)}</p>

    <p>Cart Items: {len(cart)}</p>

    <br>

    <a href="/">Back</a>

    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
