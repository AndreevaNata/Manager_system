CREATE EXTENSION IF NOT EXISTS dblink;

DROP FUNCTION IF EXISTS create_db(text, text);
CREATE FUNCTION create_db(dbname text, username text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			RAISE NOTICE 'Database "%%" already exists', dbname;
			RETURN 0;
		ELSE
   			PERFORM dblink_exec('user=natasha password=nata dbname=' || current_database(),
								'CREATE DATABASE ' || dbname);

			PERFORM dblink_exec('user=natasha password=nata dbname=' || dbname,
			    '
                DROP TABLE IF EXISTS ContactInformation CASCADE;
                CREATE TABLE ContactInformation(
                    id serial PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL
                 );
                ALTER SEQUENCE ContactInformation_id_seq RESTART WITH 1;

                DROP TABLE IF EXISTS ClientInformation CASCADE;
                CREATE TABLE ClientInformation(
                    id serial PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    email VARCHAR(40) NOT NULL
                );
                ALTER SEQUENCE ClientInformation_id_seq RESTART WITH 1;

                DROP TABLE IF EXISTS Clothes CASCADE;
                CREATE TABLE Clothes(
                    id serial PRIMARY KEY,
                    name VARCHAR(40) NOT NULL,
                    size_clothes VARCHAR(5) NOT NULL,
                    color VARCHAR(20) NOT NULL,
                    price INTEGER NOT NULL
                );
                ALTER SEQUENCE Clothes_id_seq RESTART WITH 1;

                DROP TABLE IF EXISTS Worker CASCADE;
                CREATE TABLE Worker(
                    id serial PRIMARY KEY,
                    post VARCHAR(40) NOT NULL,
                    salary INTEGER NOT NULL,
                    contact integer REFERENCES ContactInformation( id ) NOT NULL
                );
                ALTER SEQUENCE Worker_id_seq RESTART WITH 1;

                DROP TABLE IF EXISTS Buying CASCADE;
                CREATE TABLE Buying(
                    id serial PRIMARY KEY,
                    product VARCHAR(40) NOT NULL,
                    size_ VARCHAR(5) NOT NULL,
                    price INTEGER NOT NULL,
                    discount INTEGER NOT NULL,
                    date_buy VARCHAR(40),
                    where_buy VARCHAR(40) NOT NULL
                );
                ALTER SEQUENCE Buying_id_seq RESTART WITH 1;

                DROP TABLE IF EXISTS Clients CASCADE;
                CREATE TABLE Clients(
                    id serial PRIMARY KEY,
                    full_name VARCHAR(40),
                    clothes_c integer REFERENCES Buying( id ),
                    consultant integer REFERENCES Worker( id ),
                    telephone integer REFERENCES ClientInformation(id)
                );
                ALTER SEQUENCE Clients_id_seq RESTART WITH 1;
                CREATE INDEX product ON Buying (product);
                 '
			);

			PERFORM dblink_exec('user=natasha password=nata dbname=' || dbname,
			'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ' || username );
			RETURN 1;
		END IF;

	END
	$func$
	LANGUAGE plpgsql;


DROP FUNCTION IF EXISTS drop_db(text);
CREATE FUNCTION drop_db(dbname text)
	RETURNS INTEGER AS
	$func$
	BEGIN
		IF EXISTS (SELECT datname FROM pg_database WHERE datname = dbname) THEN
   			PERFORM dblink_exec('user=natasha password=nata dbname=' || current_database(),
								'DROP DATABASE ' || quote_ident(dbname));
			RETURN 1;
		ELSE
			RAISE NOTICE 'Database "%%" does not exist', dbname;
			RETURN 0;
		END IF;

	END
	$func$
	LANGUAGE plpgsql;