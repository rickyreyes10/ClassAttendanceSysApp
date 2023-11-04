import mysql.connector
from configparser import ConfigParser


def read_db_config(filename='db_config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db_config


def connect():
    """ Connect to the MySQL database and return a connection object. """
    db_config = read_db_config()

    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
        else:
            raise Exception('Failed to connect to the database.')
    except mysql.connector.Error as e:
        raise Exception(f"Error {e.errno}: {e.msg}")

