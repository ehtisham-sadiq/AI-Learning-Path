-- 1.

-- SELECT * FROM actor
-- WHERE last_name LIKE 'A%'

-- 2.

-- SELECT title, first_name, last_name FROM film
-- JOIN film_actor ON film.film_id = film_actor.film_id
-- JOIN actor ON film_actor.actor_id = actor.actor_id
-- ORDER BY film.film_id ASC

-- 3.

-- SELECT category.name, COUNT(*) as genre_count FROM category
-- JOIN film_category ON category.category_id = film_category.category_id
-- GROUP BY category.name
-- ORDER BY genre_count DESC

-- 4.

-- SELECT store.store_id, COUNT(*) FROM store
-- JOIN inventory ON store.store_id = inventory.store_id
-- GROUP BY store.store_id

-- 5.

-- SELECT DISTINCT rental.customer_id, customer.first_name, customer.last_name, customer.email FROM rental
-- JOIN inventory ON rental.inventory_id = inventory.inventory_id
-- JOIN film_category ON inventory.film_id = film_category.film_id
-- JOIN category ON film_category.category_id = category.category_id
-- JOIN customer ON rental.customer_id = customer.customer_id
-- WHERE category.name LIKE 'Comedy'
-- ORDER BY last_name ASC

-- 6.

-- SELECT film.title, COUNT(*) as rental_count FROM film
-- JOIN inventory ON film.film_id = inventory.film_id
-- JOIN rental ON inventory.inventory_id = rental.inventory_id
-- GROUP BY film.title
-- ORDER BY rental_count DESC

-- 7.

-- SELECT title, rental_date FROM rental
-- JOIN inventory ON rental.inventory_id = inventory.inventory_id
-- JOIN film ON inventory.film_id = film.film_id
-- WHERE EXTRACT(YEAR FROM rental_date) = 2022

-- 8.

-- SELECT category_id, AVG(return_date - rental_date) AS rental_time FROM film_category
-- JOIN inventory ON film_category.film_id = inventory.film_id 
-- JOIN rental ON inventory.inventory_id = rental.inventory_id
-- GROUP BY category_id
-- ORDER BY rental_time DESC

-- 9.

-- SELECT title, name FROM film
-- JOIN film_category ON film.film_id = film_category.film_id
-- JOIN category ON film_category.category_id = category.category_id
-- ORDER BY title

-- 10.

-- SELECT inventory.inventory_id, film_id FROM inventory
-- LEFT JOIN rental ON inventory.inventory_id = rental.inventory_id
-- WHERE rental.inventory_id IS NULL

-- 11.

-- SELECT payment_sum.customer_id, first_name, last_name, sum 
-- FROM (SELECT customer_id, SUM(amount) FROM payment GROUP BY customer_id) AS payment_sum
-- JOIN customer ON customer.customer_id = payment_sum.customer_id
-- ORDER BY sum DESC

-- 12.

-- SELECT first_name, last_name, film_num FROM (SELECT actor_id, COUNT(film_id) AS film_num FROM film_actor GROUP BY actor_id) AS film_count
-- JOIN actor ON film_count.actor_id = actor.actor_id
-- WHERE film_num > 10
-- ORDER BY last_name ASC

-- 13. 

-- SELECT film.title, film_revenue.count, film_revenue.rental_sum FROM 
-- 	(
-- 	SELECT inventory.film_id, COUNT(rental.rental_id), SUM(payment.amount) as rental_sum FROM inventory
-- 	JOIN rental ON inventory.inventory_id = rental.inventory_id
-- 	JOIN payment ON rental.rental_id = payment.rental_id
-- 	GROUP BY inventory.film_id
-- 	) AS film_revenue
-- JOIN film ON film_revenue.film_id = film.film_id
-- ORDER BY rental_sum DESC

-- 14. 

-- SELECT * FROM film WHERE film.rating IN 
-- 	(
-- 	SELECT rating FROM 
-- 		(
-- 		SELECT film.rating, COUNT(*) as rating_count FROM film
-- 		GROUP BY rating
-- 		) AS rating_group
-- 	WHERE rating_group.rating_count > 1
-- 	)

-- 15.

-- SELECT customer_id, COUNT(*) as rental_count FROM rental
-- GROUP BY customer_id
-- ORDER BY rental_count DESC

-- 16.

-- SELECT first_name, last_name, city, country FROM staff
-- JOIN store ON staff.store_id = store.store_id
-- JOIN address ON address.address_id = store.address_id
-- JOIN city ON city.city_id = address.city_id
-- JOIN country ON country.country_id = city.country_id

-- 17.

-- SELECT category.name, category_payment.average_payment FROM
-- 	(
-- 	SELECT category_id, AVG(payment.amount) as average_payment FROM film_category
-- 	JOIN inventory ON inventory.film_id = film_category.film_id
-- 	JOIN rental ON rental.inventory_id = inventory.inventory_id
-- 	JOIN payment ON payment.rental_id = rental.rental_id
-- 	GROUP BY category_id
-- 	) AS category_payment
-- JOIN category ON category.category_id = category_payment.category_id
-- ORDER BY category.category_id

-- 18.

-- SELECT title, COUNT(*) AS rental_count FROM film
-- JOIN inventory ON inventory.film_id = film.film_id
-- JOIN rental ON rental.inventory_id = inventory.inventory_id
-- GROUP BY title
-- ORDER BY rental_count DESC

-- 19. 

-- SELECT store_revenue.store_id, store_revenue.payment_sum, address FROM
-- 	(
-- 	SELECT store.store_id, SUM(payment.amount) AS payment_sum FROM payment
-- 	JOIN rental ON rental.rental_id = payment.rental_id
-- 	JOIN inventory ON inventory.inventory_id = rental.inventory_id
-- 	JOIN store ON store.store_id = inventory.store_id
-- 	GROUP BY store.store_id
-- 	) AS store_revenue
-- JOIN store ON store.store_id = store_revenue.store_id
-- JOIN address ON address.address_id = store.address_id

-- 20.

