

DEVICE=$1
PKTLEN=$2

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
pgset "clone_skb 0"
pgset "min_pkt_size $PKTLEN"
pgset "max_pkt_size $PKTLEN"
pgset "dst 192.168.20.242"
pgset "dst_mac 90:e2:ba:22:70:ac"
pgset "count 10000000"

# Time to run

PGDEV=/proc/net/pktgen/pgctrl

echo "Running... ctrl^C to stop"

pgset "start"

echo "Done"