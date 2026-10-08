-- Gold, line-item grain. Only built from the *_valid intermediate models,
-- so nothing quarantined upstream can reach here.
select
    i.order_item_id,
    i.order_id,
    o.customer_id,
    i.product_id,
    o.order_date,
    o.status,
    o.channel,
    i.quantity,
    i.unit_price,
    round(i.quantity * i.unit_price, 2) as line_amount
from {{ ref('int_order_items_valid') }} as i
inner join {{ ref('int_orders_valid') }} as o
    on i.order_id = o.order_id
