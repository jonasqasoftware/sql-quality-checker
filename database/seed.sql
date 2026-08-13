INSERT INTO users (id, email, status, created_at) VALUES
    (1, 'ana@example.test', 'ACTIVE', '2026-01-10'),
    (2, 'bruno@example.test', 'ACTIVE', '2026-01-12'),
    (3, 'carla@example.test', 'INACTIVE', '2026-01-15'),
    (4, 'ana@example.test', 'ACTIVE', '2026-01-20');

INSERT INTO orders (id, user_id, status, total_amount_cents, paid_at) VALUES
    (101, 1, 'PAID', 12500, '2026-02-01T10:00:00Z'),
    (102, 1, 'PENDING', 0, NULL),
    (103, 3, 'PAID', -500, NULL),
    (104, 999, 'PENDING', 9900, NULL);

INSERT INTO products (id, sku, name, stock_quantity, available_for_sale) VALUES
    (201, 'CHAIR-RED', 'Red chair', 5, 1),
    (202, 'MUG-BLUE', 'Blue mug', 0, 1),
    (203, 'BOOK-GREEN', 'Green book', 0, 0);
