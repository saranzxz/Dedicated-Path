from scapy.all import *
import os
import threading

class prior(Packet):
    MAX_LEN = 1024
    name = 'prior'
    fields_desc = [
        BitField('priority', 0, 8)
    ]

flag = True
flag2 = True
def inter_send():
    global flag
    custom_packet = prior(priority = 1)
    file = '/home/ubuntu/interactions.json'
    f = open(file, 'rb')
    
    while True:
        inter_b = f.read(1000)
        
        if inter_b:
            inter_b = b'0' + inter_b
            # print(inter_b)
            sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw(load = inter_b), iface = 'enp7s0')
        else:
            break
            
    sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw('EOFi'), iface = 'enp7s0')
    flag = False
    f.close()
    
def vid_send():
    global flag2
    custom_packet = prior(priority = 1)
    path = '/home/ubuntu/data/media/BigBuckBunny/4sec/bunny_217761bps/'
    files = list(map(lambda x: path + x, os.listdir(path)))
    files.remove('/home/ubuntu/data/media/BigBuckBunny/4sec/bunny_217761bps/BigBuckBunny_4s_init.mp4')
    files.remove('/home/ubuntu/data/media/BigBuckBunny/4sec/bunny_217761bps/BigBuckBunny_4snonSeg.mp4')
    files = sorted(files, key = lambda x: int(x.split('_4s')[1].split('.')[0]))
    files = files[: 20]
    files.insert(0, '/home/ubuntu/data/media/BigBuckBunny/4sec/bunny_217761bps/BigBuckBunny_4s_init.mp4')

    for file in files:
        if '.m4s' in file or 'init' in file:
            with open(file, 'rb') as f:
                while True:
                    vid_b = f.read(1000)

                    if vid_b:
                        vid_b = b'1' + vid_b
                        # print(vid_b)
                        p = Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw(load = vid_b)
                        sendp(p, iface = 'enp7s0')
                    else:
                        break

                sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw('EOFzxz'), iface = 'enp7s0')
                
    flag2 = False
                
def start():                
    custom_packet = prior(priority = 1)                
    threading.Thread(target = inter_send).start()
    vid_send()
    sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw('EOFv'), iface = 'enp7s0')

for j in range(20):
    custom_packet = prior(priority = 1)
    sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw('EOFnew'), iface = 'enp7s0')
    start()
    
    while flag or flag2:
        a = 1
        
    flag = True
    flag2 = True

sendp(Ether() / IP(dst = '192.168.1.10', proto = 0x92) / custom_packet / Raw('EOFend'), iface = 'enp7s0')