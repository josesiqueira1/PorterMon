from PyQt5 import QtWidgets, QtGui

from db.sqlite import PokemonDb
from helper.DialogPadrao import DialogPadrao, DialogPorID

database = PokemonDb()


class DialogLimparTodoCache(DialogPadrao):
    def __init__(self, icon: QtGui.QIcon, combo_box_pokemons: QtWidgets.QComboBox):
        self.combo_box_pokemons = combo_box_pokemons
        super().__init__(icon, 'Tem certeza que deseja limpar todo o cache?')

    def accepted_function(self, ):
        database.truncate()
        self.combo_box_pokemons.clear()
        self.combo_box_pokemons.addItem('')
        self.close()

    @staticmethod
    def montar_itens_adicionais(layout):
        pass


class DialogLimparCachePorID(DialogPorID):
    def __init__(self, icon: QtGui.QIcon, combo_box_pokemons: QtWidgets.QComboBox):
        super().__init__(icon, combo_box_pokemons, 'Selecione abaixo o ID do pokemon para limpar do cache')

    def accepted_function(self, ):
        database.delete(str(self.id_pokedex))
        self.combo_box_pokemons.removeItem(self.id_pokedex)
        self.close()
