import models
import os


def db_connect(username, password):

    if not os.path.exists('/tmp/.tmp_fuse_db/'):
        print('tmp_fuse_db not exist')
        os.makedirs('/tmp/.tmp_fuse_db/')
        os.makedirs('/tmp/.tmp_fuse_db/' + username + '/')

    print('db connect')
    dbms = models.FuseDatabase(models.SQLITE, dbname='/tmp/.tmp_fuse_db/' + username + '/fuse.db', username=username, password=password)
    print (dbms.db_engine)
    """
    # Create Tables
    print('create tables')
    dbms.create_db_tables()
    dbms.insert_key('this is a key', '/fuse/fuse/path')
    dbms.insert_token('this is a token')
    dbms.print_all_data(models.TOKENS)
    dbms.print_all_data(models.KEYS)
    """

    return dbms
