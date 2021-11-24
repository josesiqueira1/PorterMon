from typing import List

from PyQt5 import QtWidgets
from requests import get

from db.sqlite import PokemonDb

database = PokemonDb()


class Pokemon:

    def __init__(self, id_pokedex: int, ):
        self.id = id_pokedex
        self.identificacao = ''

        pokemon = self.busca_pokemon_por_id()
        if len(pokemon) == 1:
            self.nome = pokemon[0][1]
            self.url = pokemon[0][2]
            self.peso = pokemon[0][3]
            self.habilidades = self.parse_list(pokemon[0][4])
            self.tipo = self.parse_list(pokemon[0][5])
        else:
            props: dict = self.busca_pokemon_pokeapi(id_pokedex)
            self.nome = props['name']
            self.url = 'https://pokeapi.co/api/v2/pokemon/' + str(props['id'])
            self.peso = props['weight']
            self.habilidades = [x["ability"]["name"] for x in props['abilities']]
            self.tipo = [x["type"]["name"] for x in props['types']]

            self.salvar_no_banco()

    @staticmethod
    def parse_list(lista: str, ):
        return lista.strip('][').split(',')

    @staticmethod
    def busca_pokemon_pokeapi(id_pokedex: int, ):
        resultado = get('https://pokeapi.co/api/v2/pokemon/' + str(id_pokedex))
        if resultado.status_code != 200:
            raise Exception(resultado.text)
        return resultado.json()

    @property
    def habilidades(self, ) -> List[str]:
        return self._habilidades

    @habilidades.setter
    def habilidades(self, lista: List[str], ):
        self._habilidades = lista

    @property
    def tipo(self, ) -> List[str]:
        return self._tipo

    @tipo.setter
    def tipo(self, lista: List[str], ):
        self._tipo = lista

    @property
    def id(self, ) -> int:
        return self._id

    @id.setter
    def id(self, pokedex_id: int, ):
        self._id = pokedex_id

    @property
    def nome(self, ) -> str:
        return self._nome

    @nome.setter
    def nome(self, nome: str, ):
        self.identificacao = str(self.id) + ' - ' + nome
        self._nome = nome

    @property
    def peso(self, ) -> int:
        return self._peso

    @peso.setter
    def peso(self, peso: int, ):
        self._peso = peso

    @property
    def identificacao(self, ) -> str:
        return self._identificacao

    @identificacao.setter
    def identificacao(self, identificacao: str, ):
        self._identificacao = identificacao

    def salvar_no_banco(self, ):
        database.insert(['id', 'nome', 'url', 'peso', 'habilidades', 'tipo'],
                        f"{self.id}, '{self.nome}', '{self.url}', {self.peso}, '[{','.join(self.habilidades)}]', "
                        f"'[{','.join(self.tipo)}]'")

    def busca_pokemon_por_id(self, ):
        return database.busca_por_id(str(self.id))

    def __str__(self, ):
        return f'Número da Pokedex: {self.id} \n' \
               f'Nome: {self.nome} \n' \
               f'URL: {self.url} \n' \
               f'Peso: {self.peso} \n' \
               f'Habilidades: {", ".join(self.habilidades)} \n' \
               f'Tipo: {", ".join(self.tipo)}'

    def inserir_na_lista(self, combo_box: QtWidgets.QComboBox, ):
        if combo_box.findText(self.identificacao) > 0:
            return
        combo_box.insertItem(self.id, self.identificacao, userData=self)
