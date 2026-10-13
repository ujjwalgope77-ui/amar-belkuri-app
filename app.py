import os
import sqlite3
from functools import wraps

from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, price REAL NOT NULL,
        image TEXT, description TEXT);
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, address TEXT, items TEXT, total REAL,
        created TEXT DEFAULT CURRENT_TIMESTAMP);
    """)
    if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO products(name, price, image, description) VALUES(?,?,?,?)",
            [("চাল (১ কেজি)", 65, "", "ভালো মানের চাল"),
             ("সয়াবিন তেল (১ লিটার)", 170, "", "খাঁটি সয়াবিন তেল"),
             ("ডিম (১ ডজন)", 140, "", "তাজা ডিম")])
    conn.commit()
    conn.close()


init_db()


def cart_items():
    cart = session.get("cart", {})
    items, total = [], 0
    for pid, qty in cart.items():
        p = get_db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if p:
            sub = p["price"] * qty
            total += sub
            items.append({"p": p, "qty": qty, "sub": sub})
    return items, total


def admin_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*a, **kw)
    return wrapper


@app.context_processor
def inject_count():
    return {"cart_count": sum(session.get("cart", {}).values())}


@app.route("/")
def index():
    products = get_db().execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    return render_template("index.html", products=products)


@app.route("/add/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    flash("কার্টে যোগ হয়েছে")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart")
def cart():
    items, total = cart_items()
    return render_template("cart.html", items=items, total=total)


@app.route("/remove/<int:pid>", methods=["POST"])
def remove(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = cart_items()
    if not items:
        return redirect(url_for("index"))
    if request.method == "POST":
        desc = ", ".join(f'{i["p"]["name"]} x{i["qty"]}' for i in items)
        conn = get_db()
        conn.execute(
            "INSERT INTO orders(name, phone, address, items, total) VALUES(?,?,?,?,?)",
            (request.form["name"], request.form["phone"],
             request.form["address"], desc, total))
        conn.commit()
        session["cart"] = {}
        flash("অর্ডার সম্পন্ন হয়েছে! ধন্যবাদ।")
        return redirect(url_for("index"))
    return render_template("checkout.html", items=items, total=total)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("ভুল পাসওয়ার্ড")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin")
@admin_required
def admin():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("admin.html", products=products, orders=orders)


@app.route("/admin/add", methods=["POST"])
@admin_required
def admin_add():
    conn = get_db()
    conn.execute(
        "INSERT INTO products(name, price, image, description) VALUES(?,?,?,?)",
        (request.form["name"], float(request.form["price"]),
         request.form.get("image", ""), request.form.get("description", "")))
    conn.commit()
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:pid>", methods=["POST"])
@admin_required
def admin_delete(pid):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
