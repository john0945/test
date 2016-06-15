#!/usr/bin/python

import os
import re
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, UserSwitch, Host, Switch
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI

class LeafSpine(Topo):
    def __init__(self):
        "Create Leaf and Spine Topo."
        Topo.__init__(self)

        s1 = self.addSwitch('s1') #leaf
        s2 = self.addSwitch('s2') #leaf
        s3 = self.addSwitch('s3') #spine
        s4 = self.addSwitch('s4') #spine
        s5 = self.addSwitch('s5') #spine
        s6 = self.addSwitch('s6') #spine

        h1 = self.addHost('h1', cls=IpHost, ip='10.0.1.1/24', gateway='10.0.1.254') #connect to S1
        h2 = self.addHost('h2', cls=IpHost, ip='10.0.2.1/24', gateway='10.0.2.254') #connect to S2
        h4 = self.addHost('h3', cls=IpHost, ip='10.0.2.2/24', gateway='10.0.2.254') #connect to S2
        h3 = self.addHost('h4', cls=IpHost, ip='10.0.2.3/24', gateway='10.0.2.254') #connect to S2

        self.addLink(s1,s2)
        self.addLink(s1,s3)
        self.addLink(s1,s4)
        self.addLink(s2,s5)
        self.addLink(s2,s6)
        self.addLink(s3,s4)
        self.addLink(s3,s5)
        self.addLink(s4,s6)
        self.addLink(s5,s6)


        self.addLink(h1,s1)
        self.addLink(h2,s2)
        self.addLink(h3,s2)
        self.addLink(h4,s2)

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name, *args, **kwargs)
        self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self, **kwargs)
        mtu = "ifconfig "+self.name+"-eth0 mtu 1490"
        self.cmd(mtu)
        self.cmd('ip route add default via %s' % self.gateway)


def init():
    controllers = ['127.0.0.1']
    topo = LeafSpine()
    net = Mininet(topo=topo, link=TCLink, build=False,
                  switch=UserSwitch,
                  controller = None,
                  autoSetMacs = True)
    for i in range(len(controllers)):
        net.addController("c%s" % i , controller=RemoteController, ip=controllers[i])

    net.build()
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    init()
    os.system('sudo mn -c')