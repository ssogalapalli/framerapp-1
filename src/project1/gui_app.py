from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "430")
Config.set("graphics", "height", "760")

FARMER_BG = (0.95, 0.91, 0.82, 1)
FARMER_PANEL = (1.0, 0.99, 0.96, 1)
FARMER_PANEL_SOFT = (0.96, 0.93, 0.84, 1)
FARMER_GREEN = (0.18, 0.43, 0.24, 1)
FARMER_GREEN_DARK = (0.11, 0.28, 0.16, 1)
FARMER_BROWN = (0.41, 0.30, 0.17, 1)
FARMER_GOLD = (0.83, 0.64, 0.22, 1)
FARMER_TEXT = (0.12, 0.12, 0.12, 1)
FARMER_MUTED = (0.47, 0.41, 0.33, 1)
FARMER_LINE = (0.85, 0.78, 0.66, 1)


class ModernTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 48
        self.padding = (12, 10, 12, 10)
        self.write_tab = False
        self.background_color = (1, 1, 0.99, 1)
        self.foreground_color = FARMER_TEXT
        self.cursor_color = FARMER_GREEN
        self.hint_text_color = FARMER_MUTED
        self.font_size = 16


class ModernButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 52
        self.background_color = FARMER_GREEN
        self.background_down = FARMER_GREEN_DARK
        self.color = (1, 1, 1, 1)
        self.bold = True


