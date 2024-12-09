from controller import ColorRecognitionController

if __name__ == "__main__":
    dataset_path = r"D:\baitaplon\xlha\btlXLHA\training_dataset"
    csv_path = r"D:\baitaplon\xlha\btlXLHA\training2\colors.csv"

    # Lựa chọn thuật toán
    algorithm = input("Chọn thuật toán (SVM, KNN, DecisionTree): ").strip()

    controller = ColorRecognitionController(dataset_path, csv_path, algorithm)

    print(f"Đang huấn luyện mô hình với thuật toán {algorithm}...")
    controller.train_model()

    print("Bắt đầu nhận diện màu sắc...")
    controller.recognize_color()
