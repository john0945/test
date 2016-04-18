from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController




class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."



    def col(self, col, n):
        col_switch = {}
        for s in range(n):
            col_switch[s + 1] = self.addSwitch('s%s%s' % (col, s + 1))
            if s > 0:
                self.addLink(col_switch[s], col_switch[s + 1])

        return col_switch


    def build(self):
        s = {}
        l_host = {}
        r_host = {}

        connections = [
            [1, 1, 3, 1],

            [1, 2, 3, 1],
            [1, 3, 2, 1],
            [1, 3, 3, 2],
            [1, 4, 2, 1],
            [1, 4, 3, 3],
            [2, 1, 3, 2],

            [3, 1, 4, 1],
            [3, 1, 5, 1],
            [3, 2, 4, 1],
            [3, 3, 4, 2],

            [4, 1, 5, 1],
            [4, 1, 5, 2],
            [4, 2, 5, 3],
            [4, 2, 5, 4],

            [5, 1, 6, 1],
            [5, 1, 7, 1],
            [5, 2, 6, 2],
            [5, 3, 6, 3],
            [5, 4, 6, 4],

            [6, 1, 7, 2],
            [6, 2, 7, 3],
            [6, 2, 7, 4],
            [6, 3, 7, 4],
            [6, 3, 7, 5],
            [6, 4, 7, 6]]


        #
        # connections = {
        #     [1, 1]: [3, 1],
        #     [1, 2]: [3. 1],
        #     [1, 3]: [2, 1],
        #     [1, 3]: [3, 2],
        #     [1, 4]: [2, 1],
        #     [1, 4]: [3, 3],
        #
        #     [2, 1]: [3, 2],
        #
        #     [3, 1]: [4, 1],
        #     [3, 1]: [5, 1],
        #     [3, 2]: [4, 1],
        #     [3, 3]: [4, 2],
        #
        #     [4, 1]: [5, 1],
        #     [4, 1]: [5, 2],
        #     [4, 2]: [5, 1],
        #     [4, 2]: [5, 2],
        #
        #     [5, 1]: [6, 1],
        #     [5, 1]: [7, 1],
        #     [5, 2]: [6, 2],
        #     [5, 3]: [6, 3],
        #     [5, 4]: [6, 4],
        #
        #     [6, 1]: [7, 2],
        #     [6, 2]: [7, 3],
        #     [6, 2]: [7, 4],
        #     [6, 3]: [7, 4],
        #     [6, 3]: [7, 5],
        #     [6, 4]: [7, 6]
        #
        # }

        s[1] = self.col(1,4)
        s[2] = self.col(2,1)
        s[3] = self.col(3,3)
        s[4] = self.col(4,2)
        s[5] = self.col(5,4)
        s[6] = self.col(6,4)
        s[7] = self.col(7,6)

        for h in range(4):
            l_host[h+1] = self.addHost('l_h%s' % (h + 1))
            self.addLink(s[1][h+1], l_host[h+1])

        for h in range(5):
            r_host[h+1] = self.addHost('r_h%s' % (h + 1))
            if h<3:
                self.addLink(s[7][h + 1], r_host[h + 1])
            else:
                self.addLink(s[7][h + 2], r_host[h + 1])

        for l in connections:
            self.addLink(s[l[0]][l[1]], s[l[2]][l[3]])





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