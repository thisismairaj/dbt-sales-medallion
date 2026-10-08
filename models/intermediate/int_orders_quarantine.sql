-- Orders whose customer_id has no matching customer - quarantined with a
-- reason instead of being joined away silently (data-lab2's quarantine rule,
-- done here as a dbt model instead of a hand-maintained table).
select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    o.channel,
    'customer_id not found in stg_customers' as quarantine_reason
from {{ ref('int_orders_deduped') }} as o
left join {{ ref('stg_customers') }} as c
    on o.customer_id = c.customer_id
where c.customer_id is null
