#!/bin/bash
# pktgen.conf -- Sample configuration for send

modprobe pktgen

DEVICE=$'h1-eth0'
PKTLEN=$2
CPUS=1


PKT_SIZE="pkt_size 64"
COUNT="count 0"
DELAY="delay 10000000"

ETH="h1-eth0"
MAC==$(ifconfig -a | grep h1-eth0 | cut -d' ' -f 11)

COUNT = "count 500"

if [ -z $DEVICE ]; then
  echo "$0 [IFNAME]"
	exit -1
fi

if [ -z $PKTLEN ]; then
	PKTLEN=64
	echo "packet length is $PKTLEN"
fi

function pgset() {
    local result

    echo $1 > $PGDEV

    result=`cat $PGDEV | fgrep "Result: OK:"`
    if [ "$result" = "" ]; then
         cat $PGDEV | fgrep Result:
    fi
}

function pg() {
    echo inject > $PGDEV
    cat $PGDEV
}

# On UP systems only one thread exists -- so just add devices

echo "Adding devices to run".

PGDEV=/proc/net/pktgen/kpktgend_0
pgset "rem_device_all"
pgset "add_device $DEVICE"



# Configure the individual devices
echo "Configuring devices"

PGDEV=/proc/net/pktgen/$DEVICE
pgset "$COUNT"
pgset "clone_skb 1"
pgset "min_pkt_size $PKTLEN"
pgset "max_pkt_size $PKTLEN"
pgset "$DELAY"
pgset "dst 10.0.0.2"
pgset "dst_mac 00:00:00:00:00:02"
pgset "count 10000000"

# Time to run

PGDEV=/proc/net/pktgen/pgctrl

echo "Running... ctrl^C to stop"

pgset "start"

echo "Done"
