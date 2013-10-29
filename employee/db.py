"""
A module containing methods that provide useful abstractions for dealing
with the database and the ORM.
"""
import copy
import json
import time
import os
import sys
import cx_Oracle
#import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool, QueuePool, StaticPool

import logging
log = logging.getLogger()
connections_dictionary = {'default': {'host': '10.55.86.214',
                                      'Dialect': 'oracle',
                                      'Driver': 'cx_oracle',
                                      'port':'1521',
                                      'User': 'oracle',
                                      'Password': 'system',
                                      'Name': 'xe'}}
CONNECTION_KEY = 'default'

# TODO
# Add Exception Handling - throw exception for now

# Put the SQLAlchemy engines at a module level so there is only one instance
ENGINES = {}


class ConnectionWrapper:
    """
     A wrapper class for Connection objects.
    """

    def __init__(self, connection=None, metadata=None):
        self.connection = connection
        self.metadata = metadata


def _init_engine(connection_key, connection_dictionary):
    """
     Create an Engine and add it to the module-level ENGINES dictionary, along
     with a sessionmaker instance for that engine.
    """
    global ENGINES
    ENGINES[connection_key] = {}

    connection_string = '%s+%s://%s:%s@%s' % (
        # The actual import is cx_Oracle,
        # but SQLAlchemy wants cx_oracle, so we lowercase it
        # answer: the string is an RFC-1738 style URL so the "protocol"
        #         portion (i.e. left of the first":") must be lower-case
        connection_dictionary['Dialect'],
        connection_dictionary['Driver'].lower(),
        connection_dictionary['User'],
        connection_dictionary['Password'],
        connection_dictionary['Name'])

    ENGINES[connection_key]['engine'] = create_engine(
        '%s+%s://%s:%s@%s/%s' % (
            connection_dictionary['Dialect'],
            # The actual import is cx_Oracle,
            # but SQLAlchemy wants cx_oracle, so we lowercase it
            # answer: the string is an RFC-1738 style URL so the "protocol"
            #         portion (i.e. left of the first":") must be lower-case
            connection_dictionary['Driver'].lower(),
            connection_dictionary['User'],
            connection_dictionary['Password'],
            connection_dictionary['host'],
            connection_dictionary['Name']),
        coerce_to_decimal=False,
        convert_unicode=True,
        pool_recycle=300,
        pool_timeout=30)
        # poolclass=QueuePool,
        # pool_size=50,
        # pool_reset_on_return='rollback',
        # max_overflow=10)
    Session = scoped_session(sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINES[connection_key]['engine']))
    #    Session.configure(bind=ENGINES[connection_key]['engine'])

    ENGINES[connection_key]['sessionmaker'] = Session


def _initialize(connections_filename=None,
                plaintext=False, **kwargs):
    global connections_dictionary

    #
    # use the default connections file if one is not provided.
    # reset plaintext if the the default file is used.
    #
    plaintext = True

def ensure_init(original_function, **kwargs):
    """
     A decorator method to make sure we run init first if the module hasn't
     been initialized.
    """

    def new_function(*args, **kwargs):
        if not connections_dictionary:
            _initialize(**kwargs)
        return original_function(*args)

    return new_function


CONNECT_RETRIES = 5
CONNECT_RETRY_WAIT_INTERVAL = 0


@ensure_init
def get_orm_session(connection_key):
    """
     Create and return a scoped_session for a given connection_key.
     Example usage:

     session = db_wrapper.get_orm_session('Deal'):
     session.query(...)

    """
    if ENGINES.get(connection_key) is None:
        connection_dictionary = connections_dictionary[connection_key]
        _init_engine(connection_key, connection_dictionary)

    # Attempt to get the session from the cached sessionmaker class (Session).
    # In case of a database error, clean up the session and then retry
    # CONNECT_RETRIES number of times (waiting CONNECT_RETRY_WAIT_INTERVAL
    # seconds).
    for i in xrange(CONNECT_RETRIES):
        try:
            session = ENGINES[connection_key]['sessionmaker']()
            ping_connection(session)
        except Exception as e:
            session.bind.pool.dispose()
            time.sleep(CONNECT_RETRY_WAIT_INTERVAL)
            continue
        else:
            return session
        break

    ex_type, ex_value, ex_traceback = sys.exc_info()
    raise ex_type, ex_value, ex_traceback


