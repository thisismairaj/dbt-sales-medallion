"""
Generates the synthetic raw seed data for this project (seeds/raw_*.csv).

This is a sales dataset that does not exist anywhere - no customers, no real
orders. It is built on purpose with a known set of defects seeded into it
(orphan foreign keys, duplicate rows, bad quantities), so the dbt tests in
this project have something real to catch instead of passing trivially on
clean data.

Deterministic (fixed random seed) so re-running this script reproduces the
exact same CSVs and the exact same defect counts documented in the README.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

SEEDS_DIR = Path(__file__).resolve().parent.parent / "seeds"

SEGMENTS = ["retail", "wholesale", "vip"]
STATES = ["CA", "NY", "TX", "WA", "IL", "MA", "CO", "GA"]
CATEGORIES = ["electronics", "home", "apparel", "sporting_goods", "office"]
CHANNELS = ["web", "mobile_app", "phone", "in_store"]
STATUSES = ["placed", "shipped", "delivered", "cancelled"]

N_CUSTOMERS = 40
N_PRODUCTS = 15
N_ORDERS = 250

# Seeded defects - counted here, not guessed, so README numbers stay honest.
N_ORPHAN_ORDERS = 5          # orders.customer_id points at no customer
N_DUPLICATE_ORDERS = 3       # order_id repeated (re-extract style duplicate)
N_BAD_QUANTITY_ITEMS = 8     # order_items.quantity <= 0
N_ORPHAN_ITEMS = 2           # order_items.product_id points at no product


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def gen_customers():
    rows = []
    start = date(2022, 1, 1)
    for i in range(1, N_CUSTOMERS + 1):
        signup = start + timedelta(days=random.randint(0, 900))
        rows.append([
            i,
            f"First{i}",
            f"Last{i}",
            f"customer{i}@example.com",
            random.choice(STATES),
            random.choice(SEGMENTS),
            signup.isoformat(),
        ])
    return rows


def gen_products():
    rows = []
    for i in range(1, N_PRODUCTS + 1):
        cost = round(random.uniform(5, 150), 2)
        margin = random.uniform(1.3, 2.2)
        rows.append([
            i,
            f"Product {i}",
            random.choice(CATEGORIES),
            cost,
            round(cost * margin, 2),
        ])
    return rows


def gen_orders(valid_customer_ids):
    rows = []
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)
    span = (end - start).days

    for i in range(1, N_ORDERS + 1):
        order_date = start + timedelta(days=random.randint(0, span))
        rows.append([
            i,
            random.choice(valid_customer_ids),
            order_date.isoformat(),
            random.choice(STATUSES),
            random.choice(CHANNELS),
        ])

    # Seed orphan orders: customer_id with no matching customer row.
    orphan_customer_ids = range(9000, 9000 + N_ORPHAN_ORDERS)
    next_id = N_ORDERS + 1
    for cust_id in orphan_customer_ids:
        order_date = start + timedelta(days=random.randint(0, span))
        rows.append([next_id, cust_id, order_date.isoformat(),
                     random.choice(STATUSES), random.choice(CHANNELS)])
        next_id += 1

    # Seed duplicate order_id rows (same id re-appears, as from a re-extract).
    for order in random.sample(rows[:N_ORDERS], N_DUPLICATE_ORDERS):
        rows.append(list(order))

    random.shuffle(rows)
    return rows


def gen_order_items(order_ids, valid_product_ids):
    rows = []
    item_id = 1
    for order_id in order_ids:
        for _ in range(random.randint(1, 4)):
            product_id = random.choice(valid_product_ids)
            qty = random.randint(1, 5)
            unit_price = round(random.uniform(5, 300), 2)
            rows.append([item_id, order_id, product_id, qty, unit_price])
            item_id += 1

    # Seed bad quantities (<= 0) on existing item rows.
    bad_idxs = random.sample(range(len(rows)), N_BAD_QUANTITY_ITEMS)
    for idx in bad_idxs:
        rows[idx][3] = random.choice([0, -1, -2])

    # Seed orphan product_id references.
    orphan_idxs = random.sample(
        [i for i in range(len(rows)) if i not in bad_idxs], N_ORPHAN_ITEMS
    )
    for idx in orphan_idxs:
        rows[idx][2] = 9999

    return rows


def main():
    SEEDS_DIR.mkdir(parents=True, exist_ok=True)

    customers = gen_customers()
    products = gen_products()
    valid_customer_ids = [c[0] for c in customers]
    valid_product_ids = [p[0] for p in products]

    orders = gen_orders(valid_customer_ids)
    order_ids = [o[0] for o in orders]
    order_items = gen_order_items(order_ids, valid_product_ids)

    write_csv(SEEDS_DIR / "raw_customers.csv",
              ["customer_id", "first_name", "last_name", "email", "state",
               "segment", "signup_date"], customers)
    write_csv(SEEDS_DIR / "raw_products.csv",
              ["product_id", "product_name", "category", "unit_cost",
               "unit_price"], products)
    write_csv(SEEDS_DIR / "raw_orders.csv",
              ["order_id", "customer_id", "order_date", "status", "channel"],
              orders)
    write_csv(SEEDS_DIR / "raw_order_items.csv",
              ["order_item_id", "order_id", "product_id", "quantity",
               "unit_price"], order_items)

    print(f"customers:   {len(customers)}")
    print(f"products:    {len(products)}")
    print(f"orders:      {len(orders)} (incl. {N_ORPHAN_ORDERS} orphan customer_id, "
          f"{N_DUPLICATE_ORDERS} duplicate order_id)")
    print(f"order_items: {len(order_items)} (incl. {N_BAD_QUANTITY_ITEMS} bad quantity, "
          f"{N_ORPHAN_ITEMS} orphan product_id)")


if __name__ == "__main__":
    main()
