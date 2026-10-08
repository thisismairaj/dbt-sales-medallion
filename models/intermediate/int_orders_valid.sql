-- Silver: the rows that passed every check. This, not stg_orders, is what
-- the gold layer builds on.
select o.*
from {{ ref('int_orders_deduped') }} as o
where o.order_id not in (select order_id from {{ ref('int_orders_quarantine') }})
