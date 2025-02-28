from PyQt5 import QtWidgets, QtCore, uic, QtGui
import sys
from colors import colors


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("main_window_v2.ui", self)

        self.setWindowIcon(QtGui.QIcon("icons/window_icon.png"))
        # self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.NoDropShadowWindowHint)

        self.theme_status = "black"
        self.music_volume = 50
        self.playlist_layout_height = self.scrollAreaWidgetContents_playlist.height()
        self.playlist_cnt = 0
        self.music_list_layout_height = self.scrollAreaWidgetContents_music_list.height()
        self.music_cnt = 0
        self.playlist = []
        self.music_list = []

        self.ThemeSlider.sliderPressed.connect(lambda: self.my_signal(True))
        self.ThemeSlider.actionTriggered.connect(self.my_signal)

        self.volume_slider.setTracking(False)
        self.volume_slider.valueChanged.connect(self.change_volume)

        self.add_widget_to_music_list("test_music_1", "Egor")
        self.add_widget_to_music_list("test_music_2", "Maxim")
        self.add_widget_to_playlist("test_playlist_1")
        self.add_widget_to_playlist("test_playlist_2")

        self.widget_set_icon()
        self.set_style()

        self.AddPlaylistBtn.clicked.connect(self.show_add_playlist)
        self.AddMusicBtn.clicked.connect(self.show_File_Dialog)

        self.sound_btn.clicked.connect(lambda: self.change_volume(0))
        self.sound_btn.setIconSize(QtCore.QSize(40, 40))

    def change_volume(self, value=None):
        if value is not None:
            self.music_volume = value
            self.volume_slider.setValue(self.music_volume)
        else:
            self.music_volume = self.volume_slider.value()
        if not self.music_volume:
            self.sound_btn.setIcon(QtGui.QIcon("icons/volume_zero.png"))
        else:
            self.sound_btn.setIcon(QtGui.QIcon("icons/volume.png"))
        print(f"Music volume: {self.music_volume}.")

    def show_Modal_Error(self):
        modal_window = ModalWindowError(self, "Файл не найден", self.theme_status)
        print(modal_window.exec())

    def show_File_Dialog(self):
        file_dialog_window = ModalFileDialog(self)
        file_dialog_window.exec()
        print(file_dialog_window.selectedFiles())

    def show_add_playlist(self):
        widget = PlaylistAdd(self, self.theme_status)
        widget.exec()
        if widget.result() == 1:
            path, name = widget.foto_path, widget.name.text()
            self.add_widget_to_playlist(name, path)

    def add_widget_to_music_list(self, name: str, author: str, foto_path='icons/music_test.jpg'):
        name = name.strip().replace(' ', '_-_')

        new_widget = QtWidgets.QWidget()
        new_widget.setObjectName(name)

        music_layout = QtWidgets.QHBoxLayout()

        foto_btn = QtWidgets.QPushButton()
        foto_btn.setObjectName(f"{name}_foto")
        foto_btn.clicked.connect(lambda: print(name))
        foto_btn.setToolTip("Нажми на меня для запуска трека")
        foto_btn.setToolTipDuration(1500)
        foto_btn.setStyleSheet(
            f"""
            QPushButton#{name}_foto {{
                border-image: url({foto_path});
                background-color: {colors[self.theme_status]['song_foto']};
                border-radius: 4px;
                min-width: 60px;
                max-width: 60px;
                min-height: 60px;
                max-height: 60px;
                margin: 5 5 5 10;
            }}
            """)
        foto_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        text_widget = QtWidgets.QWidget()
        text_widget.setObjectName(f"{name}_text")

        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setObjectName(f"{name}_text_layout")

        music_name_label = QtWidgets.QLabel(name.replace('_-_', ' '))
        music_name_label.setObjectName(f"{name}_name")

        music_author_label = QtWidgets.QLabel(author)
        music_author_label.setObjectName(f"{name}_author")
        music_author_label.setAlignment(QtCore.Qt.AlignTop)  # noqa

        text_layout.addWidget(music_name_label)
        text_layout.addWidget(music_author_label)

        text_layout.setSpacing(0)
        text_layout.setContentsMargins(0, 0, 0, 0)

        text_widget.setLayout(text_layout)

        duration_label = QtWidgets.QLabel("2:33")
        duration_label.setObjectName(f"{name}_duration")
        duration_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)  # noqa

        music_layout.addWidget(foto_btn)
        music_layout.addWidget(text_widget)
        music_layout.addWidget(duration_label)

        music_layout.setObjectName(f"{name}_layout")
        music_layout.setSpacing(0)
        music_layout.setContentsMargins(0, 0, 0, 0)

        new_widget.setLayout(music_layout)

        self.music_list_layout.insertWidget(0, new_widget)
        if self.music_cnt > 0:
            self.music_list_layout_height += 80
            self.scrollAreaWidgetContents_music_list.setMinimumHeight(self.playlist_layout_height)
        self.music_cnt += 1
        self.music_list.append(new_widget)

    def add_widget_to_playlist(self, name: str, foto_path='icons/playlist_test.jpg', track_cnt=0):
        name = name.strip().replace(' ', '_-_')
        new_widget = QtWidgets.QWidget()
        new_widget.setObjectName(name)

        playlist_layout = QtWidgets.QVBoxLayout()
        playlist_layout.setObjectName(f"{name}_layout")

        foto_btn = QtWidgets.QPushButton()
        foto_btn.setObjectName(f"{name}_foto")
        foto_btn.clicked.connect(lambda: print(name))
        foto_btn.setToolTip("Нажми на меня, чтобы открыть плейлист")
        foto_btn.setToolTipDuration(1500)
        foto_btn.setStyleSheet(
            f"""
            QPushButton#{name}_foto {{
                border-image: url({foto_path});
                background-color: {colors[self.theme_status]['playlist_foto']};
                border-radius: 10px;
                min-width: 100px;
                min-height: 100px;
                max-width: 100px;
                max-height: 100px;
                margin: 10 0 5 40;
            }}
            """)

        playlist_name = QtWidgets.QLabel(name.replace('_-_', ' '))
        playlist_name.setObjectName(f"{name}_name")
        playlist_name.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # noqa

        track_cnt = QtWidgets.QLabel(f"{track_cnt} треков")
        track_cnt.setObjectName(f"{name}_cnt")
        track_cnt.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # noqa

        playlist_layout.addWidget(foto_btn)
        playlist_layout.addWidget(playlist_name)
        playlist_layout.addWidget(track_cnt)

        playlist_layout.setContentsMargins(0, 0, 0, 0)
        playlist_layout.setSpacing(0)

        new_widget.setLayout(playlist_layout)
        new_widget.setContentsMargins(0, 0, 0, 0)
        self.playlist_layout.insertWidget(0, new_widget)
        if self.playlist_cnt > 0:
            self.playlist_layout_height += 200
            self.scrollAreaWidgetContents_playlist.setMinimumHeight(self.playlist_layout_height)
        self.playlist_cnt += 1
        self.playlist.append(new_widget)
        self.set_style()

    def my_signal(self, click=False):
        if click:
            self.ThemeSlider.setValue(0 if self.ThemeSlider.value() else 1)
        self.theme_status = "black" if self.theme_status == "white" else "white"
        self.set_style()

    def set_footer(self):
        pass

    def set_style(self):
        """
        Устанавливаем таблицу стилей для всех элементов
        """
        self.centralwidget.setStyleSheet(
            f"background-color: {colors[self.theme_status]['background']};"
        )
        self.SearchWidget.setStyleSheet(
            f"""
                background-color: {colors[self.theme_status]['search']};
                border-radius: 10px;
            """)
        self.SearchInput.setStyleSheet(f"color: {colors[self.theme_status]['text_search']};"
                                       f"background-color: transparent;")
        self.SearchIcon.setStyleSheet("background-color: transparent;margin-left: 10px;")
        self.Main.setStyleSheet(
            f"""
                QScrollArea {{border: none;}}
                QScrollBar:vertical {{
                      border: transparent;
                      border-top-right-radius: 10px;
                      border-bottom-right-radius: 10px;
                      background-color: {colors[self.theme_status]['songs_list']};
                      width: 10px;
                      margin: 0 0 0 0;
                }}
                QScrollBar::handle:vertical {{
                      min-height: 100px;
                      max-height: 100px;
                      margin: 3 0 3 0;
                      background: {colors[self.theme_status]['handle']};
                      border-radius: 5px;
                }}
                QScrollBar::add-line:vertical {{
                      width: 0px;
                      height: 0px;
                }}
                QScrollBar::sub-line:vertical {{
                      width: 0px;
                      height: 0px;
                }}
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                      width: 0px;
                      height: 0px;
                }}
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                      background: none;
                }}
                QWidget#scrollArea_music_list_widget, QWidget#scrollArea_playlist_widget {{
                    border-top-left-radius: 10px;
                    border-bottom-left-radius: 10px;
                    background-color: {colors[self.theme_status]['songs_list']};
                }}
            """)
        self.footer_widget.setStyleSheet(
            f"""
            QWidget#footer_widget {{
                background-color: {colors[self.theme_status]['songs_track']};
                border-radius: 10px;
            }}
            QWidget#footer_widget QWidget {{
                background: none;
            }}
            
            QPushButton {{
                border: none;
                min-width: 50px;
                max-width: 50px;
                min-height: 50px;
                max-height: 50px;
            }}
            
            QWidget#sound>QPushButton {{
                margin: 0 -5 0 -5;
            }}
            """)
        self.ButtonWidget.setStyleSheet(
            f"""
            QPushButton:hover {{
                background-color: {colors[self.theme_status]['button_pressed']};
            }}
            """
        )
        self.sound.setStyleSheet(
            f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: {colors[self.theme_status]['volume_slider_handle']};
                border: none;
                width: 13px;
                margin: -5px 0;
                border-radius: 6px;
            }}
            QSlider::add-page {{
                background: {colors[self.theme_status]['volume_slider_background_add_page']};
            }}
            
            QSlider::sub-page {{
                background: {colors[self.theme_status]['volume_slider_background_sub_page']};
            }}
            QPushButton:pressed {{
                background-color: {colors[self.theme_status]['button_pressed']};
            }}
            """)
        self.ThemeFrame.setStyleSheet(
            f"""
            QSlider {{
                background: {colors[self.theme_status]['theme']};
                border-radius: 20px;
            }}
            QSlider::groove:horizontal {{
                height: 20px;
                background-color: rgb(170, 170, 170);
                margin: 0px;
                border-radius: 10px;
                background: rgba(0, 0, 0, 0);
            }}
            QSlider::handle:horizontal {{
                background: {colors[self.theme_status]['theme_handle']};
                border: 1px solid #AAAAAA;
                width: 30px;
                margin: -5px 0; 
                border-radius: 15px;
            }}
            """)
        self.play_line_main_widget.setStyleSheet(
            f"""
            .QWidget#play_line_main_widget {{
                background-color: transparent;
            }}
            .QWidget#play_line_foto_widget {{
                background-color: {colors[self.theme_status]['song_foto']};
                border-radius: 4px;
            }}
            """
        )
        self.play_line_btn_widget.setStyleSheet(
            f"""
            QPushButton:hover {{
               background-color: {colors[self.theme_status]['song_foto']};
            }}
            """
        )
        self.play_line_text.setStyleSheet(
            f"""
            QLabel#play_line_music_name {{
                color: {colors[self.theme_status]['text1']}
            }}
            QLabel#play_line_music_author {{
                color: {colors[self.theme_status]['text2']}
            }}
            """
        )
        self.play_line_slider_widget.setStyleSheet(
            f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 3px;
            }}

            QSlider::handle:horizontal {{
                background: {colors[self.theme_status]['song_slider_handle']};
                border: none;
                width: 13px;
                margin: -5px 0;
                border-radius: 6px;
            }}
            QSlider::add-page {{
                background: {colors[self.theme_status]['song_slider_background_add_page']};
            }}

            QSlider::sub-page {{
                background: {colors[self.theme_status]['song_slider_background_sub_page']};
            }}
            """
        )
        self.play_line_time_widget.setStyleSheet(
            f"""
            QLabel {{
                color: {colors[self.theme_status]['text2']};
            }}
            """
        )
        for widget in self.playlist:
            if self.theme_status == 'white':
                widget.setGraphicsEffect(None)
            else:
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                    offset=QtCore.QPoint(3, 3), blurRadius=25, color=QtGui.QColor("#111")  # noqa
                )
                widget.setGraphicsEffect(shadow_effect)
            widget.setStyleSheet(
                f"""
                QWidget#{widget.objectName()} {{
                    background-color: {colors[self.theme_status]['playlist']};
                    border-radius: 7px;
                    min-width: 180px;
                    min-height: 180px;
                    max-width: 180px;
                    max-height: 180px;
                }}
                QPushButton#{widget.objectName()}_foto {{
                    background-color: {colors[self.theme_status]['playlist_foto']};
                    border-radius: 10px;
                    min-width: 100px;
                    min-height: 100px;
                    max-width: 100px;
                    max-height: 100px;
                    margin: 10 0 5 40;
                }}
                .QLabel#{widget.objectName()}_name {{
                    color: {colors[self.theme_status]['text1']};
                    margin-top: 5px;
                    max-width: 180px;
                    max-height: 20px;
                    background-color: transparent;
                    font-size: 17px;
                }}
                .QLabel#{widget.objectName()}_cnt {{
                    color: {colors[self.theme_status]['text2']};
                    max-width: 180px;
                    background-color: transparent;
                    font-size: 17px;
                }}
                """)
        for widget in self.music_list:
            if self.theme_status == 'white':
                widget.setGraphicsEffect(None)
            else:
                shadow_effect = QtWidgets.QGraphicsDropShadowEffect(
                    offset=QtCore.QPoint(3, 3), blurRadius=25, color=QtGui.QColor("#111")  # noqa
                )
                widget.setGraphicsEffect(shadow_effect)
            widget.setStyleSheet(
                f"""
                QWidget#{widget.objectName()} {{
                    background-color: {colors[self.theme_status]['song']};
                    border-radius: 7px;
                    min-height: 70px;
                    max-height: 70px;
                }}
                .QPushButton#{widget.objectName()}_foto {{
                    background-color: {colors[self.theme_status]['song_foto']};
                    border-radius: 4px;
                    min-width: 60px;
                    max-width: 60px;
                    min-height: 60px;
                    max-height: 60px;
                    margin: 5 5 5 10;
                }}
                QWidget#{widget.objectName()}_text {{
                    background-color: transparent;
                    max-height: 65px;
                }}
                QLabel#{widget.objectName()}_name {{
                    background-color: transparent;
                    color: {colors[self.theme_status]['text1']};
                    font-size: 21px;
                }}
                QLabel#{widget.objectName()}_author {{
                    background-color: transparent;
                    color: {colors[self.theme_status]['text2']};
                    font-size: 21px;
                }}
                QWidget#{widget.objectName()}_duration {{
                    background-color: transparent;
                    margin: 0 10 0 5;
                    font-size: 21px;
                    color: {colors[self.theme_status]['text1']};
                }}
                """
            )

    def widget_set_icon(self):
        """
        Устанавливаем все иконки
        """
        try:
            self.LogoIcon.setPixmap(QtGui.QPixmap("icons/logo.png"))
            self.SearchIcon.setPixmap(QtGui.QPixmap("icons/search_black.svg"))
            self.SunIcon.setPixmap(QtGui.QPixmap("icons/sun.svg"))
            self.MoonIcon.setPixmap(QtGui.QPixmap("icons/moon.png"))
            self.AddPlaylistBtn.setIcon(QtGui.QIcon("icons/new_plalist1.png"))
            self.AddMusicBtn.setIcon(QtGui.QIcon("icons/append.png"))
            self.back_btn.setIcon(QtGui.QIcon("icons/back.png"))
            self.pause_btn.setIcon(QtGui.QIcon("icons/pause.png"))
            self.next_btn.setIcon(QtGui.QIcon("icons/next.png"))
            self.sound_btn.setIcon(QtGui.QIcon("icons/volume.png"))
            self.shuffle_btn.setIcon(QtGui.QIcon("icons/shuffle.png"))
            self.repeat_btn.setIcon(QtGui.QIcon("icons/repeat.png"))
        except Exception as error_msg:
            print(error_msg)

    def hide_footer(self):
        self.Footer.hide()
        self.Main.setContentsMargins(0, 30, 0, 30)


