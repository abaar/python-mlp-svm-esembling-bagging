# from bagging import bagging

# bagging.read_dataset("transfusion.csv")

# bagging.create_bag()

# bagging.train_data()

# bagging.test_model()

# bagging.calculate_average_model()

# print(bagging.getAccuray()

import threading

def hoa2():
	for i in range(0,100):
		print(str(i),"doa")


def hoa():
	for i in range(0,100):
		print(i)

t1 = threading.Thread(target=hoa)
# t1.start()

t2 = threading.Thread(target=hoa2)
# t2.start()

for i in range(0,100):
	print("Count",str(threading.activeCount()))