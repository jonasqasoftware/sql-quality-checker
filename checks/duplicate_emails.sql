SELECT
    'DUPLICATE_EMAIL' AS finding_id,
    'high' AS severity,
    'user_email' AS entity_type,
    u.email AS entity_id,
    'More than one user shares the same email' AS rule,
    'user_count=' || COUNT(*) AS details
FROM users AS u
GROUP BY u.email
HAVING COUNT(*) > 1;
