SELECT
    'ORDER_WITH_UNKNOWN_USER' AS finding_id,
    'critical' AS severity,
    'order' AS entity_type,
    CAST(o.id AS TEXT) AS entity_id,
    'Order references a user that does not exist' AS rule,
    'user_id=' || o.user_id AS details
FROM orders AS o
LEFT JOIN users AS u ON u.id = o.user_id
WHERE u.id IS NULL;
