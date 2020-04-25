import sqlite3
import os
import logger.logger as logger
import config.resources as resources
from main import __working__directory__

# Logger instance
logger_instance = logger.logger()
logger_instance.create_logger()

# resources instance
resources_instance = resources.resources()
__resources__path__ = resources_instance.resources_path()

# Db path
__database__path__ = os.path.join(__resources__path__, 'realdefdb.db')


def get_connection():
    '''This function will create database file if not exists'''
    logger_instance.write_log(40, 1)  # DB init
    if(os.path.isfile(__database__path__)):
        logger_instance.write_log(41, 1)  # DB file exists
        try:
            logger_instance.write_log(45, 1)  # DB connect
            conn = sqlite3.connect(__database__path__, check_same_thread=False)
            logger_instance.write_log(46, 1)
        except Exception as e:
            logger_instance.write_log(146, 0, e)
        logger_instance.write_log(42, 1)  # Launch test methods
        if (testDb(conn)):  # Testing and repairing
            logger_instance.write_log(47, 1)  # DB test
            logger_instance.write_log(69, 1)  # DB repair
        else:
            logger_instance.write_log(147, 0, '')
            logger_instance.write_log(169, 0, '')
    else:
        logger_instance.write_log(141, 0, '')
        logger_instance.write_log(44, 1)  # Creating DB file
        try:
            conn = sqlite3.connect(__database__path__)
        except Exception as e:
            logger_instance.write_log(141, 0, e)
        logger_instance.write_log(48, 1)
        initsqlite(conn)
        # Didnt create
    return conn


def initsqlite(conn):
    '''Following function will initialize DB infrastructure'''  # TODO swith to each query from different place
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE urls (date, url, user, time, type, protocol)''')
        c.execute('''CREATE TABLE whitelist (url, ip)''')
        c.execute('''CREATE TABLE blacklist (url, ip)''')
        conn.commit()
    except Exception as e:
        logger_instance.write_log(140, 0, e)  # Initialization failed
    return


def repair_db(c):
    '''Following function reparis DB, checks if tables exists'''
    logger_instance.write_log(60, 1)
    flag = True
    try:
        c.execute('''SELECT * FROM sqlite_master where name = 'urls' ''')
        query_response = c.fetchone()
        print(query_response)
        if(query_response == None):
            logger_instance.write_log(61, 1)
            c.execute(
                '''CREATE TABLE urls (date, url, user, time, type, protocol)''')
    except Exception as e:
        logger_instance.write_log(169, 0, 'urls {}'.format(e))
        flag = False

    try:
        c.execute('''SELECT * FROM sqlite_master where name = 'whitelist' ''')
        query_response = c.fetchone()
        if(query_response == None):
            logger_instance.write_log(62, 1)
            c.execute('''CREATE TABLE whitelist (url, ip)''')
    except Exception as e:
        logger_instance.write_log(169, 0, 'whitelist {} '.format(e))
        flag = False

    try:
        c.execute('''SELECT * FROM sqlite_master where name = 'blacklist' ''')
        query_response = c.fetchone()
        if(query_response == None):
            logger_instance.write_log(63, 1)
            c.execute('''CREATE TABLE blacklist (url, ip)''')
    except Exception as e:
        logger_instance.write_log(169, 0, 'blacklist {}'.format(e))
        flag = False

    return False if flag == False else True


def testDb(conn):
    c = conn.cursor()
    c.execute('''SELECT count(*) FROM sqlite_master where name in ("urls", "whitelist", "blacklist")''')
    flag = True
    if (c.fetchone()[-1] < 3):
        if(not repair_db(c)):
            flag = False
    conn.commit()
    return False if flag == False else True  # Amount of db queries.


def insert_list_type(conn, url, ip, list_type):
    print(url, list_type)
    c = conn.cursor()
    try:
        c.execute("insert into {} values (?, ?)".format(list_type), (url, ip))
        conn.commit()
    except Exception as e:
        logger_instance.write_log(
            149, 0, "DB table: {} {}".format(list_type, e))


def inserturl(conn, date=0, url=0, user=0, time=0, typerequest=1, protocol=2):
    c = conn.cursor()
    try:
        c.execute("insert into urls values (?, ?, ?, ?, ?, ?)",
                  (date, url, user, time, typerequest, protocol))
        conn.commit()
    except Exception as e:
        logger_instance.write_log(149, 0, e)


def isurlindb(conn, urltocheck):
    try:
        print(urltocheck)
        c = conn.cursor()
        urltocheck = urltocheck.split('/')[2]
        c.execute(
            "SELECT count(url) FROM whitelist WHERE url LIKE '%{}%'".format(urltocheck))
        if((c.fetchone()[0]) != 0):
            #already in db
            print("sqlite says url exists")
            conn.commit()
            return 'WL'
        else:
            c.execute(
                "SELECT count(url) FROM blacklist WHERE url LIKE '%{}%'".format(urltocheck))
            if((c.fetchone()[0]) != 0):
                #aalready in db
                print("sqlite says url exists")
                conn.commit()
                return 'BL'
            else:
                return 'CHECK'

    except Exception as e:
        print(e)
        return False


