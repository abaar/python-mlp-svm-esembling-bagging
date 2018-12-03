import numpy
import pandas
import random
import math
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
class bagging:
	def __init__(self):
		self.__svm = []
		self.__predict_result_each_bag = []
		self.__mlp = []
		self.__svm_size = None
		self.__mlp_size = None
		self.__svm_part = None
		self.__mlp_part = None
		self.__method = None
		self.__training_data = None
		self.__x_train_bags = []
		self.__y_train_bags = []
		self.__dataset = None
		self.__x_train_original= None
		self.__y_train_original = None
		self.__x_test_original = None
		self.__y_test_original = None
		self.__state = None
		self.__accuray = None
		self.__average_of_all_predicts=[]
		self.__intended_output=None
		self.__svm_only=None
		self.__mlp_only=None


	def reset(self):
		print("Reset")

	def read_dataset(self,dataset="iris"):
		try:
			self.__dataset=pandas.read_csv(dataset)
			self.__dataset=numpy.array(self.__dataset)
			return True
		except:
			return False
		# print(self.__dataset)

	def create_bag(self,amount=10,test_size=0.33,bag_size=0.9):
		# print(self.__dataset)
		# try:
		x=self.__dataset[:,:-1] #take all datas from 
		y=self.__dataset[:,-1] #take all the intended output
		self.__intended_output=list(set(y))
		self.__x_train_original,self.__x_test_original,\
		self.__y_train_original, self.__y_test_original \
		=train_test_split(x,y,test_size=test_size,random_state=1)
			#split dataset
		b_size=math.ceil(len(self.__x_train_original)*bag_size)
			#making bags
		for x in range(0,amount):
			self.__x_train_bags.append([])
			self.__y_train_bags.append([])
			holder=[]
			for y in range(0,b_size):
					#random idx from 0 to xtrain - 1 (0-based index)
				idx=random.randint(0,len(self.__x_train_original)-1) #inclusive
				self.__x_train_bags[x].append(self.__x_train_original[idx])
				self.__y_train_bags[x].append(self.__y_train_original[idx])
		self.__state="data_created"
			# print(self.dataset)
		return True
		# except:
		# 	return False

	def create_model(self, svm_models ,mlp_models):
		for i in range(0,svm_models):
			self.__svm.append(SVC(kernel='linear'))
		for i in range(0,mlp_models):
			self.__mlp.append(MLPClassifier(hidden_layer_sizes=(13,13,13), max_iter=500))

		self.__state="model_added"

	def get_len_of_svm_model(self):
		return len(self.__svm_part)

	def get_len_of_mlp_model(self):
		return len(self.__mlp_part)

	def train_svm_data(self,idx):
		if(idx>len(self.__svm_part)):
			return False
		bag_idx=self.__svm_part[idx]
		self.__svm[idx].fit(self.__x_train_bags[bag_idx],self.__y_train_bags[bag_idx])
		return True

	def train_mlp_data(self,idx):
		if(idx>len(self.__mlp_part)):
			return False
		bag_idx=self.__mlp_part[idx]
		self.__mlp[idx].fit(self.__x_train_bags[bag_idx],self.__y_train_bags[bag_idx])
		return True

	def train_data(self, svm_models=None, mlp_models=None,log=None):
		if(svm_models==None and mlp_models==None):
			svm_models=len(self.__x_train_bags)*0.6
			svm_models=math.ceil(svm_models)
			mlp_models=len(self.__x_train_bags)-svm_models
		elif(mlp_models==None):
			if(svm_models==len(self.__x_train_bags)):
				mlp_models=0
			else:
				mlp_models=len(self.__x_train_bags)-svm_models
		elif(svm_models==None):
			if(mlp_models==len(self.__x_train_bags)):
				svm_models=0
			else:
				svm_models=len(self.__x_train_bags)-mlp_models


		self.create_model(svm_models,mlp_models)

		svm_part = []
		mlp_part = []
		svm_part_checked = False
		svm_using_bag_idx=[False]*(len(self.__x_train_bags))
		for i in range(0,svm_models):
			random_bag = random.randint(0,len(self.__x_train_bags)-1) 
				#prevent out of index since it return inclusive number
			while(svm_using_bag_idx[random_bag]):
				random_bag = random.randint(0,len(self.__x_train_bags)-1)
			svm_part.append(random_bag)
			svm_using_bag_idx[random_bag]=True

		for i in range(0,len(self.__x_train_bags)):
			if(not svm_using_bag_idx[i]):
				mlp_part.append(i)
		
		for i in range(0,svm_models):
			get_svm_idx = svm_part[i]
			# print("svm train ke",i)
			if not (log is None):
				log("Training "+str(i+1)+"th SVM")
			self.__svm[i].fit(self.__x_train_bags[get_svm_idx],\
				self.__y_train_bags[get_svm_idx])

		for i in range(0,mlp_models):
			get_mlp_idx = mlp_part[i]
			# print("mlp train ke",i)
			if not (log is None):
				log("Training "+str(i+1)+"th MLP")
			self.__mlp[i].fit(self.__x_train_bags[get_mlp_idx],\
				self.__y_train_bags[get_mlp_idx])

		self.__svm_part = svm_part
		self.__mlp_part = mlp_part
		return True

	def test_model(self):
		for i in range(0,len(self.__svm_part)):
			get_svm_idx = self.__svm_part[i]
			y_predic = self.__svm[i].predict(self.__x_test_original)
			self.__predict_result_each_bag.append(y_predic)
			y_predic = None

		for i in range(0,len(self.__mlp_part)):
			get_mlp_idx = self.__mlp_part[i]
			y_predic = self.__mlp[i].predict(self.__x_test_original)
			self.__predict_result_each_bag.append(y_predic)
			y_predic = None

	def calculate_model_average(self):
		result_holder=[]
		counter_holder=dict()
		for i in range(0,len(self.__predict_result_each_bag[0])):
			counter_holder.clear()
			for j in range(0,len(self.__predict_result_each_bag)):
				count=counter_holder.get(self.__predict_result_each_bag[j][i],0)
				count+=1
				counter_holder.update({self.__predict_result_each_bag[j][i]:count})
			ma=-1
			result=None
			for k in range(0,len(self.__intended_output)):
				count_result = counter_holder.get(self.__intended_output[k],0)
				if(count_result>ma):
					ma=count_result
					result=self.__intended_output[k]
			result_holder.append(result)
		self.__average_of_all_predicts=numpy.array(result_holder)


	def getAccuracy(self):
		# score=0
		# add=0
		# for i in range(0,len(self.__predict_result_each_bag)):
		# 	print(self.__predict_result_each_bag[i])
		# 	score = metrics.accuracy_score(self.__predict_result_each_bag[i],self.__y_test_original)
		# 	add = add + score
		# add = add / len(self.__predict_result_each_bag)
		# print("++++++")
		# print(self.__y_test_original)
		# return add
		# print(self.__average_of_all_predicts)
		# print(self.__y_test_original)
		return (metrics.accuracy_score(self.__average_of_all_predicts,self.__y_test_original))


	def getSvmOnly(self):
		self.__svm_only=SVC(kernel='linear')
		self.__svm_only.fit(self.__x_train_original,self.__y_train_original)
		predict=self.__svm_only.predict(self.__x_test_original)
		return metrics.accuracy_score(predict,self.__y_test_original)


	def getMlpOnly(self):
		self.__mlp_only=MLPClassifier(hidden_layer_sizes=(13,13,13), max_iter=500)
		self.__mlp_only.fit(self.__x_train_original,self.__y_train_original)
		predict=self.__mlp_only.predict(self.__x_test_original)
		return metrics.accuracy_score(predict,self.__y_test_original)
