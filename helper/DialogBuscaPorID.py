from PyQt5 import QtWidgets, QtGui

from db.sqlite import PokemonDb
from helper.DialogPadrao import DialogPorID
from model.Pokemon import Pokemon

database = PokemonDb()


class DialogBuscaPorID(DialogPorID):
    def __init__(self, icon: QtGui.QIcon, combo_box_pokemons: QtWidgets.QComboBox):
        super().__init__(icon, combo_box_pokemons, 'Selecione abaixo o ID do pokemon para realizar a busca')

    def accepted_function(self, ):
        pokemon = Pokemon(self.id_pokedex)
        pokemon.inserir_na_lista(self.combo_box_pokemons)
        self.close()