def ping_connection(session):
    """
    Attempt to use a session's connection; if it fails,
    clean up after ourself and reraise.
    """
    try:
        session.execute('SELECT 1 FROM DUAL')
    except:
        session.rollback()
        raise


@ensure_init
def get_db_connection_wrapper(connection_key, orm=False):
    """
     Get a database connection object based off the given connection key.
    """
    connection_dictionary = copy.deepcopy(
        connections_dictionary[connection_key])
    connection = None
    if orm:
        connection = _get_orm_connection(
            connection_key,
            connection_dictionary)
        connection_dictionary['ORM'] = 'SQLAlchemy'
    else:
        if 'oracle' == connection_dictionary['Dialect']:
            connection = _get_oracle_connection(connection_dictionary)
        elif 'mongodb' == connection_dictionary['Dialect']:
            connection = _get_mongo_connection(connection_dictionary)

    # Delete the password before handing back to the caller
    del connection_dictionary['Password']
    connection_wrapper = ConnectionWrapper(
        connection,
        metadata=connection_dictionary)

    return connection_wrapper


@ensure_init
def get_orm_session_obj(connection_key):
    """
     Create and return a scoped_session object for a given connection_key.
     Example usage:

     session = db_wrapper.get_orm_session_obj('default'):
     session.query(...)


    """
    if ENGINES.get(connection_key) is None:
        connection_dictionary = connections_dictionary[connection_key]
        _init_engine(connection_key, connection_dictionary)

    # Attempt to get the session object from the cached sessionmaker class
    # (Session). In case of a database error, clean up the session and then
    # retry CONNECT_RETRIES number of times (waiting
    # CONNECT_RETRY_WAIT_INTERVAL seconds).
    for i in xrange(CONNECT_RETRIES):
        try:
            session = ENGINES[connection_key]['sessionmaker']
            ping_connection(session)
        except Exception as e:
            log.error(
                "Connection error; retrying: %s" % (str(e),),
                extra=settings.LOGGING_EXTRA_DATA)
            session.bind.pool.dispose()
            time.sleep(CONNECT_RETRY_WAIT_INTERVAL)
            continue
        else:
            return session
        break

    ex_type, ex_value, ex_traceback = sys.exc_info()
    log.error(
        "Connection failed: %s %s" % (ex_type, ex_value),
        extra=settings.LOGGING_EXTRA_DATA)
    raise ex_type, ex_value, ex_traceback


@ensure_init
def get_orm_engine(connection_key):
    """
     Return the engine object for a particular connection key
    """
    if ENGINES.get(connection_key) is None:
        connection_dictionary = connections_dictionary[connection_key]
        _init_engine(connection_key, connection_dictionary)
    return ENGINES[connection_key]['engine']


def _get_oracle_connection(connection_dictionary):
    """
     Establish a connection to Oracle and return the connection object.
    """
    connection = cx_Oracle.connect('%s/%s@%s' % (
        connection_dictionary['User'],
        connection_dictionary['Password'],
        connection_dictionary['Name']))
    return connection


def _get_mongo_connection(connection_dictionary):
    """
     Establish a connection to MongoDB and return the connection object.
    """
    #    connection = pymongo.connection.Connection(
    #            host=connection_dictionary['Host'],
    #            port=connection_dictionary['Port'])
    #    return connection
    pass


def _get_sqlserver_connection(connection_dictionary):
    """
     Establish a connection to SQL Server and return the connection object.
    """
    pass


def _get_orm_connection(connection_key, connection_dictionary):
    """
     Establish a connection to a database through the ORM and return the
     connection object.
    """
    if ENGINES.get(connection_key) is None:
        _init_engine(connection_key, connection_dictionary)
    connection = ENGINES[connection_key]['engine'].connect()
    return connection

def gensequence(connection_key=CONNECTION_KEY):
    conn = ENGINES.get(connection_key)
    if not conn:
        #need to initialize the db connection for gensequence to work
        get_orm_session(connection_key)
        conn = ENGINES[connection_key]
    #return conn['gensequence'].next()
    return (get_orm_session(connection_key)
            .execute("select Core.UDF_GETSEQUENCENUMBER(1, to_number(sys_guid(),'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')) from dual")
            .scalar())
