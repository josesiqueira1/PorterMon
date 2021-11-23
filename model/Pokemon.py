from typing import List

from db.sqlite import PokemonDb

database = PokemonDb()


class Pokemon:

    def __init__(self, props: dict, ):
        self.id = props['id']

        pokemon = self.busca_pokemon_por_id()
        if len(pokemon) == 1:
            self.nome = pokemon[0][1]
            self.url = pokemon[0][2]
            self.peso = pokemon[0][3]
            self.habilidades = self.parse_list(pokemon[0][4])
            self.tipo = self.parse_list(pokemon[0][5])
            self.sprite = pokemon[0][6]
        else:
            self.nome = props['name']
            self.url = 'https://pokeapi.co/api/v2/pokemon/' + str(props['id'])
            self.peso = props['weight']
            self.habilidades = [x["ability"]["name"] for x in props['abilities']]
            self.tipo = [x["type"]["name"] for x in props['types']]
            self.sprite = props['sprites']['front_default']

            self.salvar_no_banco()

    @staticmethod
    def parse_list(lista: str, ):
        return lista.strip('][').split(',')

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
        self._nome = nome

    @property
    def peso(self, ) -> int:
        return self._peso

    @peso.setter
    def peso(self, peso: int, ):
        self._peso = peso

    def salvar_no_banco(self, ):
        database.insert(['id', 'nome', 'url', 'peso', 'habilidades', 'tipo', 'sprite'],
                        f"{self.id}, '{self.nome}', '{self.url}', {self.peso}, '[{','.join(self.habilidades)}]', "
                        f"'[{','.join(self.tipo)}]', '{self.sprite}'")

    def busca_pokemon_por_id(self, ):
        return database.busca_por_id(str(self.id))

    def __str__(self, ):
        return f'Número da Pokedex: {self.id} \n' \
               f'Nome: {self.nome} \n' \
               f'URL: {self.url} \n' \
               f'Peso: {self.peso} \n' \
               f'Habilidades: {", ".join(self.habilidades)} \n' \
               f'Tipo: {", ".join(self.tipo)}'
