# Shopify COD Store Tools

A practical, open toolkit for cash-on-delivery stores around the world
— built from the daily workflow of a real Faisalabad suiting store
(faatehstore.com), and made to travel.

## Why this exists

A returned parcel is not just a lost sale. It is goods sent out,
courier fees paid twice, and a customer who may never order again.
For a small merchant, a few bad addresses a week can erase a month's
profit.

COD is how millions of people buy online in Pakistan, India,
Bangladesh, Nigeria, Egypt, and beyond — where trust is built at the
doorstep, not in a card form. This toolkit exists for those merchants:
boring, correct tools, in public, that catch a bad address before
dispatch, label a colour clearly before a customer guesses wrong, and
show the real return rate without hiding the parcels nobody knows
about. Small stores deserve good tools too.

## What it does

1. **Product image colour labels** — stamps `COLOR: POLO BLUE` on a
   product photo, small and bold, in a bottom corner, with no
   background bar and no extra canvas. The image keeps its exact size.
2. **COD order checklist** — checks an order before it goes to the
   courier: valid Pakistani mobile, short landmark-based address,
   ZIP field empty, payment COD, cart note `OK WA`, and line items
   present. It prints a one-line summary for final review.
3. **Return-rate calculator** — reads a Shopify orders CSV and reports
   delivered vs returned counts, return rate, and returned amount.
   Rows with an unknown status are listed separately, never guessed.
4. **Parcel classifier** — buckets parcels as normal, stuck 48h+,
   never picked up, delivered, returned, or return pipeline, from a
   simple timeline export.

## Install and use

```bash
pip install -r requirements.txt

python -m store_tools.cli label in.jpg out.jpg --color "Polo Blue"
python -m store_tools.cli check-order examples/order.json
python -m store_tools.cli check-order examples/order-india.json --country IN
python -m store_tools.cli returns examples/orders.csv
```

Countries supported today: PK, IN, BD, NG, EG, AE — see
`docs/INTERNATIONAL.md` for how to add a new one.

Run the tests:

```bash
python -m pytest tests/ -q
```

## Status — read this honestly

This project started in November 2026. It is new, small, and has no
users, stars, or releases yet beyond its first version. It is published
so other COD merchants can use and improve it, and so its maintenance
history is public and verifiable.

It does **not** claim broad adoption, and it is not, on its own, a
claim to any maintainer programme. Any application made with it should
say exactly that: a new tool, built from a real store workflow, being
maintained in public.

## License

MIT. See `LICENSE`.
