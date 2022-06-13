import socket
import threading
import json
import time
f=1
server=socket.gethostbyname(socket.gethostname())
port=9013
addr=(server,port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(addr)
print(server+" binded to {}".format(port))
info=[{"id":1,"status":"Idle","loc":[330,410],"frame":1,"bullets":[],"bulletsb":[],"health":3},{"id":2,"status":"Idleb","loc":[440,410],"frame":1,"bullets":[],"bulletsb":[],"health":3}]
def start():
    print("[SERVER] Running..... at {}".format(server))
    s.listen(2)
    while True:
        conn,addr=s.accept()
        start.thread=threading.Thread(target=handle_client,args=(conn,addr))
        start.thread.start()
        print("Active Connections",threading.activeCount())

def handle_client(conn,addr):
    global f
    global info
    print("[NEW CONNECTION] {}".format(addr),end="\n")
    handle_client.connected=True
    while handle_client.connected:
         d=conn.recv(10000)
         if len(d.decode("utf-8")) >0:
                if d.decode("utf-8")=="start":
                    conn.send(str(f).encode())
                    f+=1
                elif d.decode("utf-8")=="need":
                    s=json.dumps(info).encode()
                    conn.send(s)
                else:
                    d=json.loads(d.decode("utf-8"))
                    info=d
                    
start()                    
         
