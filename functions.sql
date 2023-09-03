-- ������� ���� ������
DROP FUNCTION IF EXISTS clear_all_tables();
CREATE FUNCTION clear_all_tables()
	RETURNS void AS
	$$
	DELETE FROM Worker;
	DELETE FROM ContactInformation;
	DELETE FROM ClientInformation;
	DELETE FROM Clothes;
	DELETE FROM Buying;
	DELETE FROM Clients;
	$$

LANGUAGE sql;


DROP FUNCTION IF EXISTS clear_worker();
CREATE FUNCTION clear_worker()
  RETURNS void AS
  $$
  DELETE FROM Worker;
  DELETE FROM ContactInformation;
  $$
LANGUAGE sql;

DROP FUNCTION IF EXISTS clear_clients();
CREATE FUNCTION clear_clients()
  RETURNS void AS
  $$
  DELETE FROM Clients;
  DELETE FROM ClientInformation;
  $$
LANGUAGE sql;

DROP FUNCTION IF EXISTS clear_buying();
CREATE FUNCTION clear_buying()
	RETURNS void AS
	$$
	DELETE FROM Buying;
	$$
LANGUAGE sql;

DROP FUNCTION IF EXISTS clear_contact_information();
CREATE FUNCTION clear_contact_information()
	RETURNS void AS
	$$
	DELETE FROM ContactInformation;
	$$
LANGUAGE sql;

DROP FUNCTION IF EXISTS clear_contact_information_c();
CREATE FUNCTION clear_contact_information_c()
	RETURNS void AS
	$$
	DELETE FROM ClientInformation;
	$$
LANGUAGE sql;


DROP FUNCTION IF EXISTS clear_clothes();
CREATE FUNCTION clear_clothes()
	RETURNS void AS
	$$
	DELETE FROM clothes;
	$$
LANGUAGE sql;


--ContactInformation W
DROP FUNCTION IF EXISTS add_to_contact_information(INTEGER, VARCHAR(40), VARCHAR(20));
CREATE FUNCTION add_to_contact_information(in_id INTEGER, in_name VARCHAR(40), in_phone_number VARCHAR(20)) -- in �������� input
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT ci.id FROM ContactInformation ci WHERE ci.id = in_id) THEN
			RAISE NOTICE 'Contact information with id % already exists', in_id;
			RETURN 0;
		ELSE
			INSERT INTO ContactInformation(id, name,  phone_number)
			VALUES (in_id, in_name, in_phone_number);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;

--ContactInformation C
DROP FUNCTION IF EXISTS add_to_contact_informationC(INTEGER, VARCHAR(20), VARCHAR(40));
CREATE FUNCTION add_to_contact_informationC(in_id INTEGER, in_phone_number VARCHAR(20), in_email VARCHAR(40)) -- in �������� input
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT cic.id FROM ClientInformation cic WHERE cic.id = in_id) THEN
			RAISE NOTICE 'Contact information with id % already exists', in_id;
			RETURN 0;
		ELSE
			INSERT INTO ClientInformation(id, phone_number, email)
			VALUES (in_id, in_phone_number, in_email);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_to_clothes(INTEGER, VARCHAR(40), VARCHAR(5), VARCHAR(20), INTEGER);
CREATE FUNCTION add_to_clothes(in_id INTEGER, in_name VARCHAR(40), in_size_clothes VARCHAR(5),
                                                        in_color VARCHAR(20), in_price INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT c.id FROM clothes c WHERE c.id = in_id) THEN
			RAISE NOTICE 'Clothes with id % already exists', in_id;
			RETURN 0;
		ELSE
			INSERT INTO clothes (id, name, size_clothes, color, price)
			VALUES (in_id, in_name, in_size_clothes, in_color, in_price);
			RETURN 1;
		END IF;
	END;
	$$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_to_worker(VARCHAR(40), INTEGER, VARCHAR(20), VARCHAR(40));
