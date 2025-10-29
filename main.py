import sys
from PyQt5.QtWidgets import QApplication
from auth.login import LoginDialog

def main():
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec_():
        from ui.main_window import MainWindow
        main_window = MainWindow(login_dialog.current_user)
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
