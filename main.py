from requests import get
from model.Pokemon import Pokemon


class PorterMon:

    @staticmethod
    def get_pokemon(id_pokedex: int, ) -> Pokemon:
        resultado = get('https://pokeapi.co/api/v2/pokemon/' + str(id_pokedex))
        if resultado.status_code != 200:
            raise Exception(resultado.text)
        return Pokemon(resultado.json())

    def run(self, ):
        lista_de_pokemons = [self.get_pokemon(i) for i in range(20)]
        print(lista_de_pokemons)


if __name__ == '__main__':
    _portermon = PorterMon()
    _portermon.run()
