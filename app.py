from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
import os

otp = random.randint(100000,999999)

app = Flask(__name__)

app.secret_key = "spare_shop_secret_key"


# ================= EMAIL OTP SETTINGS =================

from flask_mail import Mail, Message


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'venasmwaipopo@gmail.com'
app.config['MAIL_PASSWORD'] = 'xprm nxvp igdb esuu'

mail = Mail(app)


# DATABASE

def get_db():

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row

    return conn

# DATABASE CONNECTION
def get_db():

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row

    return conn
def check_columns():

    conn = get_db()

    columns = conn.execute(
        "PRAGMA table_info(users)"
    ).fetchall()


    existing = []

    for col in columns:
        existing.append(col["name"])


    new_columns = {

        "email":"TEXT",

        "phone":"TEXT",

        "address":"TEXT",

        "business":"TEXT"

    }


    for name, dtype in new_columns.items():

        if name not in existing:

            conn.execute(
                f"ALTER TABLE users ADD COLUMN {name} {dtype}"
            )


    conn.commit()

    conn.close()


check_columns()

def create_products_table():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS products(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_name TEXT,

        category TEXT,

        brand TEXT,

        buying_price REAL,

        selling_price REAL,

        quantity INTEGER,

        minimum_stock INTEGER,

        image TEXT

    )
    """)

    conn.commit()
    conn.close()

# ================= LOGIN =================


@app.route("/", methods=["GET","POST"])
def login():


    if request.method == "POST":


        username = request.form["username"]

        password = request.form["password"]



        conn = get_db()


        user = conn.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username,password)

        ).fetchone()



        conn.close()



        if user:

            session["user"] = user["fullname"]
            session["email"] = user["email"]

            return redirect("/dashboard")



        else:


            return render_template(
                "login.html",
                error="Username au Password si sahihi"
            )



    return render_template("login.html")






# ================= DASHBOARD =================


@app.route("/dashboard")
def dashboard():


    if "user" not in session:

        return redirect("/")



    return render_template(

        "dashboard.html",

        title="Dashboard",

        user=session["user"]

    )







# ================= PROFILE =================


@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/")


    conn = get_db()


    user = conn.execute(
        "SELECT * FROM users WHERE fullname=?",
        (session["user"],)
    ).fetchone()


    conn.close()


    return render_template(
        "profile.html",
        user=user,
        title="Profile"
    )

# ================= PRODUCTS =================



@app.route("/products")
def products():


    if "user" not in session:

        return redirect("/")



    search = request.args.get("search")



    conn = get_db()



    if search:


        products = conn.execute(

            """
            SELECT * FROM products
            WHERE product_name LIKE ?

            """,

            ('%'+search+'%',)

        ).fetchall()



    else:


        products = conn.execute(

            "SELECT * FROM products"

        ).fetchall()



    conn.close()



    return render_template(

        "products.html",

        products=products

    )








# ================= ADD PRODUCT =================



@app.route("/add_product", methods=["GET","POST"])
def add_product():


    if "user" not in session:

        return redirect("/")



    if request.method == "POST":


        product_name = request.form["product_name"]

        category = request.form["category"]

        brand = request.form["brand"]

        buying_price = request.form["buying_price"]

        selling_price = request.form["selling_price"]

        quantity = request.form["quantity"]

        minimum_stock = request.form["minimum_stock"]




        conn = get_db()



        conn.execute(

        """
        INSERT INTO products

        (
        product_name,
        category,
        brand,
        buying_price,
        selling_price,
        quantity,
        minimum_stock
        )

        VALUES(?,?,?,?,?,?,?)

        """,

        (

        product_name,
        category,
        brand,
        buying_price,
        selling_price,
        quantity,
        minimum_stock

        ))



        conn.commit()

        conn.close()



        return redirect("/products")




    return render_template("add_product.html")







# ================= EDIT PRODUCT =================



@app.route("/edit_product/<int:id>", methods=["GET","POST"])
def edit_product(id):


    if "user" not in session:

        return redirect("/")



    conn = get_db()



    if request.method == "POST":


        conn.execute(

        """

        UPDATE products SET

        product_name=?,

        category=?,

        brand=?,

        buying_price=?,

        selling_price=?,

        quantity=?

        WHERE id=?

        """,

        (

        request.form["product_name"],

        request.form["category"],

        request.form["brand"],

        request.form["buying_price"],

        request.form["selling_price"],

        request.form["quantity"],

        id

        ))



        conn.commit()

        conn.close()



        return redirect("/products")




    product = conn.execute(

        "SELECT * FROM products WHERE id=?",

        (id,)

    ).fetchone()



    conn.close()



    return render_template(

        "edit_product.html",

        product=product

    )







# ================= DELETE PRODUCT =================



ADMIN_PIN = "1234"

@app.route("/delete_product/<int:id>", methods=["GET", "POST"])
def delete_product(id):

    if request.method == "POST":

        pin = request.form["pin"]

        if pin == ADMIN_PIN:

            conn = get_db()

            conn.execute(
                "DELETE FROM products WHERE id=?",
                (id,)
            )

            conn.commit()
            conn.close()

            return redirect("/products")

        return render_template(
            "verify_delete.html",
            id=id,
            error="Incorrect PIN!"
        )

    return render_template(
        "verify_delete.html",
        id=id
    )
# ================= UPLOAD PROFILE =================

@app.route("/upload_profile", methods=["POST"])
def upload_profile():

    image = request.files["image"]

    folder = os.path.join(
        "static",
        "uploads"
    )

    if not os.path.isdir(folder):
        os.makedirs(folder)


    path = os.path.join(
        folder,
        "profile.jpg"
    )


    image.save(path)


    return redirect("/profile")
#================= EDIT PROFILE =================
@app.route("/edit_profile", methods=["GET","POST"])
def edit_profile():

    if "user" not in session:
        return redirect("/")


    conn = get_db()


    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        business = request.form["business"]


        conn.execute("""
        UPDATE users SET

        fullname=?,
        email=?,
        phone=?,
        address=?,
        business=?

        WHERE username=?

        """,
        (
        fullname,
        email,
        phone,
        address,
        business,
        session["username"]
        ))


        conn.commit()


        session["user"] = fullname


        conn.close()


        return redirect("/profile")



    user = conn.execute(
        """
        SELECT * FROM users
        WHERE username=?
        """,
        (session["username"],)

    ).fetchone()



    conn.close()


    return render_template(
        "edit_profile.html",
        user=user
    )


@app.route("/sales")
def sales():

    return render_template(
        "sales.html",
        title="Mauzo"
    )




@app.route("/reports")
def reports():

    conn = get_db()

    products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    low_products = conn.execute("""
        SELECT *
        FROM products
        WHERE quantity<=minimum_stock
    """).fetchall()

    conn.close()

    return render_template(
        "reports.html",
        title="Reports",
        total_sales=0,
        total_profit=0,
        purchases=0,
        products=products,
        low_products=low_products
    )



@app.route("/settings")
def settings():

    return render_template(
        "settings.html",
        title="Settings"
    )

@app.route("/stock")
def stock():

    conn = get_db()

    products = conn.execute("""
        SELECT *
        FROM products
    """).fetchall()

    total = len(products)

    available = sum(1 for p in products if p["quantity"] > 0)

    low = sum(
        1 for p in products
        if p["quantity"] > 0 and p["quantity"] <= p["minimum_stock"]
    )

    out = sum(1 for p in products if p["quantity"] == 0)

    conn.close()

    return render_template(
        "stock.html",
        title="Stock",
        products=products,
        total=total,
        available=available,
        low=low,
        out=out
    ) 

@app.route("/purchases", methods=["GET", "POST"])
def purchases():

    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products"
    ).fetchall()

    if request.method == "POST":

        # tutahifadhi database hatua inayofuata

        return redirect("/purchases")

    conn.close()

    return render_template(
        "purchases.html",
        title="Purchases",
        products=products
    )     

@app.route("/verify_add_product", methods=["GET", "POST"])
def verify_add_product():

    if request.method == "POST":

        pin = request.form["pin"]

        if pin == ADMIN_PIN:
            return redirect("/add_product")

        return render_template(
            "verify_pin.html",
            error="Incorrect PIN!"
        )

    return render_template("verify_pin.html")

#================= FORGOT PASSWORD =================
@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]


        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()


        if user:

            import random

            otp = str(random.randint(100000,999999))

            session["otp"] = otp
            session["reset_email"] = email


            msg = Message(
                "VENAS Spare Shop Password Reset OTP",
                sender="venasmwaipopo@gmail.com",
                recipients=[email]
            )


            msg.body = f"""
