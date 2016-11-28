from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from functools import partial

class lattice(Topo):

#this should be in master
    def col(self, col, n):
        col_switch = {}
        for s in range(n):
            col_switch[s] = self.addSwitch('s1%s%s' % (col, s))
            if s > 0:
                self.addLink(col_switch[s], col_switch[s - 1])

        return col_switch

    def build(self):
        s = {}
        n = 10
        for c in range(n):
            s[c] = self.col(c,n)

        for c in range(9):
            for r in range(10):
                self.addLink(s[c][r], s[c+1][r])

def usnet_run():
    "Create and test a simple network"
    topo = lattice()
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    net = Mininet(topo=topo, switch=switch, controller=None)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
#    net.pingAll()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    usnet_run()
