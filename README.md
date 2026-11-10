# ERPNext Cold Storage Warehouse Manager ❄️🥔

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise cold-chain warehouse, Controlled Atmosphere (CA) chamber management, and agro-commodity space-rental billing app for **ERPNext & Frappe**. Built for cold storages storing potatoes, apples, dairy, seafood, and temperature-sensitive pharmaceutical vaccines.

---

## 🚀 Key Features

- **Multi-Zone Chamber Telemetry**: Real-time IoT temperature and humidity boundary tracking (-25°C deep freeze to +10°C CA).
- **Critical Spoilage Excursion Alerts**: Instant warnings when chamber sensors exceed safety tolerance limits.
- **Farmer / Trader Pallet Space Rent**: Automated prorated billing per quintal/month with forklift loading/unloading charges.
- **Shelf-Life Expiry Counter**: Proactive alerts before perishable lots exceed safe storage longevity.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-cold-storage-warehouse-manager.git
cd erpnext-cold-storage-warehouse-manager
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from coldstorage.engine import ColdStorageManager

manager = ColdStorageManager()
manager.register_chamber("CH-01", "Potato Deep Chamber", target_temp=3.0, min_temp=1.0, max_temp=5.0, capacity=500)

# Inward agro lot
lot = manager.inward_lot(
    deposit_id="LOT-1002",
    client="Kisan Agro Cooperative",
    commodity="Storage Potatoes",
    weight_quintals=200.0,
    pallets=25,
    chamber_id="CH-01",
    inward_date="2026-02-01",
    shelf_life_days=180,
    rate_per_quintal=110.0
)

# Invoice billing upon dispatch
bill = manager.calculate_storage_invoice("LOT-1002", checkout_date="2026-03-03")
print(f"Total Rent: ₹{bill['grand_total']} for {bill['days_stored']} days.")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
