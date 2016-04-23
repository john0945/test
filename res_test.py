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

file_name = "1"

def startup(topo):
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip="192.168.56.102", port=6633)
    net.start()
    print ("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print ("Testing network connectivity")
    net.pingAll()
    return net

def testing(net, filename, host1, host2, switch1, switch2):
    h1 = net.get(host1)
    h2 = net.get(host2)
    s1 = net.get(switch1)
    s2 = net.get(switch2)

    h1.cmd("ping -i 0.01 {} &".format(h2.IP()))
    h2.cmd("tcpdump -XX -n -i {}-eth0 -w {}.pcap  &".format(host2, filename))
    sleep(2)
    #os.system("link {} {} down ".format(s1, s2))
    net.configLinkStatus( switch1, switch2, 'down' )
    sleep(2)

    h1.cmd("kill %ping")
    h2.cmd("kill %tcpdump")
    h2.cmd("tcpdump -tttttnr {}.pcap src host {} > {}.txt".format(filename, h1.IP(), filename))

def simple_test(file_name):

    host1 = "h1"
    host2 = "h2"
    switch1 = "s1"
    switch2 = "s2"
    filename = "simple"+file_name
    net = startup(simple())

    testing(net, filename, host1, host2, switch1, switch2)
    net.stop()


def ring_test(file_name):

    host1 = "h1"
    host2 = "h2"
    switch1 = "s1"
    switch2 = "s2"
    filename = "ring"+file_name

    net = startup(ring())
    testing(net, filename, host1, host2, switch1, switch2)
    net.stop()


def usnet_test(file_name):

    host1 = "l_h1"
    host2 = "r_h5"
    switch1 = "s41"
    switch2 = "s42"
    filename = "usnet"+file_namegit

    net = startup(USNET())
    testing(net, filename, host1, host2, switch1, switch2)
    net.stop()




if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simple_test("1")
    ring_test("1")
    usnet_test("1")

    simple_test("2")
    ring_test("2")
    usnet_test("2")

    simple_test("3")
    ring_test("3")
    usnet_test("3")