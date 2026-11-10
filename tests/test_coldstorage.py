import unittest
from coldstorage.engine import ColdStorageManager


class TestColdStorageManager(unittest.TestCase):
    def setUp(self):
        self.manager = ColdStorageManager()
        self.manager.register_chamber(
            chamber_id="CH-01",
            chamber_name="Apple CA Chamber 1",
            target_temp=1.5,
            min_temp=0.5,
            max_temp=3.0,
            capacity=200
        )

    def test_inward_and_invoice(self):
        deposit = self.manager.inward_lot(
            deposit_id="LOT-901",
            client="Kashmir Valley Orchards",
            commodity="Shimla Delicious Apples",
            weight_quintals=50.0,
            pallets=10,
            chamber_id="CH-01",
            inward_date="2026-01-01",
            shelf_life_days=180,
            rate_per_quintal=150.0
        )
        self.assertEqual(deposit.pallets_occupied, 10)
        self.assertEqual(self.manager.chambers["CH-01"].occupied_pallets, 10)

        # Invoice calculation for 30 days
        invoice = self.manager.calculate_storage_invoice("LOT-901", "2026-01-31")
        self.assertEqual(invoice["days_stored"], 30)
        self.assertEqual(invoice["storage_rent"], 7500.0)
        self.assertFalse(invoice["spoilage_risk_warning"])

    def test_temperature_breach_alarm(self):
        alarm = self.manager.check_temperature_alarm("CH-01", current_temp_celsius=5.2)
        self.assertTrue(alarm["alarm"])
        self.assertEqual(alarm["severity"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
