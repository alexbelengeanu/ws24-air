from pymilvus import MilvusClient
import os

class DatabaseManager:
    def __init__(self, db_name='local.db'):
        self.db_name = db_name
        self.__client = None

    def create_client(self, remove_if_exists=False):
        """Creates and returns a Milvus client. Optionally removes the existing database files."""
        if remove_if_exists:
            self._remove_db_files()
        self.__client = MilvusClient(self.db_name)

    def _remove_db_files(self):
        """Helper method to remove database files if they exist."""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
        if os.path.exists(f".{self.db_name}.lock"):
            os.remove(f".{self.db_name}.lock")

    def get_client(self):
        """Returns the current Milvus client, if available, otherwise creates a new one."""
        return self.__client

    def stop_client(self):
        """Stops the Milvus client, if it is running."""
        if self.__client is not None:
            # Assuming there is a method to stop the client correctly
            self.__client.close()
            self.__client = None