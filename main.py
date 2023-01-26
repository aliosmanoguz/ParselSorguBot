from PyQt5.QtWidgets import QApplication
from giris_ui_python import girisPencere

app = QApplication([])
pencere = girisPencere()
pencere.show()
app.exec_()
