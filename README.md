# Dedicated Network Pathing For Specific Data Packets

## NOTE: The resource3.ipynb can be downloaded and executed to recreate the slice and experimental setup.
### Ideally after the notebook is executed, on inspecting the client, you should be able to see a newly generated results.csv in the client with all metrics recorded. It can be further consolidated using anlyz.py.

### Some details regarding the code
- anlyz.py
    - This is a helper file to analyse the results gathered in results.csv after transfer of data is complete.
- recv.py
    - The client runs this script to sniff incoming packets from the server. In our case, video and metadata.
- resources3.ipynb
    - Notebook used to create and setup the slice.
- route.p4
    - This is the p4 program running in switch 1, which does the priority specific routing.
- rules1.sh
    - Forwarding table for switch 1.
- rules2.sh
    - Forwarding table for switch 2.
- rules3.sh
    - Forwarding table for switch 3.
- send.py
    - The server runs this script when it is ready to send data to the client.
- simple.p4
    - Switch 2 and switch 3 use this program to route packets to the client. There are not priority specific routing logic since they are intended to simply forward traffic.

On a high level, packets are crafted using scapy as follows at the server,\n
<code>Ether() / IP(dst = IP of client, proto = 0x92) / Priority(Priority = 1 or 0) / Raw(load = video/metadata)</code>
