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
        for sw in range(4):
            s[sw+1] = self.addSwitch('s%s' % (sw + 1))


        for host in range(4):
            # h = self.addHost('h%s' % (host + 1),
            #                              cls=IpHost,
            #                              ip='10.0.%s.1/24' % ((host + 1)))
            #                            #  gateway='10.0.%s.254' % (host + 1))
            h = self.addHost('h%s' % (host + 1))
            # h.setIp(intf = 'h%s' % (host + 1),
            #         ip= "10.0.%s.1"% (host + 1),
            #         prefixLen = 8)

            self.addLink(h, s[host+1])

        self.addLink(s[1], s[2])
        self.addLink(s[2], s[3])
        self.addLink(s[3], s[4])
        self.addLink(s[4], s[1])



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
    net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)
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
