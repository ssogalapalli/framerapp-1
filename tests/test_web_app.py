from uuid import uuid4

from project1 import __main__ as project_main
from project1.web_app import app, load_records


def unique_username(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Home" in response.data


def test_signup_page_renders():
    client = app.test_client()
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Sign Up" in response.data


def test_login_page_renders():
    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_signup_creates_user_and_login_redirects():
    username = unique_username("demo_user")
    client = app.test_client()
    signup = client.post(
        "/signup",
        data={"username": username, "password": "secret123"},
        follow_redirects=True,
    )
    assert signup.status_code == 200
    assert username.encode() in signup.data

    login = client.post(
        "/login",
        data={"username": username, "password": "secret123"},
        follow_redirects=True,
    )
    assert login.status_code == 200
    assert username.encode() in login.data


def test_add_page_requires_login():
    client = app.test_client()
    response = client.get("/add", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data


def test_add_record_post_creates_entry_for_logged_in_user():
    username = unique_username("farmer2")
    client = app.test_client()
    client.post("/signup", data={"username": username, "password": "pass123"})
    client.post("/login", data={"username": username, "password": "pass123"})

    response = client.post(
        "/add",
        data={
            "customer": "Asha",
            "tractor": "Mahindra 575",
            "activity": "Ploughing",
            "amount": "4500",
            "notes": "Field two completed",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Asha" in response.data


def test_records_page_renders_for_logged_in_user():
    username = unique_username("farmer3")
    client = app.test_client()
    client.post("/signup", data={"username": username, "password": "pass123"})
    client.post("/login", data={"username": username, "password": "pass123"})
    response = client.get("/records")
    assert response.status_code == 200
    assert b"All Details" in response.data


def test_add_page_has_existing_customer_option_and_customer_total_is_shown():
    username = unique_username("farmer_total")
    client = app.test_client()
    client.post("/signup", data={"username": username, "password": "pass123"})
    client.post("/login", data={"username": username, "password": "pass123"})

    client.post(
        "/add",
        data={
            "customer_type": "new",
            "customer": "Alice",
            "tractor": "John Deere",
            "activity": "Sowing",
            "amount": "2500",
            "notes": "Seed sowing",
        },
    )
    client.post(
        "/add",
        data={
            "customer_type": "existing",
            "customer": "Alice",
            "tractor": "John Deere",
            "activity": "Harvesting",
            "amount": "1500",
            "notes": "Harvest done",
        },
    )

    page = client.get("/records")
    assert page.status_code == 200
    assert b"Existing customer" in page.data
    assert b"Total" in page.data
    assert b"4000.00" in page.data


def test_owner_total_and_record_actions_work():
    username = unique_username("owner_actions")
    client = app.test_client()
    client.post("/signup", data={"username": username, "password": "pass123"})
    client.post("/login", data={"username": username, "password": "pass123"})

    client.post(
        "/add",
        data={
            "customer_type": "new",
            "customer": "Alpha",
            "tractor": "T1",
            "activity": "Ploughing",
            "amount": "1200",
            "notes": "First job",
        },
    )
    client.post(
        "/add",
        data={
            "customer_type": "new",
            "customer": "Beta",
            "tractor": "T2",
            "activity": "Harvesting",
            "amount": "900",
            "notes": "Second job",
        },
    )

    records = load_records()
    alpha_record = next(record for record in records if record.get("customer") == "Alpha")
    beta_record = next(record for record in records if record.get("customer") == "Beta")

    page = client.get("/records")
    assert page.status_code == 200
    assert b"Owner total" in page.data
    assert b"2100.00" in page.data

    toggle = client.post(f"/records/{alpha_record['id']}/toggle-paid", follow_redirects=True)
    assert toggle.status_code == 200
    assert b"Paid" in toggle.data

    update = client.post(
        f"/records/{beta_record['id']}/edit",
        data={
            "customer": "Beta",
            "tractor": "T2-updated",
            "activity": "Harvesting",
            "amount": "1500",
            "notes": "Updated job",
        },
        follow_redirects=True,
    )
    assert update.status_code == 200
    assert b"Updated job" in update.data

    delete = client.post(f"/records/{beta_record['id']}/delete", follow_redirects=True)
    assert delete.status_code == 200
    assert b"Beta" not in delete.data

    remaining = load_records()
    assert all(record.get("id") != beta_record["id"] for record in remaining)


def test_mobile_flag_runs_mobile_app(monkeypatch):
    calls = []

    def fake_mobile_main():
        calls.append("mobile")
        return 0

    monkeypatch.setattr(project_main.sys, "argv", ["project1", "--mobile"])
    monkeypatch.setattr(project_main, "mobile_main", fake_mobile_main, raising=False)

    assert project_main.main() == 0
    assert calls == ["mobile"]


def test_contact_page_renders():
    client = app.test_client()
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"Contact Us" in response.data
