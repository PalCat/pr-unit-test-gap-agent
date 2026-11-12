# Pricing Business Rules (source of truth for tests)

1. **Items:** price must be >= 0; quantity must be an integer >= 1. Otherwise raise `ValueError`.
2. **Subtotal:** sum of price x quantity, rounded to 2 decimals.
3. **Tier discount** (applied to the subtotal): standard 0%, silver 5%, gold 10%, platinum 15%. Unknown tier raises `ValueError`.
4. **Coupons** (applied AFTER the tier discount):
   - `SAVE10`: 10% off. Requires amount >= $50. Valid through 2026-12-31 inclusive.
   - `FLAT20`: $20 off. Requires amount >= $100. Never expires.
   - Unknown, expired, or below-minimum coupons raise `ValueError`.
   - A coupon never makes the amount negative.
5. **Shipping** (calculated on the amount AFTER discounts and coupon):
   - US: free if amount >= $100, otherwise $8.99.
   - Any other country: flat $24.99, regardless of amount.
6. **Order total:** amount after discounts and coupon, plus shipping, rounded to 2 decimals.
