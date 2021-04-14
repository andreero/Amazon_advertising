
class DBConfig():
    @classmethod
    def from_dict(cls, config_dict):
        kwargs = {key: value for key, value in config_dict.items()}
        return cls(**kwargs)

    def __init__(
            self,
            user,
            password,
            server,
            database,
            use_trusted_connection,
            driver='ODBC Driver 17 for SQL Server'):
        self.user = user
        self.password = password
        self.server = server
        self.database = database
        self.use_trusted_connection = True if str(use_trusted_connection).lower() == 'true' else False
        self.driver = driver

    @property
    def connection_string(self):
        if self.use_trusted_connection:
            connection_string = 'mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}'.format(
                server=self.server,
                database=self.database,
                driver=self.driver)
        else:
            connection_string = 'mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}'.format(
                user=self.user,
                password=self.password,
                server=self.server,
                database=self.database,
                driver=self.driver)
        return connection_string
