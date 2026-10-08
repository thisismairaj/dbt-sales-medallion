-- Two independent defects, each kept as its own reason: a non-positive
-- quantity, or a product_id that doesn't exist. A row can match both checks;
-- union keeps one row per reason rather than collapsing them into one.
with bad_quantity as (
    select *, 'quantity <= 0' as quarantine_reason
    from {{ ref('stg_order_items') }}
    where quantity <= 0
),

orphan_product as (
    select i.*, 'product_id not found in stg_products' as quarantine_reason
    from {{ ref('stg_order_items') }} as i
    left join {{ ref('stg_products') }} as p on i.product_id = p.product_id
    where p.product_id is null
)

select * from bad_quantity
union all
select * from orphan_product
