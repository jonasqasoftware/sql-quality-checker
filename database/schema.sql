PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    created_at TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'PAID', 'CANCELLED')),
    total_amount_cents INTEGER NOT NULL,
    paid_at TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL,
    available_for_sale INTEGER NOT NULL CHECK (available_for_sale IN (0, 1))
);

-- The orders table deliberately has no foreign key so the synthetic fixture
-- can demonstrate detection of an orphan order.