CREATE FUNCTION add_to_worker(in_post VARCHAR(40), in_salary INTEGER, in_phone_number VARCHAR(20), in_name VARCHAR(40) )
	RETURNS INTEGER AS
	$$
	BEGIN
		IF NOT EXISTS (SELECT ci.id FROM ContactInformation ci WHERE (ci.phone_number = in_phone_number and ci.name = in_name)) THEN
        INSERT INTO ContactInformation(phone_number, name)
        VALUES(in_phone_number, in_name);

    		INSERT INTO Worker (post, salary, contact)
    		VALUES
    		(
    			in_post,
    			in_salary,
    			(SELECT ci.id  FROM ContactInformation ci WHERE ci.phone_number = in_phone_number and ci.name = in_name)
    		);
    		RETURN 1;
  	ELSE RAISE NOTICE 'Worker with phone_number % already exists', in_phone_number;
			    RETURN 0;
		END IF;
	END;
	$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS add_to_clients(VARCHAR(40), VARCHAR(20), VARCHAR(40));
CREATE FUNCTION add_to_clients(in_full_name VARCHAR(40), in_phone_number VARCHAR(20), in_email VARCHAR(40))
  RETURNS INTEGER AS
  $$
  BEGIN
    IF NOT EXISTS (SELECT cic.id FROM ClientInformation cic WHERE (cic.name = in_full_name and cic.phone_number = in_phone_number and cic.email = in_email)) THEN
            INSERT INTO ClientInformation(name, phone_number,  email)
            VALUES(in_full_name, in_phone_number,  in_email);

            INSERT INTO Clients (full_name, telephone)
            VALUES
            (
                in_full_name,
                (SELECT cic.id  FROM ClientInformation cic WHERE  cic.name = in_full_name and cic.phone_number = in_phone_number and cic.email = in_email)
            );
           RETURN 1;
    ELSE RAISE NOTICE 'Client with name % already exists', in_full_name;
         RETURN 0;
    END IF;
  END;
  $$ LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS add_to_buying(VARCHAR(40), VARCHAR(40), VARCHAR(5), INTEGER, INTEGER, VARCHAR(40), VARCHAR(40));
