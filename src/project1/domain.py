from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import uuid


def _new_id() -> str:
    return str(uuid.uuid4())


def calculate_line_total(
    quantity: float,
    agreed_rate: float,
    extra_charges: float = 0.0,
    discount: float = 0.0,
) -> float:
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")
    if extra_charges < 0:
        raise ValueError("Extra charges cannot be negative.")
    if discount < 0:
        raise ValueError("Discount cannot be negative.")
    total = (quantity * agreed_rate) + extra_charges - discount
    if total < 0:
        raise ValueError("Line total cannot be negative.")
    return round(total, 2)


@dataclass
class OwnerAccount:
    owner_id: str
    display_name: str = "Owner"
    preferred_locale: str = "en-IN"
    currency_code: str = "INR"


@dataclass
class Customer:
    id: str
    owner_account_id: str
    name: str
    phone: Optional[str] = None
    village: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


@dataclass
class Tractor:
    id: str
    owner_account_id: str
    display_name: str
    registration_number: Optional[str] = None
    make_model: Optional[str] = None
    active: bool = True


@dataclass
class Rate:
    id: str
    activity_type_id: str
    unit: str
    amount: float
    currency_code: str = "INR"
    effective_from: str = ""
    effective_to: Optional[str] = None


@dataclass
class ActivityType:
    id: str
    owner_account_id: str
    name: str
    default_unit: str
    active: bool = True
    rates: List[Rate] = field(default_factory=list)

    def set_rate(self, unit: str, amount: float, currency_code: str = "INR") -> Rate:
        rate = Rate(
            id=_new_id(),
            activity_type_id=self.id,
            unit=unit,
            amount=amount,
            currency_code=currency_code,
            effective_from="now",
        )
        self.rates.append(rate)
        return rate

    def current_rate(self, unit: str) -> Rate:
        for rate in reversed(self.rates):
            if rate.unit == unit:
                return rate
        raise ValueError(f"No rate defined for activity {self.name!r} on unit {unit!r}.")


class BusinessRegistry:
    def __init__(self, owner_id: str, display_name: str = "Owner"):
        self.owner = OwnerAccount(owner_id=owner_id, display_name=display_name)
        self._customers: Dict[str, Customer] = {}
        self._tractors: Dict[str, Tractor] = {}
        self._activities: Dict[str, ActivityType] = {}

    def add_customer(
        self,
        name: str,
        phone: Optional[str] = None,
        village: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Customer:
        customer = Customer(
            id=_new_id(),
            owner_account_id=self.owner.owner_id,
            name=name,
            phone=phone,
            village=village,
            notes=notes,
            active=True,
        )
        self._customers[customer.id] = customer
        return customer

    def get_customer(self, customer_id: str) -> Customer:
        return self._customers[customer_id]

    def find_customers_by_name(self, name: str) -> List[Customer]:
        return [customer for customer in self._customers.values() if customer.name == name]

    def add_tractor(
        self,
        display_name: str,
        registration_number: Optional[str] = None,
        make_model: Optional[str] = None,
    ) -> Tractor:
        tractor = Tractor(
            id=_new_id(),
            owner_account_id=self.owner.owner_id,
            display_name=display_name,
            registration_number=registration_number,
            make_model=make_model,
            active=True,
        )
        self._tractors[tractor.id] = tractor
        return tractor

    def get_tractor(self, tractor_id: str) -> Tractor:
        return self._tractors[tractor_id]

    def add_activity_type(self, name: str, default_unit: str) -> ActivityType:
        activity = ActivityType(
            id=_new_id(),
            owner_account_id=self.owner.owner_id,
            name=name,
            default_unit=default_unit,
            active=True,
        )
        self._activities[name] = activity
        return activity

    def get_activity_type_by_name(self, name: str) -> ActivityType:
        return self._activities[name]

    def set_rate(self, activity_name: str, unit: str, amount: float, currency_code: str = "INR") -> Rate:
        activity = self.get_activity_type_by_name(activity_name)
        return activity.set_rate(unit=unit, amount=amount, currency_code=currency_code)
