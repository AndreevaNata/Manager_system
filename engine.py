import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import datetime
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database as util_drop_db

auth = {
    'user': 'postgres',
    'password': 'Nata124',
}
engine = create_engine("postgresql://{}:{}@localhost:5432/chatoyer".format(auth['user'], auth['password']))


# выделенный пользователь - viktor, пароль - viktor, он подключается к существующей базе данных
# база данных создается суперпользователем db_creator

fin = open('create_drop_func.sql')
cr_dr_func = fin.read()
fin.close()

fin = open('functions.sql')
func = fin.read()
fin.close()

engineURL = ''


def connect_as_creator(username_creator, password_creator, main_db, cr_dr_func):
    engine = create_engine(
        "postgresql+psycopg2://{}:{}@localhost/{}".format(username_creator, password_creator, main_db),
        echo=True)
    cursor = engine.connect()  # подключаемся
    cursor.execute(cr_dr_func)  # запускаем функции
    return cursor, engine


def create_database(db_name, username, cr_dr_func=cr_dr_func):  # название базы данных и имя пользователя, который будет ей пользоваться
    cursor, _ = connect_as_creator('kris', 'kris', 'chatoyer', cr_dr_func)
    cursor.execute('SELECT create_db(\'{}\', \'{}\')'.format(db_name, username))  # запускаем создание базы данных
    cursor.close()


# если в pgadmin подключаешься к базе, то от нее обязательно надо отключаться, чтобы дропалось
def drop_database(db_name, cr_dr_func=cr_dr_func):
    cursor, en = connect_as_creator('kris', 'kris', 'chatoyer', cr_dr_func)
    url =  "postgresql+psycopg2://{}:{}@localhost/{}".format('kris', 'kris', db_name)
    # cursor.execute('SELECT drop_db(\'{}\')'.format(db_name))  # запускаем удаление
    util_drop_db(url)


def connect_as_user(username, password, db_name, functions=func):
    connection = psycopg2.connect(host='localhost', database=db_name, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(functions)
    connection.commit()
    return connection


def disconnect_user(connection):
    connection.close()


def clear_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_all_tables()')
    connection.commit()


def clear_clients(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_clients()')
    connection.commit()


def clear_worker(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_worker()')
    connection.commit()


def clear_buying(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_buying()')
    connection.commit()


def clear_contact_information(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_contact_inf()')
    connection.commit()

def clear_contact_information_c(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_contact_inf()')
    connection.commit()


def clear_clothes(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT clear_clothes()')
    connection.commit()



def add_to_contact_information(connection, in_id, in_name, in_phone_number):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_contact_information({}, \'{}\', \'{}\')'.format(in_id, in_name, in_phone_number))
    connection.commit()

def add_to_contact_informationC(connection, in_id, in_phone_number, in_email):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_contact_information({}, \'{}\', \'{}\')'.format(in_id, in_phone_number, in_email))
    connection.commit()


def add_to_worker(connection, in_post, in_salary, in_phone_number, in_name):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_worker(\'{}\', {}, \'{}\', \'{}\')'.format(in_post, in_salary, in_phone_number, in_name))
    connection.commit()


def add_to_clients(connection, in_full_name, in_phone_number, in_email):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT add_to_clients(\'{}\'::varchar(40), \'{}\'::varchar(20), \'{}\'::varchar(40))'.format(in_full_name, in_phone_number, in_email))
    connection.commit()

def add_to_buying(connection, in_full_name, in_product , in_size_, in_price, in_discount, in_date_buy, in_where_buy):
    cursor = connection.cursor()
    cursor.execute('SELECT add_to_buying(\'{}\', \'{}\', \'{}\', {}, {}, \'{}\', \'{}\')'.format(in_full_name, in_product , in_size_, in_price, in_discount, in_date_buy, in_where_buy))
    connection.commit()

def update_buying(connection, in_id, in_product , in_size_, in_price, in_discount, in_date_buy, in_where_buy):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT update_buying({}, \'{}\', \'{}\', {}, {}, \'{}\', \'{}\')'.format(in_id, in_product , in_size_, in_price, in_discount, in_date_buy, in_where_buy))
    connection.commit()
#
# def update_worker(connection, in_id, in_post, in_salary, in_contact_information):
#     cursor = connection.cursor()
#     cursor.execute(
#         'SELECT update_worker({}, \'{}\', \'{}\', {})'.format(in_id, in_post, in_salary, in_contact_information))
#     connection.commit()

# def update_contact_inf(connection, in_id, in_post, in_salary, in_contact_information):
#     cursor = connection.cursor()
#     cursor.execute(
#         'SELECT update_contact_inf({}, \'{}\', \'{}\', {})'.format(in_id, in_post, in_salary, in_contact_information))
#     connection.commit()


def delete_worker_by_id(connection, in_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_worker_by_id({})'.format(in_id))
    connection.commit()

def delete_client_by_id(connection, in_id):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_client_by_id({})'.format(in_id))
    connection.commit()



def delete_contact_information_by_name(connection, in_name):
    cursor = connection.cursor()
    cursor.execute('SELECT delete_contact_information_by_id({})'.format(in_name))
    connection.commit()

def search_contact_by_name(connection, name):
    cursor = connection.cursor()
    cursor.execute('SELECT search_contact_by_name(\'{}\')'.format(name))
    table = cursor.fetchall()
    return table

def search_client_by_name(connection, full_name):
    cursor = connection.cursor()
    cursor.execute('SELECT search_client_by_name(\'{}\')'.format(full_name))
    table = cursor.fetchall()
    return table
# def delete_buying_by_id(connection, in_id):
#     cursor = connection.cursor()
#     cursor.execute('SELECT delete_buying_by_id({})'.format(in_id))
#     connection.commit()


def print_table_worker(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_worker()')
    table = cursor.fetchall()
    return table


def print_table_clients(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_clients()')
    table = cursor.fetchall()
    return table


def print_table_ContactInformation(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_ContactInformation()')
    table = cursor.fetchall()
    return table

def print_table_ClientInformation(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_ClientInformation()')
    table = cursor.fetchall()
    return table


def print_table_buying(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT print_table_buying()')
    table = cursor.fetchall()
    return table