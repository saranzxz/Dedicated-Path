from scapy.all import *
import time
import threading
import re
import os
import sys


class prior(Packet):
    MAX_LEN = 1024
    name = 'prior'
    fields_desc = [
        BitField('priority', 0, 8)
    ]
    
vid_b = b''
i = 0
f = open('test.mp4', 'ab')
fi = open('interactions.json', 'ab')
out = open('results.csv', 'a')
start1 = None
start2 = None
end1 = None
end2 = None
sv = 0
si = 0
    
def init():
    global vid_b, i, f, fi, out, start1, start2, end1, end2, sv, si
    os.system('rm interactions.json *.mp4 *.m4s -f')
    vid_b = b''
    i = 0
    f = open('test.mp4', 'ab')
    fi = open('interactions.json', 'ab')
    out = open('results.csv', 'a')
    start1 = None
    start2 = None
    end1 = None
    end2 = None
    sv = 0
    si = 0

def inter_packet_handler(packet):
    global fi, start2, si, end2
    
    vid_b = bytes(packet[Raw])

    if not start2:
        start2 = time.time()

    if b'EOFi' in vid_b:
        end2 = time.time() - start2
        print(f'Time taken for interactions: {end2} seconds (working)')
        # print(f'Average data rate for interactions: {si / end2} bytes/s')
        return
    if vid_b[0] == 48:
        vid_b = vid_b[1: ]
        si += len(vid_b)
        fi.write(vid_b)    

def inter_handler():
    sniff(filter = "ip and host 192.168.2.10", prn = inter_packet_handler, iface = ['enp9s0'])

def packet_handler(packet):
    global i, f, fi, start1, start2, si, sv, end1, end2, out
    # print(packet.summary())
    # print(packet.show())
    # print(packet.getlayer(Raw))

    # USE TIME.TIME TO EVALUATE PERFORMANCE
    vid_b = bytes(packet[Raw])
    bb = 0
    if vid_b[0] == 49 or vid_b[0] == 69:
        if vid_b[0] == 49:
            bb = 1
            vid_b = vid_b[1: ]


        if b'EOFend' in vid_b:
            out.write(f'{end1},{end2},{sv / end1},{si / end2}\n')
            f.close()
            fi.close()
            out.close()
            return

        if b'EOFnew' in vid_b:
            if start1:
                out.write(f'{end1},{end2},{sv / end1},{si / end2}\n')

            init()
            return

        if not start1:
            start1 = time.time()

        if b'EOFv' in vid_b:
            end1 = time.time() - start1
            f.close()
            print(f'Time taken for video: {end1} seconds')
            print(f'Average data rate for video: {sv / end1} bytes/s')
            return

        if b'EOFi' in vid_b and not end2:
            # print(vid_b)
            end2 = time.time() - start2
            print(f'Time taken for interactions: {end2} seconds')
            print(f'Average data rate for interactions: {si / end2} bytes/s')
            fi.close()
            return

        if b'EOFzxz' in vid_b:
            hack = False
            f.close()
            i += 1
            f = open(f'test{i}.m4s', 'ab')
            return
        
        if bb:
            sv += len(vid_b)
            f.write(vid_b)
    elif not end2:
        # print(vid_b)
        vid_b = vid_b[1: ]
        
        if not start2:
            start2 = time.time()
        # print(start2)
        try:
            si += len(vid_b)
            fi.write(vid_b)
        except:
            pass
            # print(vid_b)

init()
out.write('Time (Video) s,Time (Interactions) s,Avg rate (Video) bytes/s, Avg rate (Interactions) bytes/s\n')
bind_layers(IP, prior, proto = 0x92)
threading.Thread(target = inter_handler).start()
received_packets = sniff(filter = "ip and host 192.168.2.10", prn = packet_handler, iface = ['enp8s0'])