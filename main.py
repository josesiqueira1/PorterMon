from requests import get
from model.Pokemon import Pokemon


class PorterMon:

    @staticmethod
    def busca_pokemon_pokeapi(id_pokedex: int, ) -> Pokemon:
        resultado = get('https://pokeapi.co/api/v2/pokemon/' + str(id_pokedex))
        if resultado.status_code != 200:
            raise Exception(resultado.text)
        return Pokemon(resultado.json())

    def run(self, ):
        lista_de_pokemons = [self.busca_pokemon_pokeapi(i) for i in range(1, 21)]
        print(lista_de_pokemons)


if __name__ == '__main__':
    _portermon = PorterMon()
    _portermon.run()
