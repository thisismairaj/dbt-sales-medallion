-- Bronze -> silver: cast + rename only, no business logic, same grain as the seed.
select
    customer_id,
    first_name,
    last_name,
    email,
    state,
    segment,
    cast(signup_date as date) as signup_date
from {{ ref('raw_customers') }}
