# -*- coding: utf-8 -*-
import dlib
import cv2
import numpy as np

def comparePersonData(data1, data2):
	diff = 0
	# for v1, v2 in data1, data2:
		# diff += (v1 - v2)**2
	for i in range(len(data1)):
		diff += (data1[i] - data2[i])**2

	diff = np.sqrt(diff)
	print(diff)
	if(diff < 0.6):
		print("It's the same person")
	else:
		print("It's not the same person")
	
def savePersonData(face_rec_class, face_descriptor):
	if face_rec_class.name == None or face_descriptor == None:
		return
	filePath = face_rec_class.dataPath + face_rec_class.name + '.npy'
	vectors = np.array([])
	for i, num in enumerate(face_descriptor):
		vectors = np.append(vectors, num)
		# print(num)
	print('Saving files to :'+filePath)
	np.save(filePath, vectors)
	return vectors
	
def loadPersonData(face_rec_class, personName):
	if personName == None:
		return
	filePath = face_rec_class.dataPath + personName + '.npy'
	vectors = np.load(filePath)
	print(vectors)
	return vectors

def oneN_compare(unknow_pic, registed_pics_feature):
	distance_list=[]
	if unknow_pic == None:
		print('No file!\n')
		return

	img_bgr = cv2.imread(unknow_pic)
	b, g, r = cv2.split(img_bgr)
	img_rgb = cv2.merge([r, g, b])

	detector = dlib.get_frontal_face_detector()
	shape_predictor = dlib.shape_predictor("model/shape_predictor_68_face_landmarks.dat")
	face_rec_model = dlib.face_recognition_model_v1("model/dlib_face_recognition_resnet_model_v1.dat")

	unkonw_person_dets = detector(img_rgb, 1)
	if len(unkonw_person_dets)==0 :
		print("no person detected!")
		return
	shape = shape_predictor(img_rgb, unkonw_person_dets[0])
	unkonw_face_descriptor = face_rec_model.compute_face_descriptor(img_rgb, shape)
	for f in registed_pics_feature:
		feature=np.load("data/"+f)
		distance_list.append(np.linalg.norm(unkonw_face_descriptor - feature))

	print()
	print(distance_list)
	if min(distance_list)>0.5:
		return "unknow person"
	else:
		return registed_pics_feature[np.argmin(distance_list)].split(".")[0]

class face_recognition():
	def __init__(self):
		self.predictor_path =  "model/shape_predictor_68_face_landmarks.dat"
		self.face_rec_model_path =  "model/dlib_face_recognition_resnet_model_v1.dat"
		self.faces_folder_path = "faces/"
		self.dataPath = "data/"
		self.detector = dlib.get_frontal_face_detector()
		self.shape_predictor = dlib.shape_predictor(self.predictor_path)
		self.face_rec_model = dlib.face_recognition_model_v1(self.face_rec_model_path)
		
		self.name = None
		self.img_bgr = None
		self.img_rgb = None
		self.detector = dlib.get_frontal_face_detector()
		self.shape_predictor = dlib.shape_predictor(self.predictor_path)
		self.face_rec_model = dlib.face_recognition_model_v1(self.face_rec_model_path)
		
	def inputPerson(self, name='people', img_path=None):
		if img_path == None:
			print('No file!\n')
			return 

		# img_name += self.faces_folder_path + img_name
		self.name = name
		self.img_bgr = cv2.imread(img_path)

		b, g, r = cv2.split(self.img_bgr)
		self.img_rgb = cv2.merge([r, g, b])
		
	def create128DVectorSpace(self):
		dets = self.detector(self.img_rgb, 1)
		print("Number of faces detected: {}".format(len(dets)))
		for index, face in enumerate(dets):
			print()
			print('face {}; left {}; top {}; right {}; bottom {}'.format(index, face.left(), face.top(), face.right(), face.bottom()))
		
			shape = self.shape_predictor(self.img_rgb, face)
			face_descriptor = self.face_rec_model.compute_face_descriptor(self.img_rgb, shape)

			return face_descriptor





	
		

		