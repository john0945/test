from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from functools import partial
from mininet.node import Host

class backup(Topo):

    def build(self):
        s = {}
        h = {}
        for sw in range(7):
            s[sw+1] = self.addSwitch('s%s' % (sw + 1))


        h1 = self.addHost('h%s' % (1))
        self.addLink(h1, s[1])

        h2 = self.addHost('h%s' % (2))
        self.addLink(h2, s[6])

        self.addLink(s[1], s[2])
        self.addLink(s[1], s[3])

        self.addLink(s[7], s[3])

        self.addLink(s[2], s[3])

        self.addLink(s[1], s[4])
        self.addLink(s[4], s[5])
        self.addLink(s[6], s[5])
        self.addLink(s[6], s[7])



class IpHost(Host):
    def __init__(self, name, *args, **kwargs):
        super(IpHost, self).__init__(name, *args, **kwargs)
        #self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self, **kwargs)
   #     mtu = "ifconfig "+self.name+"-eth0 mtu 1490"
   #     self.cmd(mtu)
  #      self.cmd('ip route add default via %s' % self.gateway)


def backup_run():
    "Create and test a simple network"
    topo = backup()
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    net = Mininet(topo=topo, switch=switch, controller=None)
    net.addController('c0', controller=RemoteController, ip="172.31.21.103", port=6633)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    backup_run()