class ModalWindowError(QtWidgets.QDialog):
    def __init__(self, parent, error_msg, theme):
        super().__init__(parent)
        self.resize(QtCore.QSize(300, 100))
        self.setWindowTitle("Error")
        self.setWindowModality(QtCore.Qt.WindowModal)  # noqa
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # noqa
        self.setStyleSheet(f"background-color: {colors[theme]['background']};")

        box = QtWidgets.QDialogButtonBox(parent=self)
        box.setStyleSheet(
            f"""
                margin: 0 5 5 0;
                min-width: 50px;
                min-height: 20px;
            """)

        btn_ok = QtWidgets.QPushButton("&OK")
        btn_ok.clicked.connect(lambda: self.done(1))

        box.addButton(btn_ok, QtWidgets.QDialogButtonBox.AcceptRole)

        error_msg_layout = QtWidgets.QVBoxLayout()
        error_msg_layout.setContentsMargins(0, 0, 0, 0)
        error_msg_layout.setSpacing(0)

        error_msg_label = QtWidgets.QLabel(error_msg)
        error_msg_label.setAlignment(QtCore.Qt.AlignCenter)  # noqa
        error_msg_label.setStyleSheet(
            f"""
                color: {colors[theme]['text1']};
                background-color: {colors[theme]['background']};
                font-size: 21px;
            """)

        error_msg_layout.addWidget(error_msg_label)
        error_msg_layout.addWidget(box)
        self.setLayout(error_msg_layout)


class ModalFileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.setNameFilters(["All (*)", "MP3 (*.mp3)", "WAV (*.wav)", "AIFF (*.aiff)"])


class ModalFileDialogPixmap(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.setNameFilters(["All (*)", "PNG (*.png)", "JPG (*.jpg)", "JPEG (*.JPEG)"])


class PlaylistAdd(QtWidgets.QDialog):
    def __init__(self, parent, theme):
        super().__init__(parent)
        uic.loadUi("playlist_add.ui", self)
        self.foto_path = "icons/playlist_test.jpg"
        self.setWindowModality(QtCore.Qt.WindowModal)  # noqa
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)  # noqa
        self.setWindowTitle("Новый плейлист")
        self.resize(QtCore.QSize(470, 500))
        self.setObjectName("MainWindow")

        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() // 2 - self.width() // 2)
        y = (desktop.height() // 2 - self.height() // 2)
        self.move(x, y)
        self.set_style(theme)

        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn.clicked.connect(self.add_playlist)
        self.foto_btn.clicked.connect(self.foto_set_pixmap)
        self.foto_btn.setToolTip("Нажми на меня, чтобы изменить фото")
        self.foto_btn.setToolTipDuration(3000)

    def foto_set_pixmap(self):
        file_dialog_window = ModalFileDialogPixmap(self)
        file_dialog_window.exec()
        path = file_dialog_window.selectedFiles()
        if path:
            self.foto_path = path[0]
            self.foto_btn.setStyleSheet(
                f"""
                    border-image: url({self.foto_path});
                """
            )

    def set_style(self, theme):
        self.setStyleSheet(
            f"""
            QWidget#MainWindow {{
                background-color: {colors[theme]['playlist_background']};
                min-width: 470px;
                max-width: 470px;
                min-height: 470px;
                max-height: 470px; 
            }}
            QWidget#foto_widget, QWidget#name_widget, QWidget#btn_widget, QWidget#btn_spacer_widget {{
                background-color: {colors[theme]['playlist_background']};
            }}
            QPushButton#foto_btn {{
                background-color: {colors[theme]['song_foto']};
                border-image: url(icons/playlist_test.jpg);
                border-radius: 15px;
                min-width: 156px;
                max-width: 156px;
                min-height: 171px;
                max-height: 171px;
            }}
            QLineEdit#name {{
                background-color: {colors[theme]['playlist_name_edit']};
                color: {colors[theme]['text1']};
                border-radius: 8px;
                border: 2px solid rgba(0, 0, 0, 0.5);
                min-width: 225px;
                max-width: 225px;
                min-height: 30px;
                max-height: 30px;
            }}
            QPushButton#cancel_btn, QPushButton#add_btn {{
                background-color: rgba(217, 217, 217, 0.2);
                border: 2px solid rgba(0, 0, 0, 0.5);
                border-radius: 7px;
                color: {colors[theme]['text1']};
                min-width: 130px;
                max-width: 130px;
                min-height: 40px;
                max-height: 40px;
            }}
            """
        )

    def add_playlist(self):
        self.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
