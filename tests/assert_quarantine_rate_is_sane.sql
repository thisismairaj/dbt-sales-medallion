-- The gate: if more than 10% of orders are getting quarantined, that's not
-- "data quality is working as designed" anymore, it's "something upstream
-- broke" - this test returns rows (and fails the build) when that happens.
with counts as (
    select
        (select count(*) from {{ ref('int_orders_deduped') }}) as total_orders,
        (select count(*) from {{ ref('int_orders_quarantine') }}) as quarantined_orders
)

select *
from counts
where quarantined_orders::float / total_orders > 0.10
