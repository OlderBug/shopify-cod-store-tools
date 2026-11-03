# Going international

Cash on delivery is not one country's habit. It is how small merchants
sell in Pakistan, India, Bangladesh, Nigeria, Egypt, the UAE, and many
other markets — where a customer trusts the parcel in their hands more
than a card form on a screen.

This toolkit therefore separates what is universal from what is local:

- **Universal:** a short, landmark-based address a courier can actually
  find; a reachable phone number; a clear order summary for final review;
  honest return-rate math that never guesses an unknown status.
- **Local, by country profile:** currency and symbol, mobile format,
  and whether a postal code belongs on the courier slip at all.
  Pakistan's courier slips leave ZIP empty; India's do not.

Supported today: PK, IN, BD, NG, EG, AE. See
`store_tools/countries.py` — adding a country is adding one profile,
with a currency, a phone pattern, and a landmark hint.

## Why this matters

A returned parcel is not just a lost sale. It is fabric sent out,
courier fees paid twice, and a customer who may never order again.
For a small store, a few bad addresses a week can erase the month's
profit. Tools that catch a bad address *before* dispatch, label a
colour clearly *before* a customer guesses wrong, and show the real
return rate *without* hiding unknown parcels, are how a small merchant
stays in business — and grows into a brand customers trust.

That is the mission here: boring, correct tools, in public, for the
merchants who do not have a big tech team.
