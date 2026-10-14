import json
import os
from functools import wraps
from pathlib import Path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "records.json"
USERS_FILE = DATA_DIR / "users.json"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "src" / "project1" / "templates"),
    static_folder=str(BASE_DIR / "src" / "project1" / "static"),
)
app.config["SECRET_KEY"] = "tractor-mitra-web"


def ensure_json_file(path: Path, default: list | str = "[]") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(default, encoding="utf-8")


def load_users():
    ensure_json_file(USERS_FILE)
    try:
        with USERS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_users(users):
    ensure_json_file(USERS_FILE)
    with USERS_FILE.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def ensure_data_file() -> None:
    ensure_json_file(DATA_FILE)


def normalize_records(records):
    normalized = []
    for index, record in enumerate(records or []):
        if not isinstance(record, dict):
            continue
        normalized_record = dict(record)
        normalized_record["id"] = str(normalized_record.get("id") or f"record-{index}-{uuid4().hex[:8]}")
        normalized_record["username"] = str(normalized_record.get("username", "")).strip()
        normalized_record["customer"] = str(normalized_record.get("customer", "")).strip()
        normalized_record["tractor"] = str(normalized_record.get("tractor", "")).strip()
        normalized_record["activity"] = str(normalized_record.get("activity", "")).strip()
        normalized_record["notes"] = str(normalized_record.get("notes", "")).strip()
        normalized_record["paid"] = bool(normalized_record.get("paid", False))
        try:
            normalized_record["amount"] = float(normalized_record.get("amount", 0) or 0)
        except (TypeError, ValueError):
            normalized_record["amount"] = 0.0
        normalized.append(normalized_record)
    return normalized


def load_records():
    ensure_data_file()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            records = data if isinstance(data, list) else []
    except json.JSONDecodeError:
        records = []
    return normalize_records(records)


def save_records(records):
    ensure_data_file()
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(normalize_records(records), file, indent=2)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


def get_user_customer_names(username):
    records = load_records()
    names = {
        record.get("customer", "").strip()
        for record in records
        if record.get("username") == username and record.get("customer")
    }
    return sorted(names)


@app.route("/")
def home():
    return render_template("home.html", username=session.get("username"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            error = "Username and password are required."
        else:
            users = load_users()
            if any(user.get("username") == username for user in users):
                error = "This username already exists. Please choose another one."
            else:
                users.append({"username": username, "password": password})
                save_users(users)
                session["username"] = username
                return redirect(url_for("records"))

    return render_template("signup.html", error=error, username=session.get("username"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        users = load_users()
        user = next((u for u in users if u.get("username") == username and u.get("password") == password), None)
        if user:
            session["username"] = username
            return redirect(url_for("records"))

        error = "Invalid username or password."

    return render_template("login.html", error=error, username=session.get("username"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_details():
    error = ""
    existing_customers = get_user_customer_names(session.get("username"))

    if request.method == "POST":
        customer_type = request.form.get("customer_type", "new")
        new_customer = request.form.get("customer_new", "").strip()
        existing_customer = request.form.get("customer_existing", "").strip()
        legacy_customer = request.form.get("customer", "").strip()
        customer = (new_customer or existing_customer or legacy_customer).strip()
        tractor = request.form.get("tractor", "").strip()
        activity = request.form.get("activity", "").strip()
        amount = request.form.get("amount", "").strip()
        notes = request.form.get("notes", "").strip()

        if customer_type == "existing" and not customer:
            error = "Please select an existing customer."
        elif customer_type == "new" and not customer:
            error = "Please enter a customer name."
        elif not all([tractor, activity, amount]):
            error = "Please fill in tractor, activity, and amount."
        else:
            try:
                amount_value = float(amount)
            except ValueError:
                error = "Amount must be a valid number."
            else:
                records = load_records()
                records.insert(
                    0,
                    {
                        "id": f"record-{uuid4().hex[:12]}",
                        "username": session["username"],
                        "customer": customer,
                        "tractor": tractor,
                        "activity": activity,
                        "amount": amount_value,
                        "notes": notes,
                        "paid": False,
                    },
                )
                save_records(records)
                return redirect(url_for("records"))

    return render_template(
        "add.html",
        error=error,
        username=session.get("username"),
        existing_customers=existing_customers,
    )


@app.route("/records", methods=["GET", "POST"])
@login_required
def records():
    selected_customer = request.form.get("customer", "").strip() if request.method == "POST" else request.args.get("customer", "").strip()
    all_user_records = [
        record
        for record in load_records()
        if record.get("username") == session.get("username")
    ]
    filtered_records = [
        record for record in all_user_records if not selected_customer or record.get("customer") == selected_customer
    ]

    customer_names = sorted({record.get("customer", "").strip() for record in all_user_records if record.get("customer")})
    owner_total = sum(float(record.get("amount", 0) or 0) for record in all_user_records)
    paid_total = sum(float(record.get("amount", 0) or 0) for record in all_user_records if record.get("paid"))

    customer_totals = []
    for customer in customer_names:
        customer_entries = [record for record in all_user_records if record.get("customer") == customer]
        customer_totals.append(
            {
                "customer": customer,
                "total": sum(float(record.get("amount", 0) or 0) for record in customer_entries),
                "count": len(customer_entries),
            }
        )

    return render_template(
        "records.html",
        records=filtered_records,
        username=session.get("username"),
        customer_names=customer_names,
        selected_customer=selected_customer,
        customer_totals=customer_totals,
        owner_total=owner_total,
        paid_total=paid_total,
    )


@app.route("/records/<record_id>/toggle-paid", methods=["POST"])
@login_required
def toggle_paid(record_id):
    records = load_records()
    for record in records:
        if record.get("id") == record_id and record.get("username") == session.get("username"):
            record["paid"] = not bool(record.get("paid", False))
            save_records(records)
            break
    return redirect(url_for("records"))


@app.route("/records/<record_id>/delete", methods=["POST"])
@login_required
def delete_record(record_id):
    records = load_records()
    remaining = [
        record for record in records if not (record.get("id") == record_id and record.get("username") == session.get("username"))
    ]
    save_records(remaining)
    return redirect(url_for("records"))


@app.route("/records/<record_id>/edit", methods=["GET", "POST"])
@login_required
def edit_record(record_id):
    records = load_records()
    record = next(
        (
            item for item in records
            if item.get("id") == record_id and item.get("username") == session.get("username")
        ),
        None,
    )
    if record is None:
        return redirect(url_for("records"))

    error = ""
    if request.method == "POST":
        customer = request.form.get("customer", "").strip()
        tractor = request.form.get("tractor", "").strip()
        activity = request.form.get("activity", "").strip()
        amount = request.form.get("amount", "").strip()
        notes = request.form.get("notes", "").strip()

        if not all([customer, tractor, activity, amount]):
            error = "Please fill in customer, tractor, activity, and amount."
        else:
            try:
                amount_value = float(amount)
            except ValueError:
                error = "Amount must be a valid number."
            else:
                record["customer"] = customer
                record["tractor"] = tractor
                record["activity"] = activity
                record["amount"] = amount_value
                record["notes"] = notes
                save_records(records)
                return redirect(url_for("records"))

    return render_template("edit_record.html", username=session.get("username"), record=record, error=error)


@app.route("/contact")
def contact():
    return render_template("contact.html", username=session.get("username"))


def main():
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