CREATE FUNCTION add_to_buying(in_full_name VARCHAR(40), in_product VARCHAR(40),
                              in_size_ VARCHAR(5), in_price INTEGER, in_discount INTEGER,
                              in_date_buy VARCHAR(40), in_where_buy VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN
		IF NOT EXISTS (SELECT b.id FROM Buying b WHERE ( b.product = in_product
		                                                and b.size_ = in_size_
		                                                and b.price = in_price
		                                                and b.discount = in_discount
		                                                and b.date_buy = in_date_buy
		                                                and b.where_buy = in_where_buy)) THEN
        INSERT INTO Buying(product, size_,  price, discount, date_buy, where_buy)
        VALUES(in_product, in_size_,  in_price, in_discount, in_date_buy, in_where_buy);


    		INSERT INTO Clients (full_name, clothes_c)
    		VALUES
    		(
    			in_full_name,
    			(SELECT b.id FROM Buying b WHERE ( b.product = in_product
    		                                                and b.size_ = in_size_
    		                                                and b.price = in_price
    		                                                and b.discount = in_discount
    		                                                and b.date_buy = in_date_buy
    		                                                and b.where_buy = in_where_buy))
    		);
		    RETURN 1;
		ELSE RAISE NOTICE 'Buyng with name % already exists', in_full_name;
			    RETURN 0;
		END IF;
	END;
	$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS search_clothes_by_name(VARCHAR(40));
CREATE FUNCTION search_clothes_by_name(in_name VARCHAR(40))
	RETURNS TABLE (id INTEGER, name VARCHAR(40), size_clothes VARCHAR(5),
                                         color VARCHAR(20), price INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT c.name FROM clothes c WHERE c.name = in_name) THEN
			RETURN QUERY
				SELECT * FROM clothes c
				WHERE c.name=in_name;
		ELSE
			RAISE NOTICE 'Clothes with name % does not exist', in_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_contact_by_name(VARCHAR(40));
CREATE FUNCTION search_contact_by_name(in_name VARCHAR(40))

	RETURNS TABLE (id INTEGER,	name VARCHAR(40), phone_number VARCHAR(20)) AS
	$$
	BEGIN
		IF EXISTS (SELECT ci.name FROM ContactInformation ci WHERE ci.name = in_name) THEN
			RETURN QUERY
				SELECT * FROM ContactInformation ci
				WHERE ci.name=in_name;
		ELSE
			RAISE NOTICE 'Contact Information with name % does not exist', in_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS search_client_by_name(VARCHAR(40));
CREATE FUNCTION search_client_by_name(in_full_name VARCHAR(40))

	RETURNS TABLE (id INTEGER,	full_name VARCHAR(40), phone_number VARCHAR(20), email VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT cli.name FROM ClientInformation cli WHERE cli.name = in_full_name) THEN
			RETURN QUERY
				SELECT * FROM ClientInformation cli
				WHERE cli.name=in_full_name;
		ELSE
			RAISE NOTICE 'Contact Information with name % does not exist', in_full_name;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS update_buying(INTEGER, VARCHAR(40), VARCHAR(5), INTEGER, INTEGER, VARCHAR(40), VARCHAR(40));
CREATE FUNCTION update_buying(in_id INTEGER, in_product VARCHAR(40),
                              in_size_ VARCHAR(5), in_price INTEGER, in_discount INTEGER,
                              in_date_buy VARCHAR(40), in_where_buy VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT b.id FROM buying b WHERE b.id = in_id) THEN
				IF (in_product <> '') THEN
					UPDATE buying b
					SET product = in_product
					WHERE id = in_id;
				END IF;
				IF (in_size_ <> '') THEN
					UPDATE buying
					SET size_ = in_size_
					WHERE id = in_id;
				END IF;
				IF (in_price <> -1) THEN
					UPDATE buying
					SET price = in_price
					WHERE id = in_id;
				END IF;
				IF (in_discount <> -1) THEN
					UPDATE buying
					SET discount = in_discount
					WHERE id = in_id;
				END IF;
				IF (in_date_buy <> '') THEN
					UPDATE buying
					SET date_buy = in_date_buy
					WHERE id = in_id;
				END IF;
				IF (in_where_buy  <> '') THEN
					UPDATE buying
					SET where_buy  = in_where_buy
					WHERE id = in_id;
				END IF;
				RETURN 1;
		ELSE
			RAISE NOTICE 'Buying with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;
--DROP FUNCTION IF EXISTS update_worker(INTEGER, VARCHAR(20), INTEGER, INTEGER);
--CREATE FUNCTION update_worker(in_id INTEGER, in_post VARCHAR(20), in_salary INTEGER, in_contact_information INTEGER)
--	RETURNS INTEGER AS
--	$$
--	BEGIN
--		IF EXISTS (SELECT w.id FROM worker w WHERE w.id = in_id) THEN
--			IF (in_contact_information <> -1) AND NOT EXISTS (SELECT ci.id FROM ContactInformation ci WHERE ci.id = in_contact_information) THEN
--				RAISE NOTICE 'Contact Information % does not exist', in_contact_information;
--				RETURN 0;
--			ELSE
--				IF (in_post  <> '') THEN
--					UPDATE worker
--					SET post = in_post
--					WHERE id = in_id;
--				END IF;
--				IF (in_salary <> -1) THEN
--					UPDATE worker
--					SET salary = in_salary
--					WHERE id = in_id;
--				END IF;
--				IF (in_contact_information <> -1) THEN
--					UPDATE worker
--					SET contact_information = in_contact_information
--					WHERE id = in_id;
--				END IF;
--
--				RETURN 1;
--			END IF;
--		ELSE
--			RAISE NOTICE 'Worker with id % does not exist', in_id;
--			RETURN 0;
--		END IF;
--	END;
--	$$
--LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_clothes_by_name(VARCHAR(40));
CREATE FUNCTION delete_clothes_by_name(in_name VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT c.name FROM clothes c WHERE c.name = in_name) THEN
			DELETE FROM clothes c
			WHERE c.name = in_name;
			RETURN 1;
		ELSE
			RAISE NOTICE 'Clothe with name % does not exist', in_name;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS delete_worker_by_id(INTEGER);
CREATE FUNCTION delete_worker_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT w.id FROM worker w WHERE w.id = in_id) THEN
			DELETE FROM worker w
			WHERE w.id = in_id;
			DELETE FROM ContactInformation u
			WHERE u.id = in_id;
			RETURN 1;
		ELSE
			RAISE NOTICE 'Worker with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS delete_client_by_id(INTEGER);
