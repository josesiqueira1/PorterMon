from PyQt5 import QtWidgets, QtGui


class DialogPadrao(QtWidgets.QDialog):
    def __init__(self, icon: QtGui.QIcon, texto: str, ):
        super().__init__()

        self.resize(200, 50)
        self.setWindowTitle("Limpar cache")

        self.setWindowIcon(icon)

        q_btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        button_box = QtWidgets.QDialogButtonBox(q_btn)
        button_box.accepted.connect(self.accepted_function)
        button_box.rejected.connect(lambda: self.close())

        layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(texto)

        layout.addWidget(message)
        self.montar_itens_adicionais(layout)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.exec()

    def accepted_function(self, ):
        raise NotImplementedError()

    @staticmethod
    def montar_itens_adicionais(layout: QtWidgets.QVBoxLayout):
        raise NotImplementedError()


class DialogPorID(DialogPadrao):
    def __init__(self, icon: QtGui.QIcon, combo_box_pokemons: QtWidgets.QComboBox, texto: str, ):
        self.id_pokedex = 1
        self.combo_box_pokemons = combo_box_pokemons
        super().__init__(icon, texto)

    def accepted_function(self, ):
        pass

    def montar_itens_adicionais(self, layout):
        input_numero = QtWidgets.QSpinBox()
        input_numero.setValue(1)
        input_numero.setRange(1, 898)
        input_numero.valueChanged.connect(lambda value: setattr(self, 'id_pokedex', value))
        layout.addWidget(input_numero)
