with rank_orders as (
select
customer_id
,rank() over(partition by order_id, customer_id order by order_date desc) as rank_purchase
,order_date
from transactions
)
, unique_orders as (
select *
from rank_orders
where 1=1
and rank_purchase = 1
)
select
customer_id 
,datediff(day, order_date, '2024-07-01') as recency_days
from unique_orders 