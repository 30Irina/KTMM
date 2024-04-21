import sys
import matplotlib.pyplot as plt
from PyQt6.QtGui import QAction
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from read_param import read_param
from solve_ode import HeatEquationSolver
from write_param import ModelCalculator
import warnings
warnings.filterwarnings('ignore', 'The iteration is not making good progress')

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Решение уравнения теплопроводности")
        #self.resize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.result_path = ''
        self.start_temp_path = ''
        self.params_path = ''
        self.params = None
        self.ode_sol = []

        self.initialization_button = QPushButton("Инициализация параметров и S_i/S_ij", self)
        self.initialization_button.clicked.connect(self.initialization_params)
        self.initialization_button_clicked = False

        self.param_button = QPushButton("Параметры", self)
        self.param_button.clicked.connect(self.read_parameters)
        self.param_button_clicked = False

        self.start_button = QPushButton("Начать расчет", self)
        self.start_button.clicked.connect(self.start_calculation)
        self.start_button_clicked = False

        self.start_temp_button = QPushButton("Стартовая температура", self)
        self.start_temp_button.clicked.connect(self.start_temperature)
        self.start_temp_button_clicked = False

        self.without_start_temp_button = QPushButton("Без стартовой температуры", self)
        self.without_start_temp_button.clicked.connect(self.without_start_temperature)
        self.without_start_temp_button_clicked = False

        self.plot_button = QPushButton("Построить график", self)
        self.plot_button.clicked.connect(self.plotting_solution)

        self.save_button = QPushButton("Сохранить результаты", self)
        self.save_button.clicked.connect(self.save_solution)

        toolbar = self.addToolBar("Tools")
        toolbar.addWidget(self.initialization_button)
        toolbar.addWidget(self.param_button)
        toolbar.addWidget(self.start_temp_button)
        toolbar.addWidget(self.without_start_temp_button)
        toolbar.addWidget(self.start_button)
        toolbar.addWidget(self.plot_button)
        toolbar.addWidget(self.save_button)


    def initialization_params(self):
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("OBJ files (*.obj)")

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                calculator = ModelCalculator(file_path)
                calculator.calculate_and_write_areas()

                QMessageBox.information(self, "Успех", "Параметры и S_i/S_ij успешно проинициализированы.")
                self.initialization_button_clicked = True
        else:
            QMessageBox.warning(self, "Предупреждение", "Не выбран файл с моделью.")
        return


    def start_calculation(self):
        if not (self.without_start_temp_button_clicked or self.start_temp_button_clicked):
            QMessageBox.warning(self, "Ошибка", "Не выбран файл со стартовыми температурами или вариант расчета без них")
        else:
            if self.params_path != '':
                self.start_button_clicked = True
                self.params = read_param(self.params_path, self.start_temp_path)
                heat_solver = HeatEquationSolver(params=self.params)

                if self.start_temp_path == '':
                    self.params.start_temp = heat_solver.solve_equation_stat(self.params)
                self.solution = heat_solver.solve_equation(self.params)
            else:
                QMessageBox.warning(self, "Ошибка", "Не выбран файл с параметрами")
        return


    def read_parameters(self):
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog)

        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")

        if file_dialog.exec():
            self.param_button_clicked = True
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                filename = selected_files[0]
                self.params_path = filename
                #print("Выбранный файл с параметрами:", filename)
        else:
            QMessageBox.warning(self, "Предупреждение", "Не выбран файл с параметрами")
        return


    def start_temperature(self):
        file_dialog = QFileDialog()
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("CSV files (*.csv)")

        if file_dialog.exec():
            self.start_temp_button_clicked = True
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                filename = selected_files[0]
                self.start_temp_path = filename
                #print("Выбранный файл с температурой:", filename)
        else:
            QMessageBox.warning(self, "Предупреждение", "Не выбран файл с температурой")
        return


    def without_start_temperature(self):
        self.start_temp_path = ''
        self.without_start_temp_button_clicked = True
        return


    def plotting_solution(self):
        if not (self.start_button_clicked):
            QMessageBox.warning(self, "Ошибка", "Не была нажата кнопка <Начать расчет>")
        else:
            self.ax.clear()
            labels = [r'$T_1(t)$', r'$T_2(t)$', r'$T_3(t)$', r'$T_4(t)$', r'$T_5(t)$']
            for i in range(5):
                self.ax.plot(self.params.time_grid[:], self.solution[:, i], label=labels[i])
            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_title('Динамика изменения температур КЭ')
            self.ax.set_xlabel('Время')
            self.ax.set_ylabel('Температура')
            self.fig.tight_layout()
            self.canvas.draw()

        return


    def save_solution(self):
        if not (self.start_button_clicked):
            QMessageBox.warning(self, "Ошибка", "Не была нажата кнопка <Начать расчет>")
        else:
            file_dialog = QFileDialog()
            file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
            file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
            file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            file_dialog.setNameFilter("CSV files (*.csv)")

            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                if selected_files:
                    filename = selected_files[0]
                    with open(filename, 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['Time', 'T1', 'T2', 'T3', 'T4', 'T5'])
                        for time, row in zip(self.params.time_grid, self.solution):
                            writer.writerow([time] + row.tolist())
        self.start_button_clicked = False
        self.param_button_clicked = False
        self.start_temp_button_clicked = False
        self.without_start_temp_button_clicked = False
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())