CREATE FUNCTION delete_client_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT c.id FROM clients c WHERE c.id = in_id) THEN
			DELETE FROM clients c
			WHERE c.id = in_id;
			DELETE FROM ClientInformation r
			WHERE r.id = in_id;
			RETURN 1;
		ELSE
			RAISE NOTICE 'Worker with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;



DROP FUNCTION IF EXISTS delete_contact_information_by_name(VARCHAR(40));
CREATE FUNCTION delete_contact_information_by_name(in_name VARCHAR(40))
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT ci.name FROM ContactInformation ci WHERE ci.name = in_name) THEN
			DELETE FROM ContactInformation ci
			WHERE ci.name = in_name;
			RETURN 1;
		ELSE
			RAISE NOTICE 'Contact Information with id % does not exist', in_name;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;



DROP FUNCTION IF EXISTS delete_buying_by_id(INTEGER);
CREATE FUNCTION delete_buying_by_id(in_id INTEGER)
	RETURNS INTEGER AS
	$$
	BEGIN
		IF EXISTS (SELECT b.id FROM buying b WHERE b.id = in_id) THEN
			DELETE FROM buying b
			WHERE b.id = in_id;
			RETURN 1;
		ELSE
			RAISE NOTICE 'Worker with id % does not exist', in_id;
			RETURN 0;
		END IF;
	END;
	$$
LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS print_table_clothes();
CREATE FUNCTION print_table_clothes()
	RETURNS TABLE (id INTEGER,  name VARCHAR(40), size_clothes VARCHAR(5), color VARCHAR(20), cost INTEGER) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM clothes) THEN
			RETURN QUERY
				SELECT * FROM clothes;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS print_table_clients();
CREATE FUNCTION print_table_clients()
	RETURNS TABLE (full_name VARCHAR(40), phone_number VARCHAR(20), email VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM Clients) THEN
			RETURN QUERY
				SELECT Clients.full_name, ClientInformation.phone_number, ClientInformation.email
                FROM ClientInformation
                JOIN Clients On Clients.telephone = ClientInformation.id;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS print_table_worker();
CREATE FUNCTION print_table_worker()
	RETURNS TABLE (post VARCHAR(20), salary INTEGER, phone_number VARCHAR(20), name VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM worker) THEN
			RETURN QUERY
				SELECT Worker.post, Worker.salary, ContactInformation.phone_number, ContactInformation.name
                FROM ContactInformation
                JOIN Worker On Worker.contact = ContactInformation.id;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS print_table_buying();
CREATE FUNCTION print_table_buying()
	RETURNS TABLE (in_full_name VARCHAR(40), in_product VARCHAR(40),
                              in_size_ VARCHAR(5), in_price INTEGER, in_discount INTEGER,
                              in_date_buy VARCHAR(40), in_where_buy VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM buying) THEN
			RETURN QUERY
				SELECT Clients.full_name, Buying.product, Buying.size_, Buying.price, Buying.discount, Buying.date_buy, Buying.where_buy
                    FROM Buying
                    JOIN Clients On Clients.clothes_c = Buying.id;

		ELSE RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS print_table_ContactInformation();
CREATE FUNCTION print_table_ContactInformation()
	RETURNS TABLE (id INTEGER, name VARCHAR(40), number VARCHAR(20)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM ContactInformation) THEN
			RETURN QUERY
				SELECT * FROM ContactInformation;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS print_table_ClientInformation();
CREATE FUNCTION print_table_ClientInformation()
	RETURNS TABLE (id INTEGER, full_name VARCHAR(40), number VARCHAR(20), email VARCHAR(40)) AS
	$$
	BEGIN
		IF EXISTS (SELECT * FROM ClientInformation) THEN
			RETURN QUERY
				SELECT * FROM ClientInformation;
		ELSE
			RAISE NOTICE 'Table is empty';
		END IF;
	END;
	$$
LANGUAGE plpgsql;

