from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."

    def build(self):
        switch = {}
        host = {}
        for s in range(3):
            switch[s+1] = self.addSwitch('s%s' % (s + 1))

        for h in range(2):
            host[h+1] = self.addHost('h%s' % (h + 1))

        self.addLink(host[1], switch[1])
        self.addLink(host[2], switch[2])
        self.addLink(switch[1], switch[2])
        self.addLink(switch[1], switch[3])
        self.addLink(switch[3], switch[2])


def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo()
    net = Mininet(topo=topo, controller=None)
    net.addController('c0', controller=RemoteController, ip="192.168.56.102", port=6633)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()