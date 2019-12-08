from face_recog import face_rec as fc
import os
registed_person_pics=os.listdir("faces")    #存放已经注册过的人脸文件夹
unknow_person="unknow_person/reba.jpg"                    #未知人脸所在位置
#计算所有已注册过的人脸特征，并保存在data文件夹中

face_rec = fc.face_recognition()
compare_flag=False
compute_all_rec_per_feature_flag=False
if compute_all_rec_per_feature_flag:
    for index, pic in enumerate(registed_person_pics):
        face_rec.inputPerson(name=pic.split('.')[0], img_path=os.path.join("faces",pic))
        vector = face_rec.create128DVectorSpace()  # 提取128维向量
        person_data1 = fc.savePersonData(face_rec, vector )   # 将提取出的数据保存到data文件夹，为便于操作返回numpy数组

person_feature=os.listdir("data/")

#人脸对比
compare_result=fc.oneN_compare(unknow_person,person_feature)#1:N对比找出最小的欧式距离
print("-------------------------------------------")
print("compare result : {}".format(compare_result))