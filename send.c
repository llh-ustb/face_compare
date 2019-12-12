#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>
#define MAXLINE 4096
unsigned int conn_flag = 1;
unsigned int run_flag=1;
unsigned int send_success_flag=1;
unsigned int send_flag=1;
void print_usage(char *proc) {
    printf("usage: %s <ip> <port> \n", proc);
}


int main(int argc, char *argv[]) {
    int sockfd;
    struct sockaddr_in their_addr;
    int head = 0xabcd;
    int cmd;
    int pic_hw[2] = {200, 200};
    char buffer[1024*2];
    unsigned int  byte_count;

    FILE *fp;
    if (argc < 3) {
        print_usage(argv[0]);
        return 2;
    }
    printf("Waitting for connect...\n");
    while(run_flag) {
        if (conn_flag) {

            while ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
                printf("Get the sockfd error\n");
                sleep(1);
            }

            their_addr.sin_family = AF_INET;
            their_addr.sin_port = htons(atol(argv[2]));
            their_addr.sin_addr.s_addr = inet_addr(argv[1]);
            bzero(&(their_addr.sin_zero), 8);

            while (connect(sockfd, (struct sockaddr *) &their_addr, sizeof(struct sockaddr)) == -1) {
                printf("Connect to server error\n");
                sleep(1);
            }

            conn_flag = 0;
            printf("Get the Server\n");
            cmd = 1;
            send(sockfd, &head, sizeof(head), 0);
            send(sockfd, &cmd, sizeof(cmd), 0);
            cmd = 2;
            sleep(1);
        }
        else {
            if(send_flag){

                fp=fopen("/data/send_pics/1.jpg","rb");
                send(sockfd, &head, sizeof(head), MSG_NOSIGNAL);
                send(sockfd, &cmd, sizeof(cmd), MSG_NOSIGNAL);
                while(1){
                    byte_count=fread(buffer,1,2048,fp);
                    if(byte_count==0){
                        fclose(fp);
                        break;
                        //exit(0);
                    }
                    send_success_flag=send(sockfd,buffer,byte_count,0);
                    if(send_success_flag==-1){
                        printf("Send error \n");
                        printf("Reconnecting...\n");
                        conn_flag = 1;
                    }
                }
                printf("send succ\n");
                send_flag=0;
            }
            if(send_flag==0){
                printf("waitting send...\n");
                sleep(1);
            }

        }

    }
}
