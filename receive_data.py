# -*- coding:utf-8 -*-
import struct
from socketserver import TCPServer, StreamRequestHandler, ThreadingTCPServer
import logging
import time
import argparse
from face_recog import face_rec as fc
import os
import shutil


logger = logging.getLogger()
face_rec = fc.face_recognition()

def compute_all_rec_per_feature(registed_person_pics_dir):      #faces
    registed_person_pics = os.listdir(registed_person_pics_dir)  # 存放已经注册过的人脸文件夹
    for index, pic in enumerate(registed_person_pics):
        face_rec.inputPerson(name=pic.split('.')[0], img_path=os.path.join("faces",pic))
        vector = face_rec.create128DVectorSpace()  # 提取128维向量
        person_data1 = fc.savePersonData(face_rec, vector )   # 将提取出的数据保存到data文件夹，为便于操作返回numpy数组

class MsgHandler(StreamRequestHandler):
    def handle(self):
        logger.info('gate connection success! %s', self.request)
        while True:
            data = self.request.recv(4)
            if data == '':
                continue
                time.sleep(0.1)
            try:
                unpacked_data = struct.unpack('<i', data)
                if unpacked_data == (0xabcd,):
                    print("receive head")
                    d = self.request.recv(4)
                    if struct.unpack('<i', d) == (1,):
                        continue
                    if struct.unpack('<i', d) == (2,):
                        print("start receiving pics")
                        pic=str(int(time.time())) + ".jpg"
                        op = open(os.path.join("unknow_person",pic) , "wb")
                        count=0
                        while True:
                            count = count+1
                            pics_data = self.request.recv(1024 * 2)
                            #print(len(pics_data))
                            if b"\xee\xee\xee\xee" in pics_data:
                                #op.write(pics_data)
                                break
                            op.write(pics_data)
                        op.close()
                        print("receive finished")
            except:
                logger.info("data unmeet format")

            if(os.listdir("unknow_person")!=[]):
                unknow_person = os.path.join("unknow_person", pic)
                person_feature = os.listdir("data/")
                # 人脸对比
                compare_result = fc.oneN_compare(unknow_person, person_feature)  # 1:N对比找出最小的欧式距离
                #self.request.sendall(compare_result)
                print("-------------------------------------------")
                print("compare result : {}".format(compare_result))
                shutil.move(unknow_person, "haveBeenProcessed")



def main():

    arg=argparse.ArgumentParser()
    arg.add_argument("-ip",default="0.0.0.0",type=str)
    arg.add_argument("-port",default=7001,type=int)
    a=arg.parse_args()

    server = ThreadingTCPServer((a.ip, a.port), MsgHandler)
    print('listening....')
    server.serve_forever()

    compute_all_rec_per_feature("faces")
    while True:
        if(len(os.listdir("data"))!=len(os.listdir("faces"))):   #已经注册过的人脸数量和特征的数量不等，代表有新人加进来
            compute_all_rec_per_feature("faces")
        else:
            time.sleep(0.1)

if __name__ =="__main__":
    main()

