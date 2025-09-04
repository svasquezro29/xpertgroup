select 
category
,sum(order_amount) as revenue
from transactions
where 1=1
and order_date between '2024-07-01'- interval '30d' and '2024-07-01'
group by 1
order by 2 desc