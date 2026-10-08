select i.*
from {{ ref('stg_order_items') }} as i
where i.order_item_id not in (
    select order_item_id from {{ ref('int_order_items_quarantine') }}
)
