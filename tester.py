import os
from optparse import OptionParser

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, UserSwitch, Host

from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import usnet, backup, ag_n_test
from time import ctime, sleep
from mininet.node import OVSSwitch
from functools import partial
import itertools


# Parse command line options and dump results
def parseOptions():
    """Parse command line options"""
    parser = OptionParser()
    parser.add_option('--controller', dest='controller', type='string', default='ryu',
                      help='controller ip')
    parser.add_option('--topo', dest='topo', type='string', default='backup',
                      help='topology to test')
    parser.add_option('--test', dest='test', type='string', default='none',
                      help='link, agg, or node test')
    parser.add_option('--bfd', dest='bfd', type='string', default='off',
                      help='')
    (options, args) = parser.parse_args()
    return options, args


opts, args = parseOptions()

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


def node_test(net):
    switches = net.switches

    for switch in switches:
        print (switch.name)



        if switch.name[1] == '1' or switch.name[1] == '7':
            print ('skip')

        else:
            filename = switch.name
            os.system("sudo tshark -n -i eth0 -T text > tester_results/{}.txt  &".format(filename))

            for k, v in switch.ports.items():
                if k.name[0] == 's':
                    switch.cmd("ifconfig {} down &".format(k))

            print (switch.name)

            sleep(1)
            net.pingAll()
            os.system("sudo pkill tshark")
            append_results(filename)

            for k, v in switch.ports.items():
                if k.name[0] == 's':
                    switch.cmd("ifconfig {} up &".format(k))




def link_test(net):
    links = net.links

    for link in links:
        node1 = link.intf1.node
        node2 = link.intf2.node

        intf_name = link.intf1.name
        intf_name2 = link.intf2.name

        print(intf_name + "       " + intf_name2)


        if intf_name[0] =='s' and intf_name2[0] == 's':
            filename = intf_name + '-' + intf_name2

            os.system("sudo tshark -n -i eth0 -T text > tester_results/{}.txt  &".format(filename))
            sleep(5)
            node1.cmd("ifconfig {} down &".format(intf_name))
            node2.cmd("ifconfig {} down &".format(intf_name2))

            sleep(5)

            # net.pingAll()
            os.system("sudo pkill tshark")
            append_results(filename)

            node1.cmd("ifconfig {} up &".format(intf_name))
            node2.cmd("ifconfig {} up &".format(intf_name2))
            sleep(2)






def agg_test(net):
    switches = net.switches
    links = net.links


    list(itertools.combinations(switches, 2))

    for pair in list(itertools.combinations(switches, 2)):

        switch1 = pair[0]
        switch2 = pair[1]

        print(switch1.name + "   " + switch2.name)
        filename = switch1.name + '-'+ switch2.name

        os.system("sudo tshark -n -i eth0 -T text > tester_results/{}.txt  &".format(filename))

        for intf in switch1.intfs:
            if intf.link.intf2.node == switch2:
                intf_name = intf.name
                intf_name2 = intf.link.intf2.name

                print(intf_name + "       " + intf_name2)

                switch1.cmd("ifconfig {} down &".format(intf_name))
                switch2.cmd("ifconfig {} down &".format(intf_name2))

        sleep(1)
        net.pingAll()

        os.system("sudo pkill tshark")
        append_results(filename)
        for intf in switch1.intfs:
            if intf.link.intf2.node == switch2:
                intf_name = intf.name
                intf_name2 = intf.link.intf2.name

                switch1.cmd("ifconfig {} up &".format(intf_name))
                switch2.cmd("ifconfig {} up &".format(intf_name2))

def append_results(filename):
    log = open("log.txt", 'a')

    print("./tester_results/{}.txt".format(filename))
    with open("./tester_results/{}.txt".format(filename), 'r') as file:
        start = -1
        first = -1
        last = -1
        mods = 0
        for line in file:
            l= line.split(' ')
            # print(l)
            if 'OFPT_PORT_STATUS\n' in l and start == -1:
                start = float(l[1])
                print(start)

            if 'OFPT_FLOW_MOD\n' in l:
                print("found flow mod")
                mods += 1
                if first == -1:
                    first = float(l[1]) - start
                last = float(l[1]) - start

        log.write("{},{},{},{},{}\n".format(filename, start, first, last, mods))

    log.close()


def config(opts):
    controller = opts.controller
    topo = opts.topo
    test = opts.test

    if controller  == 'ryu':
        ip = '172.31.21.103'

    if controller == 'onos':
        ip = '172.31.31.144'

    if topo == 'usnet':
        topo_func = usnet.USNET()
    if topo == 'backup':
        topo_func = backup.backup()
    if topo == 'agg':
        topo_func = ag_n_test.USNET()

    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    net = Mininet(topo=topo_func, switch=switch, controller=None)
    net.addController('c0', controller=RemoteController, ip=ip, port=6633)
    net.start()

    if opts.bfd == 'on':
        enable_bfd(net)
        print "bfd enabled"

    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    CLI(net)
    print "Testing network connectivity"

    if test == 'node':
        node_test(net)
    if test == 'link':
        for i in range(20):
            link_test(net)
    if test == 'agg':
        agg_test(net)

    # print(self.switches)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    config(opts)
    os.system('sudo mn -c')