Hello {user['fullname']}

Your OTP code is:

{otp}

Use this code to reset your password.

VENAS J. MWAIPOPO
Spare Shop System
"""


            mail.send(msg)


            return redirect("/verify_otp")


        else:

            return render_template(
                "forgot_password.html",
                error="Email address not found"
            )


    return render_template("forgot_password.html")
    
#================= VERIFY OTP =================    
@app.route("/verify_otp", methods=["GET","POST"])
def verify_otp():

    if request.method == "POST":

        otp = request.form["otp"]


        if otp == session.get("otp"):

            return redirect("/reset_password")


        else:

            return render_template(
                "verify_otp.html",
                error="Invalid OTP"
            )


    return render_template("verify_otp.html")
   
#================= CHANGE PASSWORD =================        
@app.route("/change_password", methods=["GET","POST"])
def change_password():

    global ADMIN_PIN


    if "reset_password" not in session:

        return redirect("/")


    if request.method=="POST":

        new_pin=request.form["new_password"]

        ADMIN_PIN=new_pin


        session.pop("reset_password", None)


        return redirect("/dashboard")


    return render_template(
        "change_password.html"
    ) 
@app.route("/reset_password", methods=["GET","POST"])
def reset_password():

    if request.method == "POST":

        password = request.form["password"]


        email = session.get("reset_email")


        conn = get_db()

        conn.execute(
            """
            UPDATE users
            SET password=?
            WHERE email=?
            """,
            (password,email)
        )


        conn.commit()
        conn.close()


        session.clear()


        return redirect("/")


    return render_template("reset_password.html")        
# ================= LOGOUT =================



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

#=========================================
if __name__ == "__main__":

    create_products_table()
    app.run()