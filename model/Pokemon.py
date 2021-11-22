class Pokemon:

    def __init__(self, props: dict):
        self.id = props['id']
        self.nome = props['name']
        self.url = 'https://pokeapi.co/api/v2/pokemon/' + str(props['id'])
        self.peso = props['weight']
        self.habilidades = props['abilities']
        self.tipo = props['types']

    def __str__(self):
        return f'Número da Pokedex: {self.id} \n' \
               f'Nome: {self.nome} \n' \
               f'URL: {self.url} \n' \
               f'Peso: {self.peso} \n' \
               f'Habilidades: {", ".join(self.habilidades)} \n' \
               f'Tipo: {", ".join(self.tipo)}'
