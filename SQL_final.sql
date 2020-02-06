--Karl Glaub
--January 14, 2020


--Create a query that lists each movie, the film category it is classified in,
--and the number of times it has been rented out.
WITH cat AS (
	SELECT
		f.title AS film_title,
		c.name AS category
	FROM film f
	JOIN film_category fc
	ON f.film_id = fc.film_id
	JOIN category c
	ON fc.category_id = c.category_id
WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
ORDER BY 1),

rentals AS (
	SELECT
		f.title AS film_title,
		COUNT(r.rental_date) AS rentals_of_film
FROM film f
JOIN inventory i
ON f.film_id = i.film_id
JOIN rental r
ON i.inventory_id = r.inventory_id
GROUP BY 1
ORDER BY 1)

SELECT
	cat.film_title,
	cat.category,
	rentals.rentals_of_film
FROM cat
JOIN rentals
ON cat.film_title = rentals.film_title
ORDER BY 2,1
;



--Can you provide a table with the movie titles and divide them into 4 levels (first_quarter, second_quarter, third_quarter,
--and final_quarter) based on the quartiles (25%, 50%, 75%) of the rental duration for movies across all categories?
--How many Family films are in each quartile?
WITH all_cat_duration AS (
	SELECT
		NTILE(4) OVER (ORDER BY rental_duration) AS qtile,
		title,
		film_id,
		rental_duration
	FROM film),

fam_quartiles AS (
	SELECT
		f.title AS film_title,
		c.name AS category,
		f.qtile AS quartile,
		f.rental_duration AS duration
	FROM all_cat_duration f
	JOIN film_category fc
	ON f.film_id = fc.film_id
	JOIN category c
	ON fc.category_id = c.category_id
	WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
	ORDER BY 3,2)

SELECT
	quartile,
	COUNT(*) AS quartile_size
FROM fam_quartiles fq
GROUP BY 1
ORDER BY 1
;


--Can you write a query to capture the customer name,
--month and year of payment, and total payment amount for each month by these top 10 paying customers?
WITH top_ten AS (
	SELECT
		c.first_name || ' ' || c.last_name AS full_name,
		c.customer_id,
		SUM(p.amount) AS paid_amount
	FROM customer c
	JOIN payment p
	ON c.customer_id = p.customer_id
	GROUP BY 1,2
	ORDER BY 3 DESC
	LIMIT 10)

SELECT
	t.full_name,
	DATE_TRUNC('month',p.payment_date) AS month,
	COUNT(p.amount) AS payments,
	SUM(p.amount) AS paid_amount
FROM top_ten t
JOIN payment p
ON t.customer_id = p.customer_id
GROUP BY 1,2
ORDER BY 1,2
;


--I would like to find out the difference across their monthly payments during 2007.
--Please go ahead and write a query to compare the payment amounts in each successive month.
--Repeat this for each of these 10 paying customers.
--Also, it will be tremendously helpful if you can identify the customer name who paid the most difference in terms of payments.
WITH top_ten AS (
	SELECT
		c.first_name || ' ' || c.last_name AS full_name,
		c.customer_id,
		SUM(p.amount) AS paid_amount
	FROM customer c
	JOIN payment p
	ON c.customer_id = p.customer_id
	GROUP BY 1,2
	ORDER BY 3 DESC
	LIMIT 10),

monthly AS (
	SELECT
		t.full_name,
		DATE_TRUNC('month',p.payment_date) AS month,
		COUNT(p.amount) AS payments,
		SUM(p.amount) AS paid_amount
	FROM top_ten t
	JOIN payment p
	ON t.customer_id = p.customer_id
	GROUP BY 1,2
	ORDER BY 1,2)

SELECT
	m.full_name,
	m.month,
	m.paid_amount,
	LEAD(m.paid_amount) OVER (PARTITION BY m.full_name ORDER BY m.month) - paid_amount AS amount_difference
FROM monthly m
GROUP BY 1,2,3
ORDER BY 1,2
;
