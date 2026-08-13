SELECT
    'INVALID_ORDER_VALUE' AS finding_id,
    'high' AS severity,
    'order' AS entity_type,
    CAST(o.id AS TEXT) AS entity_id,
    'Order total must be positive' AS rule,
    'total_amount_cents=' || o.total_amount_cents AS details
FROM orders AS o
WHERE o.total_amount_cents <= 0;
