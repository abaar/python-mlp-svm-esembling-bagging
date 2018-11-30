# from bagging import bagging

# main = bagging()

# main.read_dataset("iris")

# main.create_bag()

# main.train_data()

# main.test_model()

# main.calculate_model_average()

# print(main.getAccuracy())

from gui import Gui
import tkinter as tk

if (__name__ == "__main__"):
    root = tk.Tk()
    root.title("Essembling SVM and MLP Using Bootstrap Aggregation")
    app = Gui(master=root)
    app.mainloop()
