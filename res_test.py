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
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip="192.168.56.102", port=6633)
    net.start()
    print ("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print ("Testing network connectivity")
    net.pingAll()
    return net

def testing(net, time, host1, host2, switch1, switch2, network):
    h1 = net.get(host1)
    h2 = net.get(host2)

    h1.cmd("ping -i 0.01 {} &".format(h2.IP()))
    h2.cmd("tcpdump -XX -n -i {}-eth0 -w pcaps/{}-{}.pcap  &".format(host2, network, filename))
    sleep(2)
    net.configLinkStatus( switch1, switch2, 'down' )
    sleep(2)
    net.configLinkStatus( switch1, switch2, 'up' )
    h1.cmd("kill %ping")
    h2.cmd("kill %tcpdump")
    h2.cmd("tcpdump -tttttnr pcaps/{n}-{t}.pcap src host {ip} > results/{}-{}.txt".format(n=network, t=time, ip = h1.IP()))

    append_results(time, network)


def simple_test(file_name):

    network = simple
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

    for s in range(3):
        simple_test("{}".format(ctime()))
        ring_test("{}".format(ctime()))
        usnet_test("{}".format(ctime()))

