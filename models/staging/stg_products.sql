select
    product_id,
    product_name,
    category,
    cast(unit_cost as numeric(10, 2)) as unit_cost,
    cast(unit_price as numeric(10, 2)) as unit_price
from {{ ref('raw_products') }}
