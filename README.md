#  InventoryPro | Enterprise Stock Management
**A robust, multi-tenant inventory solution for the modern business.**

InventoryPro is a professional-grade application designed to streamline stock tracking, asset valuation, and cross-border commerce. Built with a focus on the West and Central African markets, it provides a localized experience that generic tools lack.

---

###  Core Value Pillars

####  Regional Localization
* **Multi-Currency Engine**: Native support for **NGN (₦)**, **XOF/XAF (CFA)**, and **USD ($)**.
* **Hybrid Translation**: A custom-built English/Spanish translation system that bypasses browser cookie restrictions for 100% reliability.

####  Enterprise Security
* **Data Isolation**: Strict multi-tenant architecture ensuring business owners only access their specific datasets.
* **Environment Shielding**: Zero-exposure policy using `.env` vaulting to protect sensitive application keys from version control.
* **Secure Authentication**: Industry-standard password hashing and protected session management.

####  Business Intelligence
* **Asset Valuation**: Real-time total inventory value calculations for better financial reporting.
* **Threshold Alerts**: Automated visual cues for low-stock items to prevent supply chain breaks.

---

###  Technical Specifications

| Layer | Technology |
| :--- | :--- |
| **Framework** | Python / Flask |
| **Database** | SQLAlchemy ORM (SQLite / PostgreSQL-ready) |
| **Frontend** | Jinja2, Bootstrap 5, FontAwesome |
| **Security** | Python-Dotenv, Werkzeug Security |
| **Environment** | Virtualenv (Python 3.12+) |



---

###  Deployment & Installation

1. **Clone & Navigate**
   ```bash
   git clone [https://github.com/yourusername/InventoryPro.git](https://github.com/yourusername/InventoryPro.git)
   cd InventoryPro
