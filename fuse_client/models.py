from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData

#engine = create_engine('sqlite:///tmp/.tmp_fuse_db/fuse.db', echo=True)
#Base = declarative_base()

# Global Variables
SQLITE = 'sqlite'
# Table Names
TOKENS = 'tokens'
KEYS = 'keys'
PKEY = 'pkey'

class FuseDatabase:
    DB_ENGINE = {
        #SQLITE: 'sqlite+pysqlcipher://:{password}@{DB}',
        SQLITE: 'sqlite:///{DB}',
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            print(str(dbtype))
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)#, password=password)

            print(engine_url)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)

        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        tokens = Table(TOKENS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('token', String),
                      )

        keys = Table(KEYS, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('key', String),
                        Column('path', String)
                        )

        pkey = Table(PKEY, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('private', String),
                        Column('public', String)
                        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '' : return

        print (query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        print(query)

        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row) # print(row[0], row[1], row[2])
                result.close()

        print("\n")

    # Examples

    def get_all_tokens(self):
        # Sample Query
        query = "SELECT token FROM {TBL_TOKENS};".format(TBL_TOKENS=TOKENS)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for r in result:
                    token = r[0]
                result.close()
                return token

    def get_all_keys(self):
        # Sample Query
        query = "SELECT key, path FROM {TBL_KEYS};".format(TBL_KEYS=KEYS)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                keys = []
                paths = []
                for r in result:
                    keys.append(r[0])
                    paths.append(r[1])

                result.close()
                return keys, paths

    def get_key_from_path(self, path):
        # Sample Query
        query = "SELECT key FROM {TBL_KEYS} WHERE path={paths};".format(TBL_KEYS=KEYS, paths=path)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                keys = []
                for r in result:
                    keys.append(r[0])

                result.close()
                return keys

    def get_all_pkeys(self):
        # Sample Query
        query = "SELECT public FROM {TBL_KEYS};".format(TBL_KEYS=KEYS)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                keys = []
                for r in result:
                    keys.append(r[0])

                result.close()
                return keys

    def delete_key_by_path(self, path):
        # Delete Data by Id
        query = "DELETE FROM {} WHERE path={}".format(KEYS, path)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                return result

        # Delete All Data
        '''
        query = "DELETE FROM {}".format(TOKENS)
        self.execute_query(query)
        self.print_all_data(USERS)
        '''

    def insert_token(self, token):
        # Insert Data
        query = "INSERT INTO {}(token) " \
                "VALUES ('{}');".format(TOKENS, token)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                return result

    def insert_key(self, k, path):
        # Insert Data
        query = "INSERT INTO {}(key, path) " \
                "VALUES ('{}', '{}');".format(KEYS, k, path)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                return result

    def insert_pkey(self, public, private):
        # Insert Data
        query = "INSERT INTO {}(public, private) " \
                "VALUES ('{}', '{}');".format(PKEY, public, private)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                return result

    def db_drop_all(self):
        self.execute_query('DROP TABLE TOKENS;')
        self.execute_query('DROP TABLE KEYS;')
        self.execute_query('DROP TABLE PKEY;')

    def db_drop_tokens(self):
        self.execute_query('DROP TABLE TOKENS;')

    def db_drop_keys(self):
        self.execute_query('DROP TABLE KEYS;')

    def db_drop_pkeys(self):
        self.execute_query('DROP TABLE PKEY;')