import sys
from functools import partial
from os import path
from threading import Lock

from PyQt5 import QtWidgets, QtGui, QtCore

from helper.DialogBuscaPorID import DialogBuscaPorID
from helper.DialogsLimparCache import DialogLimparTodoCache, DialogLimparCachePorID
from model.Pokemon import Pokemon

PROPRIEDADE_VISIVEIS = ['Nome', 'URL', 'Peso', 'Habilidades', 'Tipo', ]


class Tasks(QtCore.QObject):
    sinalstatusbar = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Tasks, self).__init__()

    def addstatus(self, texto):
        self.sinalstatusbar.emit(texto)


class PorterMon(QtWidgets.QApplication):

    def __init__(self, argv, ):
        super(PorterMon, self).__init__(argv)
        self.main_window, self.icon, self.pokemons = self.set_layout()

        tasks = Tasks()
        tasks.sinalstatusbar.connect(self.atualizar_barra_de_status)

        self.redrawLock = Lock()
        self.main_window.resize(400, 300)

    def set_layout(self, ):
        main_window = QtWidgets.QMainWindow()
        main_window.raise_()
        main_window.show()

        scriptdir = path.dirname(path.realpath(__file__))
        icon = QtGui.QIcon(scriptdir + path.sep + 'favicon.png')

        main_window.setWindowIcon(icon)

        main_window.setWindowTitle("PorterMon")

        self.monta_barra_de_status(main_window)

        layout = QtWidgets.QGridLayout()

        self.novo_label(layout, 0, 'Lista de pokemons')

        pokemons = QtWidgets.QComboBox()
        pokemons.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        pokemons.addItem('')
        pokemons.currentIndexChanged.connect(partial(self.handle_change_pokemon, pokemons, ))
        layout.addWidget(pokemons, 1, 0)

        self.novo_label(layout, 2, 'Informações')

        form_layout = QtWidgets.QFormLayout()
        layout.addLayout(form_layout, 3, 0)
        self.adicionar_campos_form(form_layout)

        grid_layout_botoes = QtWidgets.QGridLayout()
        layout.addLayout(grid_layout_botoes, 4, 0)

        self.monta_botoes_inferiores(grid_layout_botoes, pokemons)

        centralwidget = QtWidgets.QWidget()
        centralwidget.setLayout(layout)
        main_window.setCentralWidget(centralwidget)

        return main_window, icon, pokemons

    @staticmethod
    def monta_barra_de_status(main_window: QtWidgets.QMainWindow, ):
        statusbar = QtWidgets.QStatusBar()
        statusbar.setObjectName("statusbar")
        main_window.setStatusBar(statusbar)
        statusbar.setFixedHeight(30)

    @staticmethod
    def novo_botao_inferior(texto: str, linha: int, coluna: int, layout: QtWidgets.QGridLayout, ):
        botao = QtWidgets.QPushButton()
        botao.setText(texto)
        layout.addWidget(botao, linha, coluna)

        return botao

    def monta_botoes_inferiores(self, grid_layout: QtWidgets.QGridLayout, pokemons: QtWidgets.QComboBox, ):
        botao_primeiros_20 = self.novo_botao_inferior('Carregar 20 primeiros pokemons', 0, 0, grid_layout)
        botao_primeiros_20.clicked.connect(partial(self.carregar_20_pokemons, pokemons))

        botao_carregar_por_id = self.novo_botao_inferior('Carregar pokemon pelo ID', 0, 1, grid_layout)
        botao_carregar_por_id.clicked.connect(lambda: DialogBuscaPorID(self.icon, self.pokemons))

        botao_limpar_todo_cache = self.novo_botao_inferior('Limpar todo o cache', 1, 0, grid_layout)
        botao_limpar_todo_cache.clicked.connect(lambda: DialogLimparTodoCache(self.icon, self.pokemons))

        botao_limpar_cache_por_id = self.novo_botao_inferior('Limpar pokemon do cache pelo ID', 1, 1, grid_layout)
        botao_limpar_cache_por_id.clicked.connect(lambda: DialogLimparCachePorID(self.icon, self.pokemons))

    @staticmethod
    def novo_label(layout: QtWidgets.QGridLayout, row: int, texto: str, ):
        lb = QtWidgets.QLabel(texto)
        layout.addWidget(lb, row, 0)

    def adicionar_campos_form(self, form_layout: QtWidgets.QFormLayout, ):
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
            valor = em_branco or getattr(pokemon, prop_lower)
            if prop_lower in ['habilidades', 'tipo', ]:
                valor = ', '.join(valor or [])
            getattr(self, 'texto_' + prop_lower).setText(str(valor))

    def atualizar_barra_de_status(self, text: str, ):
        with self.redrawLock:
            self.main_window.statusBar().showMessage(text, 3000)

    def carregar_20_pokemons(self, combo_box: QtWidgets.QComboBox, ):
        for i in range(1, 21):
            pokemon = Pokemon(i)
            pokemon.inserir_na_lista(combo_box)
        self.atualizar_barra_de_status('Pokemons carregados')


if __name__ == '__main__':
    app = PorterMon(sys.argv)
    sys.exit(app.exec())
