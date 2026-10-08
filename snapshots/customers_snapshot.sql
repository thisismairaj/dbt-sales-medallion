{% snapshot customers_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['segment', 'state'],
    )
}}

-- SCD Type 2 history of customers.segment / state. Re-running `dbt snapshot`
-- after a customer's segment changes in the source adds a new row here with
-- dbt_valid_from/dbt_valid_to, instead of overwriting the old value.
select * from {{ ref('stg_customers') }}

{% endsnapshot %}
