from project1.domain import (
    BusinessRegistry,
    calculate_line_total,
)


def test_business_registry_tracks_customers_and_tractors():
    registry = BusinessRegistry(owner_id="owner-1")

    customer = registry.add_customer(
        name="Ravi Kumar",
        phone="9876543210",
        village="Nashik",
    )
    tractor = registry.add_tractor(
        display_name="Mahindra 575",
        registration_number="MH12AB1234",
    )

    assert customer.name == "Ravi Kumar"
    assert customer.phone == "9876543210"
    assert tractor.display_name == "Mahindra 575"
    assert registry.get_customer(customer.id).id == customer.id
    assert registry.get_tractor(tractor.id).id == tractor.id


def test_activity_rates_are_configurable_and_historical():
    registry = BusinessRegistry(owner_id="owner-1")

    registry.add_activity_type("Ploughing", default_unit="acre")
    registry.set_rate("Ploughing", "acre", 1200)
    registry.set_rate("Ploughing", "acre", 1350)

    activity = registry.get_activity_type_by_name("Ploughing")
    assert activity.default_unit == "acre"
    assert len(activity.rates) == 2
    assert activity.current_rate("acre").amount == 1350


def test_line_total_calculation_and_duplicate_warning():
    registry = BusinessRegistry(owner_id="owner-1")

    assert calculate_line_total(2, 1200, extra_charges=200, discount=100) == 2500

    first = registry.add_customer("Suresh Patil", phone="9999999999")
    second = registry.add_customer("Suresh Patil", phone="9999999999")

    assert first.id != second.id
    assert first.name == second.name
    assert registry.find_customers_by_name("Suresh Patil")[0].id == first.id
