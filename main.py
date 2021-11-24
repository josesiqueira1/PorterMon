import sys
from functools import partial
from os import path
from threading import Lock

from PyQt5 import QtWidgets, QtGui, QtCore

from model.Pokemon import Pokemon

PROPRIEDADE_VISIVEIS = ['Nome', 'URL', 'Peso', 'Habilidades', 'Tipo']


class Tasks(QtCore.QObject):
    sinalstatusbar = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Tasks, self).__init__()

    def addstatus(self, texto):
        self.sinalstatusbar.emit(texto)


class PorterMon(QtWidgets.QApplication):

    def __init__(self, argv):
        super(PorterMon, self).__init__(argv)
        self.main_window = self.set_layout()

        tasks = Tasks()
        tasks.sinalstatusbar.connect(self.attstatusbar)
        self.tasks = tasks

        self.redrawLock = Lock()
        self.main_window.resize(400, 300)

    def set_layout(self, ):
        main_window = QtWidgets.QMainWindow()
        main_window.raise_()
        main_window.show()

        scriptdir = path.dirname(path.realpath(__file__))
        main_window.setWindowIcon(QtGui.QIcon(scriptdir + path.sep + 'favicon.png'))

        main_window.setWindowTitle("PorterMon")

        statusbar = QtWidgets.QStatusBar()
        statusbar.setObjectName("statusbar")
        main_window.setStatusBar(statusbar)
        statusbar.setFixedHeight(30)

        layout = QtWidgets.QGridLayout()

        self.novo_label(layout, 0, 'Lista de pokemons')

        pokemons = QtWidgets.QComboBox()
        pokemons.addItem('')
        pokemons.currentIndexChanged.connect(partial(self.handle_change_pokemon, pokemons, ))
        layout.addWidget(pokemons, 1, 0)

        self.novo_label(layout, 2, 'Informações')

        form_layout = QtWidgets.QFormLayout()
        layout.addLayout(form_layout, 3, 0)
        self.adicionar_campos_form(form_layout)

        grid_layout_botoes = QtWidgets.QGridLayout()
        layout.addLayout(grid_layout_botoes, 4, 0)

        botao_20 = QtWidgets.QPushButton()
        botao_20.setText('Carregar 20 primeiros pokemons')
        botao_20.clicked.connect(partial(self.carregar_20_pokemons, pokemons))
        grid_layout_botoes.addWidget(botao_20, 0, 0)

        botao = QtWidgets.QPushButton()
        botao.setText('Carregar pokemon com id')
        grid_layout_botoes.addWidget(botao, 0, 1)

        centralwidget = QtWidgets.QWidget()
        centralwidget.setLayout(layout)
        main_window.setCentralWidget(centralwidget)

        return main_window

    @staticmethod
    def novo_label(layout: QtWidgets.QGridLayout, row: int, texto: str):
        lb = QtWidgets.QLabel(texto)
        layout.addWidget(lb, row, 0)

    def adicionar_campos_form(self, form_layout: QtWidgets.QFormLayout):
        for propriedade in PROPRIEDADE_VISIVEIS:
            line = QtWidgets.QLineEdit(' ')
            line.setReadOnly(True)
            setattr(self, 'texto_' + propriedade.lower(), line)
            form_layout.addRow(QtWidgets.QLabel(propriedade), line)

    def handle_change_pokemon(self, cb_pokemon: QtWidgets.QComboBox, ):
        pokemon: Pokemon = cb_pokemon.currentData()
        em_branco = None
        if not pokemon:
            em_branco = ' '
        for prop in PROPRIEDADE_VISIVEIS:
            prop_lower = prop.lower()
            getattr(self, 'texto_' + prop_lower).setText(str(em_branco or getattr(pokemon, prop_lower)))

    def attstatusbar(self, text: str):
        with self.redrawLock:
            self.main_window.statusBar().showMessage(text, 3000)

    def carregar_20_pokemons(self, combo_box: QtWidgets.QComboBox):
        for i in range(1, 21):
            pokemon = Pokemon(i)
            if combo_box.itemData(i):
                continue
            combo_box.insertItem(pokemon.id, str(pokemon.id) + ' - ' + pokemon.nome, userData=pokemon)
        self.attstatusbar('Pokemons carregados')


if __name__ == '__main__':
    app = PorterMon(sys.argv)
    sys.exit(app.exec())
