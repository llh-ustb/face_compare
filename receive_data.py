import socket
import struct

def main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('0.0.0.0',8888))
    print('listening....')
    sock.listen(5)
    conn, addr = sock.accept()
    op=open("a.jpg","wb")
    while True:
        data = conn.recv(4)
        if data=='':
            continue
        unpacked_data=struct.unpack('<i',data)
        if unpacked_data==(0xabcd,):
            print("receive head")
            d=conn.recv(4)
            if struct.unpack('<i',d)==(1,):
                continue
            if struct.unpack('<i',d)==(2,):
                print("start receiving pics")
                while True:
                    pics_data = conn.recv(1024*2)
                    if len(pics_data) == 0:
                        break
                    op.write(pics_data)
                op.close()
                print("receive finished")
                break
    conn.close()


if __name__ =="__main__":
    main()

