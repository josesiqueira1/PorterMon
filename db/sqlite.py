import sqlite3
from os import path
from typing import List


class PokemonDb:

    @staticmethod
    def nova_conexao():
        base_dir = path.dirname(path.abspath(__file__))
        db_path = path.join(base_dir, "pokemons.sqlite")
        return sqlite3.connect(db_path)

    def insert(self, campos: List[str], values: str, ):
        try:
            conn = self.nova_conexao()

            insert_sql = f"""insert into pokemons({', '.join(campos)}) """ \
                         f"""values ({values})"""
            conn.execute(insert_sql)

            conn.commit()
        except Exception as e:
            raise e

    def select(self, sql: str):
        try:
            conn = self.nova_conexao()

            result = conn.execute(sql)

            conn.commit()

            return result.fetchall()
        except Exception as e:
            raise e

    def busca_por_id(self, id_query: str):
        return self.select(f'select * from pokemons where id = {id_query}')
