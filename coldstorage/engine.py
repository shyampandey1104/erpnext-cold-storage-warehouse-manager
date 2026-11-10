"""Cold Storage Warehouse Chamber Monitoring, Slot Rental & Perishables Engine."""

from datetime import date, datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class ChamberZone(BaseModel):
    chamber_id: str
    chamber_name: str
    target_temperature_celsius: float
    min_temp_limit: float
    max_temp_limit: float
    humidity_pct: float
    total_pallet_capacity: int
    occupied_pallets: int = 0


class PalletDeposit(BaseModel):
    deposit_id: str
    farmer_or_client: str
    commodity: str  # e.g., Apples, Potatoes, Dairy, Vaccine, Frozen Seafood
    weight_quintals: float
    pallets_occupied: int
    chamber_id: str
    inward_date: str  # YYYY-MM-DD
    max_shelf_life_days: int
    monthly_rate_per_quintal: float


class ColdStorageManager:
    """Manages cold chambers, telemetry temperature breaches, and space billing."""

    def __init__(self):
        self.chambers: Dict[str, ChamberZone] = {}
        self.deposits: Dict[str, PalletDeposit] = {}

    def register_chamber(
        self,
        chamber_id: str,
        chamber_name: str,
        target_temp: float,
        min_temp: float,
        max_temp: float,
        capacity: int
    ) -> ChamberZone:
        chamber = ChamberZone(
            chamber_id=chamber_id,
            chamber_name=chamber_name,
            target_temperature_celsius=target_temp,
            min_temp_limit=min_temp,
            max_temp_limit=max_temp,
            humidity_pct=85.0,
            total_pallet_capacity=capacity,
            occupied_pallets=0
        )
        self.chambers[chamber_id] = chamber
        return chamber

    def inward_lot(
        self,
        deposit_id: str,
        client: str,
        commodity: str,
        weight_quintals: float,
        pallets: int,
        chamber_id: str,
        inward_date: str,
        shelf_life_days: int,
        rate_per_quintal: float = 120.0
    ) -> PalletDeposit:
        if chamber_id not in self.chambers:
            raise ValueError(f"Chamber {chamber_id} does not exist.")

        chamber = self.chambers[chamber_id]
        if chamber.occupied_pallets + pallets > chamber.total_pallet_capacity:
            raise ValueError("Insufficient pallet capacity in this chamber.")

        chamber.occupied_pallets += pallets
        deposit = PalletDeposit(
            deposit_id=deposit_id,
            farmer_or_client=client,
            commodity=commodity,
            weight_quintals=weight_quintals,
            pallets_occupied=pallets,
            chamber_id=chamber_id,
            inward_date=inward_date,
            max_shelf_life_days=shelf_life_days,
            monthly_rate_per_quintal=rate_per_quintal
        )
        self.deposits[deposit_id] = deposit
        return deposit

    def check_temperature_alarm(self, chamber_id: str, current_temp_celsius: float) -> Dict[str, Any]:
        """Telemetry check to detect temperature excursions threatening perishables."""
        chamber = self.chambers.get(chamber_id)
        if not chamber:
            return {"error": "Invalid chamber"}

        if current_temp_celsius > chamber.max_temp_limit:
            excursion = current_temp_celsius - chamber.max_temp_limit
            return {
                "alarm": True,
                "severity": "CRITICAL",
                "message": f"Chamber {chamber.chamber_name} temperature HIGH (+{current_temp_celsius}°C, threshold {chamber.max_temp_limit}°C). Spoilage risk!",
                "excursion_degrees": round(excursion, 2)
            }
        elif current_temp_celsius < chamber.min_temp_limit:
            return {
                "alarm": True,
                "severity": "WARNING",
                "message": f"Chamber {chamber.chamber_name} temperature chilling freeze hazard ({current_temp_celsius}°C < {chamber.min_temp_limit}°C).",
                "excursion_degrees": round(chamber.min_temp_limit - current_temp_celsius, 2)
            }

        return {"alarm": False, "severity": "NORMAL", "message": "Optimal temperature maintained."}

    def calculate_storage_invoice(self, deposit_id: str, checkout_date: str) -> Dict[str, Any]:
        """Calculates prorated cold-storage rent based on days and quintals."""
        dep = self.deposits.get(deposit_id)
        if not dep:
            raise ValueError(f"Deposit {deposit_id} not found.")

        d1 = datetime.strptime(dep.inward_date, "%Y-%m-%d").date()
        d2 = datetime.strptime(checkout_date, "%Y-%m-%d").date()
        days_stored = max(1, (d2 - d1).days)

        # Rate per day = monthly_rate / 30
        daily_rate_per_quintal = dep.monthly_rate_per_quintal / 30.0
        total_rent = days_stored * daily_rate_per_quintal * dep.weight_quintals
        handling_fee = dep.pallets_occupied * 150.0  # forklift pallet handling

        return {
            "deposit_id": deposit_id,
            "client": dep.farmer_or_client,
            "commodity": dep.commodity,
            "days_stored": days_stored,
            "weight_quintals": dep.weight_quintals,
            "storage_rent": round(total_rent, 2),
            "handling_fee": round(handling_fee, 2),
            "grand_total": round(total_rent + handling_fee, 2),
            "spoilage_risk_warning": days_stored > dep.max_shelf_life_days
        }
