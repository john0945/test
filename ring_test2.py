#!/usr/bin/python

import os
from optparse import OptionParser

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, UserSwitch, Host
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from time import ctime, sleep
from failure_param import append_results


# Parse command line options and dump results
def parseOptions():
    """Parse command line options"""
    parser = OptionParser()
    parser.add_option('--core', dest='core', type='int', default=2,
                      help='number of core switches, default=2')
    parser.add_option('--fanout', dest='fanout', type='int', default=2,
                      help='number of hosts per leaf switch, default=2')
    parser.add_option('--node1', dest='node1', type='string', default="edge1",
                      help='default=edge1')
    parser.add_option('--node2', dest='node2', type='string', default="core101",
                      help='default=core101')
    (options, args) = parser.parse_args()
    return options, args 


opts, args = parseOptions()


class LeafAndSpine(Topo):
    def __init__(self, core=1, fanout=2, node1="edge1", node2="core101", **opts):
        "Create Leaf and Spine Topo."

        Topo.__init__(self, **opts)

	# Set link speeds to 10Mb/s
        linkopts = dict(bw=10)

        # Add core switches
        branch1 = {}
        branch2 = {}
        branch3 = {}
        cores = {1:branch1, 2:branch2, 3:branch3}
        for c in range(core):
            branch1[c] = self.addSwitch('core10%s' % (c + 1), dpid="00000000010%s" % (c + 1))
            branch2[c] = self.addSwitch('core20%s' % (c + 1), dpid="00000000020%s" % (c + 1))
            branch3[c] = self.addSwitch('core30%s' % (c + 1), dpid="00000000030%s" % (c + 1))

        
        # Add edge switches
        edgeSwitch1 = self.addSwitch('edge1', dpid="000000000001")
        edgeSwitch2 = self.addSwitch('edge2', dpid="000000000002")

        # Add hosts under an edge, fanout hosts per edge switch 
        # Connecting the hosts first should mean they're always on port1+2 which simplifies the config file

        for f in range(fanout):
            host1 = self.addHost('h%s' % (f + 1), cls=IpHost, ip='10.0.1.%s/24' % ((f + 1)), gateway='10.0.1.254')
            host2 = self.addHost('h%s' % (f+ 2 + 1), cls=IpHost, ip='10.0.2.%s/24' % ((f + 1)), gateway='10.0.2.254')
            self.addLink(host1, edgeSwitch1, **linkopts)
            self.addLink(host2, edgeSwitch2, **linkopts)

        
        for c in cores:
            switch1 = cores[c][0]
            self.addLink(edgeSwitch1, switch1, **linkopts)
            self.addLink(edgeSwitch2, switch1, **linkopts)

class IpHost(Host):
    def __init__(self, name, gateway, *args, **kwargs):
        super(IpHost, self).__init__(name, *args, **kwargs)
        self.gateway = gateway

    def config(self, **kwargs):
        Host.config(self, **kwargs)
        mtu = "ifconfig "+self.name+"-eth0 mtu 1490"
        self.cmd(mtu)
        self.cmd('ip route add default via %s' % self.gateway)


def testing(net, time):

    h1 = net.get("h1")
    h2 = net.get("h4")

    sleep(2)
    h1.cmd("ping -i 0.001 {}".format(h2.IP()))
    h2.cmd("tcpdump -XX -n -i {}-eth0 -w './pcaps/{}.pcap'".format("h4", time))


    sleep(5)
    net.configLinkStatus( node1, node2, 'down' )

    sleep(5)
    h1.cmd("kill %ping")
    h2.cmd("kill %tcpdump")
    net.configLinkStatus( node1, node2, 'up' )

    h2.cmd("tcpdump -tttttnr './pcaps/{t}.pcap' src host {ip} > ./results/'{t}.txt'".format(t=time, ip = h1.IP()))

    append_results(time)
    sleep(2)


def config(opts):

    core = opts.core
    fanout = opts.fanout
    node1 = opts.node1
    node2 = opts.node2
    controllers = ['192.168.56.1']
    topo = LeafAndSpine(core=core, fanout=fanout, node1=node1, node2=node2)
    net = Mininet(topo=topo, link=TCLink, build=False,
                  switch=UserSwitch,
                  controller = None,
                  autoSetMacs = True)
    i = 0
    for ip in controllers:
        net.addController( "c%s" % (i), controller=RemoteController, ip=ip)
        i += 1;
    net.build()
    net.start()
    CLI(net)
#    testing(net, ctime())
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    config(opts)
    os.system('sudo mn -c')

