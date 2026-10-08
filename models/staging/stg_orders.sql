-- Raw passthrough, duplicates included on purpose: deduping is the
-- intermediate layer's job, not staging's. Staging stays 1:1 with the source.
select
    order_id,
    customer_id,
    cast(order_date as date) as order_date,
    status,
    channel
from {{ ref('raw_orders') }}
