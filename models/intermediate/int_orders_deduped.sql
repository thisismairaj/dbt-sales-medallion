-- Collapses exact order_id duplicates (a re-extract style defect seeded into
-- raw_orders). Keeps the first-seen row per order_id; nothing is silently
-- dropped - int_orders_quarantine.sql is where rejected rows land, with why.
with ranked as (
    select
        *,
        row_number() over (
            partition by order_id order by order_date
        ) as rn
    from {{ ref('stg_orders') }}
)

select
    order_id,
    customer_id,
    order_date,
    status,
    channel
from ranked
where rn = 1
