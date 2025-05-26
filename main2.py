import pymysql
from enter import Ui_Mebel
from product import Ui_Mebel2
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QInputDialog
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QTime
def connect_to_bd():
    return pymysql.connect(
        host="localhost",
        user="root",
        database="mebel"
    )

class Product(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Mebel2()
        self.ui.setupUi(self)
        self.connect_bd = connect_to_bd()
        self.ui.BackButton.clicked.connect(self.back)
        self.ui.DelButton.clicked.connect(self.del_product)
        self.ui.AddButton.clicked.connect(self.add_product)
        self.products()

    def products(self):
        try:
            cursor = self.connect_bd.cursor()
            cursor.execute("""SELECT type.name,
            tovar.name, tovar.articul, tovar.cost, tovar.t_made, material.name
            FROM tovar
            JOIN type ON tovar.id_type = type.id
            JOIN tovar_material ON tovar.id = tovar_material.id_tovar
            JOIN material ON tovar_material.id_material = material.id""")
            result = cursor.fetchall()
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['Тип', 'Наименование продукта', 'Артикул', 'Минимальная стоимость', 'Время изготовления (мин)', 'Основной материал'])
            for row in result:
                x = [QStandardItem(str(f)) for f in row]
                model.appendRow(x)
            self.ui.tableView.setModel(model)
            self.ui.tableView.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")

    def back(self):
        self.ui = Enter()
        self.ui.show()
        self.close()

    def del_product(self):
        selection = self.ui.tableView.selectionModel().selectedRows()
        if not selection:
            QMessageBox.warning(self, "Ошибка", "Выберите строку")
            return
        index = selection[0]
        product_articul = index.sibling(index.row(), 2).data()
        try:
            cursor = self.connect_bd.cursor()
            cursor.execute("DELETE FROM tovar WHERE articul = %s", (product_articul,))
            self.connect_bd.commit()
            self.products()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")

    def add_product(self):
        name, ok = QInputDialog.getText(self, "Наименование", "Введите наименование")
        articul, ok2 = QInputDialog.getText(self, "Артикул", "Введите артикул")
        costs, ok3 = QInputDialog.getDouble(self, "Цена", "Введите стоимость", decimals=2)
        t_made, ok4 = QInputDialog.getInt(self, "Время изготовления", "Введите время в минутах")
        items = ["Дерево", "Хлопок"]
        item, ok5 = QInputDialog.getItem(self, "Выберите материал", "Материал:", items, 0, False)
        cursor = self.connect_bd.cursor()
        cursor.execute("SELECT id FROM material WHERE name = %s", (item,))
        result1 = cursor.fetchone()
        material_id = result1[0]
        cursor = self.connect_bd.cursor()
        item2 = ["Детская мебель", "Мебель для гостиной"]
        items2, ok6 = QInputDialog.getItem(self, "Выберите тип", "Тип:", item2, 0, False)
        cursor.execute("SELECT id FROM type WHERE name = %s", (items2,))
        result2 = cursor.fetchone()
        type_id = result2[0]
        if not all([ok, ok2, ok6, ok5, ok3, ok4]):
            QMessageBox.information(self, "Отменено", "Добавление отменено.")
            return
        try:
            cursor = self.connect_bd.cursor()
            cursor.execute("""INSERT INTO tovar (name, articul, cost, t_made, id_model, id_type)
            VALUES (%s, %s, %s, %s, %s, %s)""", (name, articul, costs, t_made, material_id, type_id))
            tovar_id = cursor.lastrowid
            cursor.execute("""INSERT INTO tovar_material (id_tovar, id_material)
            VALUES (%s, %s)""", (tovar_id, material_id))
            self.connect_bd.commit()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")
        self.products()



class Enter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Mebel()
        self.ui.setupUi(self)
        self.ui.ButtonProduct.clicked.connect(self.ProductWin)

    def ProductWin(self):
        self.pw = Product()
        self.pw.show()
        self.close()