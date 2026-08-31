-- Bank Analytics SQL Portfolio
-- 30 selected queries from the original practice file
-- Database: bank_analytics

USE bank_analytics;

-- 1. Count customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Count distinct customer cities
SELECT COUNT(DISTINCT city) AS total_cities
FROM customers;

-- 3. Customers from Tamil Nadu
SELECT customer_name, city
FROM customers
WHERE state = 'tamil nadu';

-- 4. Female customers
SELECT customer_name, gender
FROM customers
WHERE gender = 'female';

-- 5. Customers with balance above 50,000
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM accounts
    WHERE balance > 50000
);

-- 6. Customer with the highest account balance
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM accounts
    WHERE balance = (SELECT MAX(balance) FROM accounts)
);

-- 7. Total transaction amount by customer
SELECT c.customer_name, SUM(t.amount) AS total_amount
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_name;

-- 8. Maximum transaction amount by customer
SELECT c.customer_name, MAX(t.amount) AS max_transaction_amount
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_name;

-- 9. Total transactions by customer
SELECT c.customer_name, COUNT(*) AS transaction_count
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_name;

-- 10. Customers with at least 3 transactions
SELECT c.customer_name, COUNT(*) AS transaction_count
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_name
HAVING COUNT(*) >= 3;

-- 11. Total deposits by customer
SELECT c.customer_name, SUM(t.amount) AS total_deposit
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'deposit'
GROUP BY c.customer_name;

-- 12. Total withdrawals by customer
SELECT c.customer_name, SUM(t.amount) AS total_withdrawal
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'withdrawal'
GROUP BY c.customer_name;

-- 13. Transaction amount by transaction type
SELECT transaction_type, SUM(amount) AS total_amount
FROM transactions
GROUP BY transaction_type;

-- 14. Total balance by account type
SELECT account_type, SUM(balance) AS total_balance
FROM accounts
GROUP BY account_type;

-- 15. Top 3 customers by total transaction amount
SELECT c.customer_name, SUM(t.amount) AS total_amount
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY c.customer_name
ORDER BY total_amount DESC
LIMIT 3;

-- 16. Customers with no accounts
SELECT c.customer_name
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
WHERE a.customer_id IS NULL;

-- 17. Customers with total balance above 100,000
WITH high_balance AS (
    SELECT c.customer_name, SUM(a.balance) AS total_balance
    FROM customers c
    JOIN accounts a ON c.customer_id = a.customer_id
    GROUP BY c.customer_name
    HAVING SUM(a.balance) > 100000
)
SELECT *
FROM high_balance;

-- 18. Rank accounts by balance
SELECT account_id,
       balance,
       RANK() OVER (ORDER BY balance DESC) AS balance_rank
FROM accounts;

-- 19. Dense rank accounts by balance
SELECT account_id,
       balance,
       DENSE_RANK() OVER (ORDER BY balance DESC) AS balance_rank
FROM accounts;

-- 20. Row number for each transaction within an account
SELECT account_id,
       transaction_date,
       ROW_NUMBER() OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS transaction_number
FROM transactions;

-- 21. Previous transaction amount
SELECT account_id,
       amount,
       transaction_date,
       LAG(amount) OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS previous_amount
FROM transactions;

-- 22. Next transaction amount
SELECT account_id,
       amount,
       transaction_date,
       LEAD(amount) OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS next_amount
FROM transactions;

-- 23. Difference from previous transaction
SELECT account_id,
       amount,
       LAG(amount) OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS previous_amount,
       amount - LAG(amount) OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS difference
FROM transactions;

-- 24. Running transaction total by account
SELECT account_id,
       transaction_date,
       amount,
       SUM(amount) OVER (
           PARTITION BY account_id
           ORDER BY transaction_date
       ) AS running_total
FROM transactions;

-- 25. Average balance by account type
SELECT account_id,
       account_type,
       balance,
       AVG(balance) OVER (
           PARTITION BY account_type
       ) AS average_balance
FROM accounts;

-- 26. Highest balance by account type
SELECT account_id,
       account_type,
       balance,
       MAX(balance) OVER (
           PARTITION BY account_type
       ) AS highest_balance
FROM accounts;

-- 27. Difference from account-type average
SELECT account_id,
       account_type,
       balance,
       balance - AVG(balance) OVER (
           PARTITION BY account_type
       ) AS difference_from_average
FROM accounts;

-- 28. Customer signup year
SELECT customer_name,
       YEAR(signup_date) AS signup_year
FROM customers;

-- 29. Customer signup month name
SELECT customer_name,
       MONTHNAME(signup_date) AS signup_month
FROM customers;

-- 30. Latest transaction for each account
SELECT account_id, amount, transaction_date
FROM (
    SELECT account_id,
           amount,
           transaction_date,
           ROW_NUMBER() OVER (
               PARTITION BY account_id
               ORDER BY transaction_date DESC
           ) AS rn
    FROM transactions
) t
WHERE rn = 1;
