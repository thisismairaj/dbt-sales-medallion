select
    order_date,
    channel,
    count(distinct order_id) as order_count,
    sum(line_amount) as revenue
from {{ ref('fct_order_items') }}
group by order_date, channel
