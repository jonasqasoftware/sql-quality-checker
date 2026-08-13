SELECT
    'PAID_ORDER_WITHOUT_PAYMENT_DATE' AS finding_id,
    'high' AS severity,
    'order' AS entity_type,
    CAST(o.id AS TEXT) AS entity_id,
    'PAID order requires a payment date' AS rule,
    'status=' || o.status AS details
FROM orders AS o
WHERE o.status = 'PAID'
  AND o.paid_at IS NULL;
