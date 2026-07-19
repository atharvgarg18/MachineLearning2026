# Lab 01 - Data Dictionary

## 1. Customers Table

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| customer_id | String | Unique identifier assigned to a customer for an order. | 06b8999e2fba1a1fbc88172c00ba8bc7 |
| customer_unique_id | String | Unique identifier representing the actual customer across multiple orders. | 861eff4711a542e4b93843c6dd7febb0 |
| customer_zip_code_prefix | Integer | ZIP code prefix of the customer's location. | 14409 |
| customer_city | String | Customer's city. | franca |
| customer_state | String | Customer's state. | SP |

---

## 2. Orders Table

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| order_id | String | Unique identifier for an order. | e481f51cbdc54678b7cc49136f2d6af7 |
| customer_id | String | Customer associated with the order. | 9ef432eb6251297304e76186b10a928d |
| order_status | String | Current status of the order. | delivered |
| order_purchase_timestamp | Datetime | Date and time when the order was placed. | 2017-10-02 10:56:33 |
| order_approved_at | Datetime | Date and time when the payment was approved. | 2017-10-02 11:07:15 |
| order_delivered_carrier_date | Datetime | Date and time when the order was handed to the carrier. | 2017-10-04 19:55:00 |
| order_delivered_customer_date | Datetime | Date and time when the customer received the order. | 2017-10-10 21:25:13 |
| order_estimated_delivery_date | Datetime | Estimated delivery date provided to the customer. | 2017-10-18 00:00:00 |

---

## 3. Order Items Table

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| order_id | String | Identifier of the order. | 00010242fe8c5a6d1ba2dd792cb16214 |
| order_item_id | Integer | Sequence number of the item within the order. | 1 |
| product_id | String | Identifier of the purchased product. | 4244733e06e7ecb4970a6e2683c13e61 |
| seller_id | String | Identifier of the seller. | 48436dade18ac8b2bce089ec2a041202 |
| shipping_limit_date | Datetime | Last date by which the seller should ship the item. | 2017-09-19 09:45:35 |
| price | Float | Price of the product. | 58.90 |
| freight_value | Float | Shipping cost charged for the item. | 13.29 |