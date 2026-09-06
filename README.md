# 🛒 Hybrid Django E-Commerce Platform

A robust E-Commerce application utilizing a **hybrid backend architecture**. It seamlessly combines **Pure Django (Server-Side Rendered Templates)** with a decoupled **Django REST Framework (DRF) API** for ultimate client flexibility. The application securely manages complex business workflows including dynamic shopping carts, coupon mechanics, asynchronous order queues, and direct payment processing.

---

## 🚀 Key Modules & Architecture

- **Hybrid Setup:** Implements standard Django views alongside a RESTful API ecosystem (`/api/`) for versatile frontend integrations.
- **Cart & Coupon System (`cart/`, `coupons/`):** Manages live shopping cart state variables and processes absolute/percentage discount codes.
- **Orders & Payments (`orders/`, `payment/`):** Handles checkout configurations and processes card charges via the **Stripe Payment Gateway**.
- **Asynchronous Workflows:** Offloads heavy computing operations (like order confirmation invoicing) to an asynchronous worker queue.

---

## 🛠️ Tech Stack

- **Frameworks:** Django & Django REST Framework (DRF)
- **Asynchronous Task Queue:** Celery & RabbitMQ
- **Caching & Ranking Store:** Redis (Configured for high-speed Sorted Sets operations)
- **Payment Gateway:** Stripe API Integration
- **Local Database:** SQLite (Development standard)

---

## 📂 Project Structure

```text
├── api/             # Django REST Framework API controllers and serializers
├── cart/            # Session-based or API-driven shopping cart state logic
├── coupons/         # Coupon application engine and validation systems
├── locale/          # Internationalization (i18n) translation matrices
├── myshop/          # Core routing configurations and global settings
├── orders/          # Checkout tracking and order creation models
├── payment/         # Stripe webhook handlers and payment checkout pipelines
├── shop/            # Catalog structure (Categories, Products, and inventories)
└── templates/       # Pure Django server-side HTML template architecture
```

---

## ⚙️ Development Environment Setup

Because this project relies on specialized local services, follow these specific instructions to spin up the infrastructure background processes manually in your terminal windows.

### Prerequisites
- Python 3.11+ installed locally.
- **Docker Desktop** installed (used for launching external dependencies cleanly).
- **Stripe CLI** utility binary configured on your host workstation.

### Step 1: Clone and Set Up Dependencies
```bash
git clone https://github.com/SopheakBackend/Django-Backend-E-Commerce-with-Hybrid-Django-Rest-API-and-Pure-Django.git
cd Django-Backend-E-Commerce-with-Hybrid-Django-Rest-API-and-Pure-Django
python -m venv venv
# On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

### Step 2: Spin Up Infrastructure Terminals
Open **five separate terminal windows/panes** to operate the multi-service pipeline:

#### 💻 Terminal 1: Launch Redis (Sorted Sets Backend)
Run the exact version-pinned Redis image using Docker to serve your sorting and ranking tasks:
```bash
docker run -it --rm --name redis -p 6379:6379 redis:7.2.4
```

#### 🐇 Terminal 2: Launch RabbitMQ (Message Broker)
Run the RabbitMQ container with the management plugin dashboard active:
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
```

#### 💳 Terminal 3: Listen for Stripe Webhook Events
Tunnel live Stripe asynchronous event payloads directly down into your local running Django development node application endpoint:
```bash
stripe.exe listen --forward-to localhost:8000/payment/webhook/
```
*(Copy the generated webhook signing secret returned in the console output and paste it into your local configurations).*

#### ⚙️ Terminal 4: Start Celery Worker Tasks inside your VS CODE terminal
Launch your asynchronous engine worker instance with the `solo` pool execution flag (optimized for Windows machines):
```bash
celery -A myshop worker --pool=solo -l info
```

#### 🐍 Terminal 5: Run the Django Development Web Server
DO not forget to generate a django secret key inside the setting.py
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Start the local server instance to access the application UI components:
```bash
python manage.py runserver
```

---

## 🔒 Security Best Practices Warning

Before launching or pushing updates:
1. Ensure your local sensitive variables (such as **Stripe API Secret Keys** and **Django Secret Keys**) are safely externalized via an invisible local environment `.env` wrapper.
2. Verify that `db.sqlite3` configurations are strictly isolated out of your standard online repository tracking configurations via your root layout `.gitignore` file.
