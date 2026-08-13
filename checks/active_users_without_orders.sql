SELECT
    'ACTIVE_USER_WITHOUT_ORDERS' AS finding_id,
    'medium' AS severity,
    'user' AS entity_type,
    CAST(u.id AS TEXT) AS entity_id,
    'ACTIVE user has no orders' AS rule,
    'email=' || u.email AS details
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE u.status = 'ACTIVE'
GROUP BY u.id, u.email
HAVING COUNT(o.id) = 0;
