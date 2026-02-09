import sys
import requests
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox
)


class ChemicalDashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Dashboard")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        # Title
        self.title = QLabel("Chemical Equipment Dashboard")
        self.title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(self.title)

        # Summary text
        self.summary_label = QLabel("Click 'Load Summary' to fetch data")
        layout.addWidget(self.summary_label)

        # Load summary button
        self.load_btn = QPushButton("Load Summary")
        self.load_btn.clicked.connect(self.load_summary)
        layout.addWidget(self.load_btn)

        # Upload CSV button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        layout.addWidget(self.upload_btn)

        # 👉 NEW: Show chart button
        self.chart_btn = QPushButton("Show Equipment Chart")
        self.chart_btn.clicked.connect(self.show_chart)
        layout.addWidget(self.chart_btn)

        self.setLayout(layout)

    def load_summary(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/summary/")
            data = response.json()

            text = (
                f"Total Equipment: {data['total_equipment']}\n"
                f"Avg Flowrate: {data['averages']['avg_flowrate']}\n"
                f"Avg Pressure: {data['averages']['avg_pressure']}\n"
                f"Avg Temperature: {data['averages']['avg_temperature']}"
            )

            self.summary_label.setText(text)

        except Exception:
            QMessageBox.critical(self, "Error", "Backend not running")

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            files = {'file': open(file_path, 'rb')}
            response = requests.post(
                "http://127.0.0.1:8000/api/upload/",
                files=files
            )

            if response.status_code == 201:
                QMessageBox.information(
                    self,
                    "Success",
                    "CSV uploaded successfully"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Failed",
                    "Upload failed"
                )

        except Exception:
            QMessageBox.critical(self, "Error", "Backend not running")

    def show_chart(self):
        try:
            response = requests.get("http://127.0.0.1:8000/api/summary/")
            data = response.json()

            labels = [item['equipment_type'] for item in data['type_distribution']]
            counts = [item['count'] for item in data['type_distribution']]

            plt.figure(figsize=(6, 4))
            plt.bar(labels, counts)
            plt.title("Equipment Type Distribution")
            plt.xlabel("Equipment Type")
            plt.ylabel("Count")
            plt.tight_layout()
            plt.show()

        except Exception:
            QMessageBox.critical(self, "Error", "Unable to load chart")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChemicalDashboard()
    window.show()
    sys.exit(app.exec_())