class SummaryCard(BoxLayout):
    def __init__(self, label, value, subtitle, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [16, 12, 16, 12]
        self.spacing = 4
        self.size_hint_y = None
        self.height = 116
        self.canvas.before.clear()
        self.canvas.before.add(Color(1, 0.99, 0.97, 1))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        self.add_widget(Label(text=label.upper(), color=FARMER_MUTED, font_size=12, bold=True, halign="left"))
        self.add_widget(Label(text=value, color=FARMER_GREEN_DARK, font_size=22, bold=True, halign="left"))
        self.add_widget(Label(text=subtitle, color=FARMER_MUTED, font_size=12, halign="left"))


class NavBar(BoxLayout):
    def __init__(self, dashboard, **kwargs):
        super().__init__(**kwargs)
        self.dashboard = dashboard
        self.size_hint_y = None
        self.height = 52
        self.spacing = 6
        self.padding = [8, 6, 8, 6]
        self.canvas.before.clear()
        self.canvas.before.add(Color(0.9, 0.82, 0.68, 1))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        buttons = ["Home", "Add", "Records", "Profile"]
        for name in buttons:
            btn = Button(text=name, background_color=FARMER_GREEN, color=(1, 1, 1, 1), bold=True)
            btn.bind(on_press=lambda instance, view=name: self.dashboard.switch_view(view))
            self.add_widget(btn)


class WorkOrderForm(BoxLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent_app = parent
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 12
        self.size_hint_y = None
        self.height = 370
        self.canvas.before.clear()
        self.canvas.before.add(Color(*FARMER_PANEL))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        title = Label(text="Add Details", font_size=24, bold=True, color=FARMER_GREEN_DARK, size_hint_y=None, height=30)
        self.add_widget(title)

        self.customer_input = ModernTextInput(hint_text="Customer name")
        self.tractor_input = ModernTextInput(hint_text="Tractor / vehicle")
        self.activity_input = ModernTextInput(hint_text="Activity")
        self.amount_input = ModernTextInput(hint_text="Amount (₹)", input_filter="float")
        self.notes_input = ModernTextInput(hint_text="Notes")

        self.status_label = Label(
            text="Ready to record a job",
            halign="center",
            valign="middle",
            color=FARMER_GREEN_DARK,
            size_hint_y=None,
            height=42,
            text_size=(350, None),
            bold=True,
        )

        save_button = ModernButton(text="SAVE ENTRY")
        save_button.bind(on_press=self.save_work_order)

        self.add_widget(self.customer_input)
        self.add_widget(self.tractor_input)
        self.add_widget(self.activity_input)
        self.add_widget(self.amount_input)
        self.add_widget(self.notes_input)
        self.add_widget(save_button)
        self.add_widget(self.status_label)

    def save_work_order(self, instance):
        customer = self.customer_input.text.strip()
        tractor = self.tractor_input.text.strip()
        activity = self.activity_input.text.strip()
        amount = self.amount_input.text.strip()
        notes = self.notes_input.text.strip()

        if not customer or not tractor or not activity or not amount:
            self.status_label.text = "Please fill all fields before saving."
            return

        try:
            amount_value = float(amount)
        except ValueError:
            self.status_label.text = "Amount must be a valid number."
            return

        self.parent_app.add_record(
            {
                "id": f"record-{len(self.parent_app.records) + 1}",
                "customer": customer,
                "tractor": tractor,
                "activity": activity,
                "amount": amount_value,
                "notes": notes,
                "paid": False,
            }
        )
        self.status_label.text = f"Saved: {customer} / {tractor} / ₹{amount_value:.2f}"
        self.customer_input.text = ""
        self.tractor_input.text = ""
        self.activity_input.text = ""
        self.amount_input.text = ""
        self.notes_input.text = ""


class RecordCard(BoxLayout):
    def __init__(self, record, callback_toggle, callback_delete, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 4
        self.padding = [12, 10, 12, 10]
        self.size_hint_y = None
        self.height = 150
        self.canvas.before.clear()
        self.canvas.before.add(Color(1, 0.99, 0.97, 1))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        self.record = record
        self.callback_toggle = callback_toggle
        self.callback_delete = callback_delete

        top = BoxLayout(size_hint_y=None, height=34)
        top.add_widget(Label(text=record["customer"], bold=True, color=FARMER_GREEN_DARK, font_size=18))
        top.add_widget(Label(text=f"₹{record['amount']:.2f}", bold=True, color=FARMER_GREEN, font_size=18, halign="right"))

        status = Label(
            text="PAID" if record.get("paid") else "OUTSTANDING",
            color=(0.29, 0.55, 0.31, 1) if record.get("paid") else (0.76, 0.58, 0.05, 1),
            bold=True,
            font_size=12,
            size_hint_y=None,
            height=20,
        )

        details = Label(
            text=f"{record['tractor']} • {record['activity']}\n{record.get('notes', '') or 'No notes'}",
            color=FARMER_TEXT,
            font_size=13,
            halign="left",
            valign="middle",
            text_size=(340, None),
            size_hint_y=None,
            height=58,
        )

        actions = BoxLayout(size_hint_y=None, height=36, spacing=8)
        toggle = Button(text="MARK PAID" if not record.get("paid") else "MARK UNPAID", background_color=FARMER_GREEN, color=(1, 1, 1, 1))
        delete = Button(text="DELETE", background_color=(0.86, 0.38, 0.32, 1), color=(1, 1, 1, 1))
        toggle.bind(on_press=lambda instance, rec=record: self.callback_toggle(rec))
        delete.bind(on_press=lambda instance, rec=record: self.callback_delete(rec))
        actions.add_widget(toggle)
        actions.add_widget(delete)

        self.add_widget(top)
        self.add_widget(status)
        self.add_widget(details)
        self.add_widget(actions)


class RecordsList(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = 8
        self.padding = 8
        self.size_hint_y = None
        self.bind(minimum_height=self.setter("height"))

    def update_records(self, records):
        self.clear_widgets()
        if not records:
            empty = Label(
                text="No work orders yet.",
                color=FARMER_MUTED,
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=80,
            )
            self.add_widget(empty)
            return

        for record in records:
            self.add_widget(RecordCard(record, self.parent.parent_app.toggle_paid, self.parent.parent_app.delete_record))


class TractorMitraDashboard(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = 18
        self.spacing = 12
        self.canvas.before.clear()
        self.canvas.before.add(Color(*FARMER_BG))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        self.records = [
            {"id": "record-1", "customer": "Alpha", "tractor": "Tractor 1", "activity": "Ploughing", "amount": 1200.0, "notes": "Field preparation", "paid": False},
            {"id": "record-2", "customer": "Beta", "tractor": "Tractor 2", "activity": "Harvesting", "amount": 900.0, "notes": "Crop collection", "paid": True},
        ]
        self.current_view = "Home"

        self.nav_bar = NavBar(self)
        self.add_widget(self.nav_bar)

        self.content_area = BoxLayout(orientation="vertical", spacing=10)
        self.add_widget(self.content_area)

        self.summary_cards = BoxLayout(size_hint_y=None, height=120, spacing=10)
        self.total_card = SummaryCard("TOTAL AMOUNT TO BE RECEIVED", "₹0.00", "All customer work billed")
        self.received_card = SummaryCard("AMOUNT RECEIVED", "₹0.00", "Total received")
        self.summary_cards.add_widget(self.total_card)
        self.summary_cards.add_widget(self.received_card)

        self.filter_row = BoxLayout(size_hint_y=None, height=42, spacing=10)
        self.filter_label = Label(text="Filter customer", color=FARMER_GREEN_DARK, bold=True, size_hint_x=0.5)
        self.filter_spinner = Spinner(text="All customers", values=["All customers", "Alpha", "Beta"], size_hint_x=1.5)
        self.filter_spinner.bind(text=self.on_filter_change)
        self.filter_row.add_widget(self.filter_label)
        self.filter_row.add_widget(self.filter_spinner)

        self.records_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.records_list = RecordsList()
        self.records_view.add_widget(self.records_list)

        self.form = WorkOrderForm(self)
        self.home_panel = BoxLayout(orientation="vertical", spacing=10)
        self.home_panel.add_widget(Label(text="Welcome to Tractor Mitra", font_size=24, bold=True, color=FARMER_GREEN_DARK, size_hint_y=None, height=30))
        self.home_panel.add_widget(Label(text="Track your field operations, customer work, and payment status from one place.", color=FARMER_MUTED, font_size=14, text_size=(340, None), halign="left"))
        self.home_panel.add_widget(self.summary_cards)

        self.show_home_view()

    def switch_view(self, view_name):
        self.current_view = view_name
        if view_name == "Home":
            self.show_home_view()
        elif view_name == "Add":
            self.show_add_view()
        elif view_name == "Records":
            self.show_records_view()
        else:
            self.show_profile_view()

    def show_home_view(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.home_panel)
        self.refresh_summary()

    def show_add_view(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.form)

    def show_records_view(self):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.filter_row)
        self.content_area.add_widget(self.records_view)
        self.apply_filter()

    def show_profile_view(self):
        self.content_area.clear_widgets()
        profile = BoxLayout(orientation="vertical", spacing=10)
        profile.add_widget(Label(text="Profile", font_size=24, bold=True, color=FARMER_GREEN_DARK, size_hint_y=None, height=30))
        profile.add_widget(Label(text="Logged in as: Farmer Owner", color=FARMER_MUTED, font_size=16))
        profile.add_widget(Label(text="Customer account management", color=FARMER_MUTED, font_size=14, text_size=(340, None), halign="left"))
        self.content_area.add_widget(profile)

    def on_filter_change(self, instance, value):
        if self.current_view == "Records":
            self.apply_filter()

    def apply_filter(self):
        selected = self.filter_spinner.text
        if selected == "All customers" or not selected:
            visible = self.records
        else:
            visible = [record for record in self.records if record.get("customer") == selected]
        self.records_list.update_records(visible)

    def add_record(self, record):
        self.records.insert(0, record)
        current_customers = [self.filter_spinner.values[i] for i in range(1, len(self.filter_spinner.values))]
        if record["customer"] not in current_customers:
            values = list(self.filter_spinner.values)
            values.append(record["customer"])
            self.filter_spinner.values = values
        self.apply_filter()
        self.refresh_summary()

    def toggle_paid(self, record):
        for item in self.records:
            if item.get("id") == record.get("id"):
                item["paid"] = not item.get("paid", False)
                break
        self.apply_filter()
        self.refresh_summary()

    def delete_record(self, record):
        self.records = [item for item in self.records if item.get("id") != record.get("id")]
        self.apply_filter()
        self.refresh_summary()

    def refresh_summary(self):
        total = sum(item["amount"] for item in self.records)
        paid = sum(item["amount"] for item in self.records if item.get("paid"))
        self.total_card.children[1].text = f"₹{total:.2f}"
        self.received_card.children[1].text = f"₹{paid:.2f}"


class SplashScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = [30, 40, 30, 40]
        self.spacing = 10
        self.canvas.before.clear()
        self.canvas.before.add(Color(0.86, 0.74, 0.46, 1))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        logo = Label(text="🌾", font_size=72, halign="center", valign="middle", size_hint_y=None, height=90)
        title = Label(text="Tractor Mitra", font_size=30, bold=True, color=FARMER_GREEN_DARK)
        subtitle = Label(text="Farm operations dashboard", font_size=14, color=FARMER_BROWN)
        self.add_widget(logo)
        self.add_widget(title)
        self.add_widget(subtitle)


class MobileLoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.spacing = 12
        self.padding = [20, 30, 20, 30]
        self.canvas.before.clear()
        self.canvas.before.add(Color(*FARMER_BG))
        self.canvas.before.add(Rectangle(pos=self.pos, size=self.size))

        self.add_widget(Label(text="Tractor Mitra", font_size=30, bold=True, color=FARMER_GREEN_DARK, size_hint_y=None, height=40))
        self.add_widget(Label(text="Login / Sign Up", font_size=18, color=FARMER_BROWN, size_hint_y=None, height=24))

        form = BoxLayout(orientation="vertical", spacing=12, size_hint_y=None, height=220)
        form.canvas.before.clear(); form.canvas.before.add(Color(*FARMER_PANEL)); form.canvas.before.add(Rectangle(pos=form.pos, size=form.size))
        self.username_input = ModernTextInput(hint_text="Username")
        self.password_input = ModernTextInput(hint_text="Password", password=True)
        form.add_widget(self.username_input)
        form.add_widget(self.password_input)

        buttons = BoxLayout(size_hint_y=None, height=52, spacing=10)
        login_btn = ModernButton(text="LOGIN")
        signup_btn = ModernButton(text="SIGN UP")
        login_btn.bind(on_press=self.do_login)
        signup_btn.bind(on_press=self.do_signup)
        buttons.add_widget(login_btn)
        buttons.add_widget(signup_btn)

        form.add_widget(buttons)
        self.add_widget(form)

    def do_login(self, instance):
        self.app.screen_manager.current = "dashboard"

    def do_signup(self, instance):
        self.app.screen_manager.current = "dashboard"


class TractorMitraApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        splash_widget = SplashScreen(self)
        splash_screen = Screen(name="splash")
        splash_screen.add_widget(splash_widget)

        login_screen_widget = MobileLoginScreen(self)
        login_screen = Screen(name="login")
        login_screen.add_widget(login_screen_widget)

        dashboard_widget = TractorMitraDashboard(self)
        dashboard_screen = Screen(name="dashboard")
        dashboard_screen.add_widget(dashboard_widget)

        self.screen_manager.add_widget(splash_screen)
        self.screen_manager.add_widget(login_screen)
        self.screen_manager.add_widget(dashboard_screen)
        self.screen_manager.current = "splash"
        Clock.schedule_once(lambda dt: setattr(self.screen_manager, "current", "login"), 1.5)
        return self.screen_manager


def main():
    TractorMitraApp().run()
