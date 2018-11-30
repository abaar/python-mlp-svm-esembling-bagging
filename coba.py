from bagging import bagging

bagging.read_dataset("transfusion.csv")

bagging.create_bag()

bagging.train_data()

bagging.test_model()

bagging.calculate_average_model()

print(bagging.getAccuray()