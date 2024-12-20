from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QWidget, QDialog, QLabel
)
import win32api
import os
import sys


class MainApp(QWidget):
    def __init__(self, folder_path=None):
        super().__init__()
        # 아이콘 초기화
        self.drive_icon = QIcon("./file_icon.png")
        self.folder_path = folder_path
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("종합 버튼 기능 구현")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # 파일 탐색기 스타일 트리 구조
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.itemClicked.connect(self.handle_item_click)
        self.file_tree.setIconSize(QtCore.QSize(16, 16))

        # 선택된 폴더의 내용을 표시
        self.populate_root_nodes(self.folder_path)

        layout.addWidget(self.file_tree)
        self.setLayout(layout)

    def populate_root_nodes(self, folder_path=None):
        """
        초기 트리에 선택한 폴더의 내용을 추가합니다.
        """
        self.file_tree.clear()  # 기존 항목 제거
        if folder_path:
            folder_name = os.path.basename(folder_path)
            root = QTreeWidgetItem(self.file_tree, [folder_name])
            root.setIcon(0, self.drive_icon)
            root.setData(0, 1, folder_path)

            # 선택한 폴더의 내용을 트리에 추가
            try:
                for entry in os.listdir(folder_path):
                    full_path = os.path.join(folder_path, entry)
                    item = QTreeWidgetItem(root, [entry])
                    if os.path.isdir(full_path):
                        item.setIcon(0, self.drive_icon)
                    else:
                        file_icon = QIcon("./file_icon.png")
                        item.setIcon(0, file_icon)
                    item.setData(0, 1, full_path)
            except Exception as e:
                print(f"폴더 내용을 불러오는 중 오류 발생: {e}")

            root.setExpanded(True)

    def update_folder(self, new_folder_path):
        """
        폴더 경로를 업데이트하고 트리를 다시 그립니다.
        """
        self.folder_path = new_folder_path
        self.populate_root_nodes(new_folder_path)

    def add_drive(self, parent, drive_letter):
        """
        루트에 드라이브를 추가하고 아이콘을 설정합니다.
        """
        drive_item = QTreeWidgetItem(parent, [f"로컬 디스크 ({drive_letter})"])
        drive_item.setIcon(0, self.drive_icon)  # 드라이브 아이콘 설정
        drive_item.setData(0, 1, drive_letter)

    def handle_item_click(self, item, column):
        """
        트리 항목 클릭 이벤트 처리.
        """
        try:
            drive_letter = item.data(0, 1)
            if drive_letter:
                print(f"클릭된 항목: {drive_letter}")
                self.populate_directory(item, drive_letter)
            else:
                print("잘못된 항목 데이터")
        except Exception as e:
            print(f"트리 항목 클릭 처리 중 오류 발생: {e}")

    def populate_directory(self, parent_item, path):
        """
        선택된 디렉토리의 하위 항목(폴더 및 파일)을 트리에 추가하고 아이콘을 설정합니다.
        """
        parent_item.takeChildren()  # 기존 하위 항목 제거
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                sub_item = QTreeWidgetItem(parent_item, [entry])
                if os.path.isdir(full_path):
                    sub_item.setIcon(0, self.drive_icon)  # 폴더 아이콘 설정
                    sub_item.setData(0, 1, full_path)
                else:
                    # 파일 아이콘 설정 (폴더와 구분하기 위해)
                    file_icon = QIcon("./file_icon.png")  # 파일 아이콘 이미지 설정
                    sub_item.setIcon(0, file_icon)
                    sub_item.setData(0, 1, full_path)
        except PermissionError:
            print(f"권한 부족으로 {path}의 내용을 읽을 수 없습니다.")
        except FileNotFoundError:
            print(f"{path} 경로를 찾을 수 없습니다.")
        except Exception as e:
            print(f"예기치 못한 오류 발생: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())