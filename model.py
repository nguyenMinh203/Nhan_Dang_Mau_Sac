import os
import cv2
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

class ColorRecognitionModel:
    def __init__(self, dataset_path, csv_path, algorithm='SVM'):
        """
        Khởi tạo model với thuật toán mặc định là SVM.
        """
        self.dataset_path = dataset_path
        self.csv_path = csv_path
        self.algorithm = algorithm
        self.model = None
        self.accuracy = 0.0
        self.metrics = {}  # Lưu các độ đo: precision, recall, f1-score

    def load_image_data(self):
        """
        Đọc dữ liệu từ thư mục ảnh và trích xuất đặc trưng RGB trung bình.
        """
        features = []
        labels = []

        for label in os.listdir(self.dataset_path):
            label_dir = os.path.join(self.dataset_path, label)
            if os.path.isdir(label_dir):
                for file_name in os.listdir(label_dir):
                    file_path = os.path.join(label_dir, file_name)
                    # Đọc ảnh
                    img = cv2.imread(file_path)
                    if img is not None:
                        # Tính RGB trung bình
                        mean_rgb = img.mean(axis=(0, 1))
                        features.append(mean_rgb[::-1])  # Đảo BGR -> RGB
                        labels.append(label)

        return np.array(features), np.array(labels)

    def load_csv_data(self):
        """
        Đọc dữ liệu từ file CSV.
        """
        try:
            df = pd.read_csv(self.csv_path, header=None)
            df.columns = ['ColorName', 'FullDescription', 'Hex', 'R', 'G', 'B']
            features = df[['R', 'G', 'B']].values
            labels = df['ColorName'].values
            return features, labels
        except FileNotFoundError:
            print(f"File CSV không tìm thấy: {self.csv_path}")
            return None, None
        except Exception as e:
            print(f"Lỗi khi đọc file CSV: {e}")
            return None, None

    def load_data(self):
        """
        Kết hợp dữ liệu từ thư mục ảnh và file CSV.
        """
        img_features, img_labels = self.load_image_data()
        csv_features, csv_labels = self.load_csv_data()

        if csv_features is None or csv_labels is None:
            return img_features, img_labels

        features = np.vstack((img_features, csv_features))
        labels = np.concatenate((img_labels, csv_labels))
        return features, labels

    def select_algorithm(self):
        """
        Chọn thuật toán huấn luyện dựa trên tham số đầu vào.
        """
        if self.algorithm == 'SVM':
            return SVC(kernel='linear', probability=True)
        elif self.algorithm == 'KNN':
            return KNeighborsClassifier(n_neighbors=5)
        elif self.algorithm == 'DecisionTree':
            return DecisionTreeClassifier()
        else:
            raise ValueError(f"Thuật toán '{self.algorithm}' không được hỗ trợ.")

    def train_model(self):
        """
        Huấn luyện mô hình với thuật toán được chọn và tính toán các độ đo.
        """
        X, y = self.load_data()
        if X is None or y is None:
            print("Không có dữ liệu để huấn luyện.")
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Chọn thuật toán
        self.model = self.select_algorithm()
        self.model.fit(X_train, y_train)

        # Dự đoán trên tập kiểm tra
        y_pred = self.model.predict(X_test)

        # Tính toán các độ đo
        self.accuracy = accuracy_score(y_test, y_pred)
        self.metrics['Precision'] = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        self.metrics['Recall'] = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        self.metrics['F1-score'] = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        print(f"Model trained with {self.algorithm}")
        print(f"Accuracy: {self.accuracy:.2f}")
        print(f"Precision: {self.metrics['Precision']:.2f}")
        print(f"Recall: {self.metrics['Recall']:.2f}")
        print(f"F1-score: {self.metrics['F1-score']:.2f}")

        # Lưu mô hình
        with open(f'color_model_{self.algorithm}.pkl', 'wb') as f:
            pickle.dump((self.model, self.accuracy, self.metrics), f)

    def load_model(self):
        """
        Tải mô hình đã lưu dựa trên thuật toán.
        """
        try:
            with open(f'color_model_{self.algorithm}.pkl', 'rb') as f:
                self.model, self.accuracy, self.metrics = pickle.load(f)
        except FileNotFoundError:
            print(f"Không tìm thấy mô hình đã lưu cho thuật toán {self.algorithm}")
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")

    def predict_color(self, rgb):
        """
        Dự đoán nhãn màu từ giá trị RGB.
        """
        if self.model is None:
            self.load_model()
        return self.model.predict([rgb])[0]
