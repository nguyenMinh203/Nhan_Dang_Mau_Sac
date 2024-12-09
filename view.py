import cv2
from tkinter import filedialog, Tk

class ColorRecognitionView:
    def __init__(self):
        self.image = None

    def select_image(self):
        """
        Hiển thị hộp thoại để chọn ảnh.
        """
        Tk().withdraw()  # Ẩn cửa sổ gốc của Tkinter
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            cv2.imshow('Selected Image', self.image)
            return file_path
        return None

    def display_image_with_callback(self, callback):
        """
        Hiển thị ảnh và gán hàm xử lý sự kiện click chuột.
        """
        if self.image is not None:
            cv2.imshow('Selected Image', self.image)
            cv2.setMouseCallback('Selected Image', callback)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
