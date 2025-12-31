import sys
import json
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import yt_dlp

class YouTubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pro YouTube Player & Downloader")
        self.setGeometry(100, 100, 1300, 850)
        
        # Veri dosyası
        self.db_file = "playlist.json"
        self.load_playlist()

        # Ana Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # --- SOL PANEL ---
        self.side_panel = QVBoxLayout()
        self.label = QLabel("📋 Oynatma Listem")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        self.side_panel.addWidget(self.label)

        self.playlist_widget = QListWidget()
        self.playlist_widget.itemDoubleClicked.connect(self.play_from_list)
        self.side_panel.addWidget(self.playlist_widget)
        self.refresh_list_ui()

        self.add_list_btn = QPushButton("➕ Listeye Ekle")
        self.add_list_btn.clicked.connect(self.add_to_playlist)
        self.side_panel.addWidget(self.add_list_btn)

        self.remove_btn = QPushButton("🗑️ Seçileni Sil")
        self.remove_btn.clicked.connect(self.remove_from_playlist)
        self.side_panel.addWidget(self.remove_btn)
        
        self.main_layout.addLayout(self.side_panel, 1)

        # --- SAĞ PANEL ---
        self.right_panel = QVBoxLayout()

        # Navigasyon ve Kontroller
        self.nav_bar = QHBoxLayout()
        
        self.back_btn = QPushButton("⬅ Geri")
        # Tarayıcıyı sonra tanımlayacağımız için bağlantıyı aşağıda yapacağız
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Video URL...")
        
        self.download_mp4_btn = QPushButton("🎬 MP4 İndir")
        self.download_mp4_btn.setStyleSheet("background-color: #cc0000; color: white;")
        self.download_mp4_btn.clicked.connect(lambda: self.download_video(mode='mp4'))

        self.download_mp3_btn = QPushButton("🎵 MP3 İndir")
        self.download_mp3_btn.setStyleSheet("background-color: #2ecc71; color: white;")
        self.download_mp3_btn.clicked.connect(lambda: self.download_video(mode='mp3'))

        self.nav_bar.addWidget(self.back_btn)
        self.nav_bar.addWidget(self.url_input)
        self.nav_bar.addWidget(self.download_mp4_btn)
        self.nav_bar.addWidget(self.download_mp3_btn)
        self.right_panel.addLayout(self.nav_bar)

        # Tarayıcı (Önce tarayıcıyı oluşturuyoruz)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.youtube.com"))
        self.browser.urlChanged.connect(self.update_url_field)
        
        # Geri butonu bağlantısını şimdi güvenle yapabiliriz
        self.back_btn.clicked.connect(self.browser.back)
        
        self.right_panel.addWidget(self.browser, 5)
        self.main_layout.addLayout(self.right_panel, 4)

    # --- FONKSİYONLAR ---
    def update_url_field(self, q):
        self.url_input.setText(q.toString())

    def load_playlist(self):
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self.playlist_data = json.load(f)
            else:
                self.playlist_data = []
        except: self.playlist_data = []

    def save_playlist(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.playlist_data, f, ensure_ascii=False)

    def refresh_list_ui(self):
        self.playlist_widget.clear()
        for item in self.playlist_data:
            self.playlist_widget.addItem(item['title'])

    def add_to_playlist(self):
        url = self.url_input.text()
        # Başlığı URL'den basitçe alalım, indirme anında gerçek başlık gelir
        title = f"Video {len(self.playlist_data) + 1}" 
        self.playlist_data.append({"title": title, "url": url})
        self.save_playlist()
        self.refresh_list_ui()

    def remove_from_playlist(self):
        row = self.playlist_widget.currentRow()
        if row >= 0:
            self.playlist_data.pop(row)
            self.save_playlist()
            self.refresh_list_ui()

    def play_from_list(self, item):
        index = self.playlist_widget.currentRow()
        url = self.playlist_data[index]['url']
        self.browser.setUrl(QUrl(url))

    def download_video(self, mode='mp4'):
        url = self.url_input.text()
        if "youtube.com" not in url and "youtu.be" not in url:
            return

        path = QFileDialog.getExistingDirectory(self, "Kayıt Yerini Seç")
        if not path: return

        # İndirme Ayarları
        if mode == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
            }

        try:
            QMessageBox.information(self, "Bilgi", "İndirme arka planda başladı...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, "Tamamlandı", "İndirme başarılı!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())