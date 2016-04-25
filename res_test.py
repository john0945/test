from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from usnet import USNET
from simple import simple
from ring import ring
from time import sleep
import os
from time import ctime
from failure_param import append_results


def startup(topo):
    net = Mininet(topo=topo)
    # net.addController('c0', controller=RemoteController, ip="192.168.56.102", port=6633)
    net.start()
    CLI(net)
    print ("Testing network connectivity")
    net.pingAll()
    return net


def testing(net, time, host1, host2, switch1, switch2, network):

    h1 = net.get(host1)
    h2 = net.get(host2)

    h1.cmd("ping -i 0.01 {} &".format(h2.IP()))
    # print("tcpdump -XX -n -i {}-eth0 -w ./pcaps/\"{}-{}.pcap\"  &".format(host2, network, time))
    h2.cmd("tcpdump -XX -n -i {}-eth0 -w './pcaps/{}-{}.pcap'  &".format(host2, network, time))

    # h1.cmd("tcpdump -XX -n -i {}-eth0 -w './host_pcaps/{}-{}.pcap'  &".format(host1, network, time))


    sleep(2)
    net.configLinkStatus( switch1, switch2, 'down' )
    sleep(2)
    h1.cmd("kill %ping")
    # h1.cmd("kill %tcpdump")
    h2.cmd("kill %tcpdump")
    net.configLinkStatus( switch1, switch2, 'up' )


    # print("tcpdump -tttttnr ./pcaps/\"{n}-{t}.pcap\" src host {ip} > ./results/'{n}-{t}.txt'".format(n=network, t=time, ip = h1.IP()))
    h2.cmd("tcpdump -tttttnr './pcaps/{n}-{t}.pcap' src host {ip} > ./results/'{n}-{t}.txt'".format(n=network, t=time, ip = h1.IP()))

    # h1.cmd("tcpdump -tttttnr './host_pcaps/{n}-{t}.pcap' src host {ip} > ./host_results/'{n}-{t}.txt'".format(n=network, t=time, ip=h1.IP()))
    append_results(time, network)
    sleep(5)

def simple_test(filename):

    network = "simple"
    host1 = "h1"
    host2 = "h2"
    switch1 = "s1"
    switch2 = "s2"
    net = startup(simple())

    testing(net, filename, host1, host2, switch1, switch2, network)
    net.stop()


def ring_test(filename):

    network = "ring"
    host1 = "h1"
    host2 = "h2"
    switch1 = "s1"
    switch2 = "s2"

    net = startup(ring())
    testing(net, filename, host1, host2, switch1, switch2, network)
    net.stop()


def usnet_test(filename):

    network = "usnet"
    host1 = "l_h1"
    host2 = "r_h5"
    switch1 = "s41"
    switch2 = "s42"

    net = startup(USNET())
    testing(net, filename, host1, host2, switch1, switch2, network)
    net.stop()




if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    os.system("sudo mn -c")

    for s in range(3):
        simple_test("{}".format(ctime()))

    with open('log.txt', 'a') as log:
        log.write('\n')

    for s in range(3):
        ring_test("{}".format(ctime()))

    with open('log.txt', 'a') as log:
        log.write('\n')

    #for s in range(3):
   #     usnet_test("{}".format(ctime()))

    with open('log.txt', 'a') as log:
        log.write('\n-------------------------------------------------------------\n')

