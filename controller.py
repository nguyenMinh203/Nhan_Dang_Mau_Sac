from model import ColorRecognitionModel
from view import ColorRecognitionView
import cv2

class ColorRecognitionController:
    def __init__(self, dataset_path, csv_path, algorithm='SVM'):
        """
        Khởi tạo controller với thuật toán được chọn.
        """
        self.model = ColorRecognitionModel(dataset_path, csv_path, algorithm)
        self.view = ColorRecognitionView()

    def train_model(self):
        """
        Huấn luyện mô hình.
        """
        self.model.train_model()

    def recognize_color(self):
        """
        Nhận diện màu sắc từ ảnh.
        """
        file_path = self.view.select_image()
        if file_path:
            self.model.load_model()
            print(f"Độ chính xác của mô hình ({self.model.algorithm}): {self.model.accuracy:.2f}")
            self.view.display_image_with_callback(self.handle_click)

    def handle_click(self, event, x, y, flags, param):
        """
        Xử lý sự kiện click chuột và dự đoán màu sắc.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            b, g, r = self.view.image[y, x]
            rgb = (r, g, b)
            print(f"RGB tại điểm ({x}, {y}): {rgb}")

            label = self.model.predict_color(rgb)
            print(f"Màu sắc dự đoán: {label}")
            print(f"Độ chính xác của mô hình ({self.model.algorithm}): {self.model.accuracy:.2f}")
