from src.constants import EnvironmentVariable
from src.logger import logger
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class CassandraConnect:
    """
    This class shall be used to
    -establish connection with cassandra db(cloud)

    written by: Aparna T Parkala
    Version:1.0
    """
    def __init__(self, env_var: EnvironmentVariable):
        
        try:
            print("here1")
            self.env_var=env_var
            
            cloud_config= {
                    'secure_connect_bundle': self.env_var.SECURE_CONNECT_BUNDLE
            }
            auth_provider = PlainTextAuthProvider(self.env_var.CLIENT_ID, self.env_var.CLIENT_SECRET)
            logger.info("Trying to connect to database")
            print("here")
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            session = cluster.connect(self.env_var.KEYSPACE_NAME)
            self.session = session
            logger.info("Database Connection Established.")
        except Exception as e:
            logger.exception(e)
            raise e