# Logistics Microservice

A **microservice for managing products, stock, and orders**, built with **FastAPI** and **SQLAlchemy**. It handles transactional order creation, ensures data integrity, and provides a clean API for product and order management.  

---

## Project Overview

This microservice provides:

- **Products**: Create, list, and paginate available products.
- **Orders**: Transactional order creation, stock validation, and order item management.
- **Data Integrity**: Atomic transactions, isolation to prevent race conditions, and database constraints.
- **Testing**: Unit and integration tests using `pytest`.

Optional frontend integration (React/Next.js) can provide a dashboard for managing products and orders.

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy ORM
- **Database**: PostgreSQL
- **Testing**: pytest
- **Code Quality**: black, isort, flake8
- **Optional Frontend**: React/Next.js

---

## Features

### Products

- Create a new product
- List products with pagination
- Data validation for stock and price

### Orders

- Create an order with multiple items
- Check stock and reduce quantities
- Transactional: ensures atomicity and isolation
- Rollback on insufficient stock or errors
- Order items linked to products for historical price tracking

### Data Integrity

- Non-negative stock and price constraints (`CheckConstraint`)
- Enum-based order status (`OrderStatus`)
- Relationships and cascading delete for order items

---

## Folder Structure

```
logistics_microservice/
├─ app/
│  ├─ api/
│  │  ├─ orders.py        # Order endpoints
│  │  └─ products.py      # Product endpoints
│  ├─ core/
│  │  └─ database.py      # Database session & connection
│  ├─ enums.py            # Enums like OrderStatus
│  ├─ models/
│  │  ├─ order.py
│  │  ├─ order_item.py
│  │  └─ product.py
│  ├─ schemas/
│  │  ├─ order.py
│  │  └─ product.py
│  └─ services/
│     └─ order_service.py # Order business logic
├─ tests/
├─ alembic/               # Database migrations
├─ requirements.txt
├─ .env
└─ README.md
```

---

## Setup

1. Clone the repo:

```bash
git clone <repo_url>
cd logistics_microservice/logistics_microservice
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/logistics_db
```

5. Run database migrations:

```bash
alembic upgrade head
```

---

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`  
Swagger UI: `http://127.0.0.1:8000/docs`  

---

## API Endpoints

### Products

- **POST `/products`** – Create product

  Request:

  ```json
  {
    "name": "Product A",
    "price": 100.0,
    "stock_quantity": 50
  }
  ```

- **GET `/products?page=1&page_size=50`** – List products with pagination

  Response:

  ```json
  {
    "total_items": 120,
    "total_pages": 3,
    "current_page": 1,
    "items": [
      {
        "id": 1,
        "name": "Product A",
        "price": 100.0,
        "stock_quantity": 50
      }
    ]
  }
  ```

### Orders

- **POST `/orders`** – Create an order

  Request:

  ```json
  {
    "items": [
      {"product_id": 1, "quantity": 3},
      {"product_id": 2, "quantity": 1}
    ]
  }
  ```

  Response:

  ```json
  {
    "id": 1,
    "status": "PENDING",
    "items": [
      {"product_id": 1, "quantity_ordered": 3, "price_at_time_of_order": 100.0}
    ]
  }
  ```

- **Transactional Guarantees**
  - Validates stock availability
  - Deducts stock atomically
  - Rolls back if any product is out of stock
  - Prevents race conditions using `SELECT FOR UPDATE` and `db.begin_nested()`

---

## Testing

Run tests with:

```bash
pytest
```

Tests cover:

- Successful order creation
- Insufficient stock error handling
- Stock rollback on failed orders

---

## Code Quality

- **Formatting:** `black`
- **Imports:** `isort`
- **Linting:** `flake8`

Optional pre-commit hooks can enforce these rules automatically.

---

## Optional Frontend

- React/Next.js dashboard for products and orders
- View product list, stock, and order status
- “Ship” button to update pending orders via API

---

## Notes

- `db.flush()` is used to populate auto-generated primary keys before committing.
- `db.begin_nested()` allows nested transactions, useful for tests.
- Use **Enums** for consistent, type-safe status values.
- Constraints ensure stock and price cannot be negative.

