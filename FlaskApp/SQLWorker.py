from sqlalchemy import create_engine, MetaData, Table
import pandas as pd
import datetime
from sqlalchemy.dialects.mysql.dml import Insert


class SQLWorker:
    def __init__(self, db_string):
        self.db_string = db_string
        self.engine = create_engine(self.db_string)

    def get_columns(self, table_name):
        meta = MetaData(bind=self.engine)
        meta.reflect(only=[table_name])
        table_sql = Table(table_name, meta)
        columns = [c.name for c in table_sql.columns]
        return columns

    def insert_duplicate_df(self, df, table_name):
        self.meta = MetaData(bind=self.engine)
        self.meta.reflect()
        table_sql = self.meta.tables[table_name]
        data = df.to_dict(orient="records")
        stmt = Insert(table_sql).values(data)
        columns = [c.name for c in table_sql.columns if c.name in list(df.columns)]
        update_dic = {}
        for c in columns:
            update_dic[c] = stmt.inserted[c]
        if 'created' in [c.name for c in table_sql.columns]:
            update_dic['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stmt = stmt.on_duplicate_key_update(**update_dic)
        #print(stmt)
        self.engine.execute(stmt)

    def exec_query_as_df(self, query):
        df = pd.read_sql_query(query, self.engine)
        return df
