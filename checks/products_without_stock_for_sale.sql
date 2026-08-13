SELECT
    'OUT_OF_STOCK_PRODUCT_FOR_SALE' AS finding_id,
    'medium' AS severity,
    'product' AS entity_type,
    CAST(p.id AS TEXT) AS entity_id,
    'Product without stock is available for sale' AS rule,
    'sku=' || p.sku AS details
FROM products AS p
WHERE p.stock_quantity <= 0
  AND p.available_for_sale = 1;
