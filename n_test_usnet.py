from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from functools import partial

from time import sleep

class USNET(Topo):

#this should be in master
    def col(self, col, n):
        col_switch = {}
        for s in range(n):
            col_switch[s + 1] = self.addSwitch('s%s%s' % (col, s + 1))
            # self.switches.append("s" + str(col)+ str(s + 1))
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
            l = self.addLink(s[l[0]][l[1]], s[l[2]][l[3]])
            #print(l)

def enable_bfd(net):
    links = net.links

    for link in links:
        node1 = link.intf1.node
        node2 = link.intf2.node

        intf_name = link.intf1.name
        intf_name2 = link.intf2.name

        if intf_name[0] =='s' and intf_name2[0] == 's':
            node1.cmd("ovs-vsctl set interface {} bfd:enable=true ".format(intf_name))
            node2.cmd("ovs-vsctl set interface {} bfd:enable=true ".format(intf_name2))


def test(net):
    switches = net.switches

    for switch in switches:
        print (switch.name)

        if switch.name[1] == '1' or switch.name[1] == '7':
            print ('skip')

        else:
            for k, v in switch.ports.items():
                if k.name[0] == 's':
                    switch.cmd("ifconfig {} down &".format(k))

            print (switch.name)
            sleep(0.5)
            net.pingAll()

            for k, v in switch.ports.items():
                if k.name[0] == 's':
                    switch.cmd("ifconfig {} up &".format(k))

            sleep(0.5)


def usnet_run():
    "Create and test a simple network"
    topo = USNET()
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    net = Mininet(topo=topo, switch=switch, controller=None)
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)
    net.start()
    enable_bfd(net)
    print "bfd enabled"
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    CLI(net)
    print "Testing network connectivity"
    test(net)
    CLI(net)

    # print(self.switches)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    usnet_run()
