#! /usr/bin/python3
from datetime import datetime
import csv
import sys
import math
import os
import time
from prometheus_api_client import PrometheusConnect
os.environ["TZ"] = "UTC"
time.tzset()

# INPUTS
# CLIENTS = ['Nimbus', 'Prysm', 'Teku', 'Lighthouse', 'Lodestar', 'Grandine']
CLIENT = str(sys.argv[1])
INIT = str(sys.argv[2])
END = str(sys.argv[3])
DELTA_T = float(sys.argv[4])  # seconds
URL = str(sys.argv[5])
G_SAMPLE = str(sys.argv[6])
CPU_RATE = float(sys.argv[7])
NET_RATE = float(sys.argv[8])
DISK_RATE = float(sys.argv[9])
LAYER = str(sys.argv[10])
LABEL = str(sys.argv[11])
iskiln = False
if(LABEL == 'NE_kiln-'):
    iskiln = True
    URL2 = str(sys.argv[12])
isfat = False
if(LABEL == "NE_fat-"):
    isfat = True

# rick: I assume this will be by parameter
NCPUS = 4
if(LABEL == "NE_fat-"):
    NCPUS = 32

# PARAMETERS
CLIENTS = [CLIENT]
Mega = float(1024*1024)
METRIC_MEMORY = 'node_memory_MemAvailable_bytes'
METRIC_MEMORYTOTAL = 'node_memory_MemTotal_bytes'
METRIC_CPU = 'node_cpu_seconds_total'
METRIC_NETRECV = 'node_network_receive_bytes_total'
METRIC_NETSENT = 'node_network_transmit_bytes_total'
METRIC_NETRECV_PACK = 'node_network_receive_packets_total'
METRIC_NETSENT_PACK = 'node_network_transmit_packets_total'
METRIC_SLOT = 'beacon_head_slot'
METRIC_PEERS = 'libp2p_peers'
METRIC_DISKTOTAL = "node_filesystem_size_bytes"
METRIC_DISKAVAIL = "node_filesystem_avail_bytes"
METRIC_DISKWRITE_BYTES = "node_disk_written_bytes_total"
METRIC_DISKREAD_BYTES = "node_disk_read_bytes_total"
METRIC_DISKWRITE_OPS = "node_disk_writes_completed_total"
METRIC_DISKREAD_OPS = "node_disk_reads_completed_total"
METRIC_EARNS = "validators_epoch_earned_amount_metrics"
METRIC_INCORRECTS = "validators_incorrect_head_metrics"
METRICS_INCORR_TARG = "validators_incorrect_target_metrics"
METRICS_INCORR_SRC = "validators_incorrect_source_metrics"


for CLIENT in CLIENTS:

    print(CLIENT)

    # INITIALIZATIONS
    isGrandine = False
    if(CLIENT == "Grandine"):
        isGrandine = True
    start_time = datetime.strptime(INIT, '%d/%m/%Y-%H:%M:%S:%f')
    end_time = datetime.strptime(END, '%d/%m/%Y-%H:%M:%S:%f')
    start_timestamp = start_time.timestamp()
    end_timestamp = end_time.timestamp()

    pid_name = LABEL+CLIENT
    memory_label = "{job='"+CLIENT+"_"+LAYER+"_resources'}"
    disk_label = "{job='"+CLIENT+"_"+LAYER+"_resources', device='/dev/sda1'}"
    disk_label_throughput = "{job='"+CLIENT + \
        "_"+LAYER+"_resources', device='sda'}"
    if((not iskiln) and (not isfat) and (CLIENT == "Lodestar" or CLIENT == "Lighthouse")):
        disk_label_throughput = "{job='"+CLIENT + \
            "_"+LAYER+"_resources', device='sdb'}"
    cpu_label = "{job='"+CLIENT+"_"+LAYER+"_resources', mode='user'}"
    net_label = "{job='"+CLIENT+"_"+LAYER+"_resources', device='ens3'}"
    beacon_label = ''
    if(LAYER == 'mainnet'):
        beacon_label = "{job='"+CLIENT.lower()+"_node'}"
    else:
        assert(iskiln)
        beacon_label = "{job='"+CLIENT+"'}"
    if(isfat and CLIENT == 'Teku'):
        beacon_label = "{job='Teku_node'}"
    validators_label = "{pool='kiln_"+CLIENT.lower()+"'}"

    # OBTAIN DATA
    prom = PrometheusConnect(
        url=URL, disable_ssl=True)

    # metric cpu
    cpu_data = prom.get_metric_range_data(
        METRIC_CPU+cpu_label,
        start_time=start_time,
        end_time=end_time,
    )

    # metric memory
    memory_data = prom.get_metric_range_data(
        METRIC_MEMORY+memory_label,
        start_time=start_time,
        end_time=end_time,
    )

    # metric memory 2
    memTot_data = prom.get_metric_range_data(
        METRIC_MEMORYTOTAL+memory_label,
        start_time=start_time,
        end_time=end_time,
    )

    # NET_SENT
    netsent_data = prom.get_metric_range_data(
        METRIC_NETSENT+net_label,
        start_time=start_time,
        end_time=end_time,
    )

    # NET_RECEIVED
    netrecv_data = prom.get_metric_range_data(
        METRIC_NETRECV+net_label,
        start_time=start_time,
        end_time=end_time,
    )

    # DISK NODE USAGE
    diskavail_data = prom.get_metric_range_data(
        METRIC_DISKAVAIL+disk_label,
        start_time=start_time,
        end_time=end_time,
    )
    disktot_data = prom.get_metric_range_data(
        METRIC_DISKTOTAL+disk_label,
        start_time=start_time,
        end_time=end_time,
    )
    # SLOT
    slot_data = []
    if(not isGrandine):
        slot_data = prom.get_metric_range_data(
            METRIC_SLOT+beacon_label,
            start_time=start_time,
            end_time=end_time,
        )
    else:
        file = open(G_SAMPLE)
        csvreader = csv.reader(file)
        header = []
        header = next(csvreader)
        for row in csvreader:
            ts = datetime.strptime(row[2], '%d/%m/%Y-%H:%M:%S:%f').timestamp()
            slot_data.append([ts, row[8]])
        file.close()

    # PEERS
    peers_data = prom.get_metric_range_data(
        METRIC_PEERS+beacon_label,
        start_time=start_time,
        end_time=end_time,
    )
    peers_on = True
    if(len(peers_data) == 0):
        peers_on = False

    # VALIDATORS DATA
    earns_data = []
    incorrect_heads_data = []
    incorrect_target_data = []
    incorrect_source_data = []
    if(iskiln):
        prom2 = PrometheusConnect(
            url=URL2, disable_ssl=True)
        earns_data = prom2.get_metric_range_data(
            METRIC_EARNS+validators_label,
            start_time=start_time,
            end_time=end_time,
        )
        incorrect_heads_data = prom2.get_metric_range_data(
            METRIC_INCORRECTS+validators_label,
            start_time=start_time,
            end_time=end_time,
        )
        incorrect_target_data = prom2.get_metric_range_data(
            METRICS_INCORR_TARG+validators_label,
            start_time=start_time,
            end_time=end_time,
        )
        incorrect_source_data = prom2.get_metric_range_data(
            METRICS_INCORR_SRC+validators_label,
            start_time=start_time,
            end_time=end_time,
        )

    # DEFINE DOABLE TIME INERVALS
    start_timestamp_eval = start_timestamp
    # start_timestamp_eval = max(cpu_data[0]['values'][0][0], start_timestamp)
    while(start_timestamp_eval < cpu_data[0]['values'][0][0]):
        start_timestamp_eval += DELTA_T
    if(not isGrandine):
        # start_timestamp_eval = max(
        #    slot_data[0]['values'][0][0], start_timestamp_eval)
        while(start_timestamp_eval < slot_data[0]['values'][0][0]):
            start_timestamp_eval += DELTA_T
    else:
        # start_timestamp_eval = max(
        #    slot_data[0][0], start_timestamp_eval)
        while(start_timestamp_eval < slot_data[0][0]):
            start_timestamp_eval += DELTA_T
    if(peers_on):
        # start_timestamp_eval = max(
        #    peers_data[0]['values'][0][0], start_timestamp_eval)
        while(start_timestamp_eval < peers_data[0]['values'][0][0]):
            start_timestamp_eval += DELTA_T
    if(iskiln):
        while(start_timestamp_eval < earns_data[0]['values'][0][0]):
            start_timestamp_eval += DELTA_T

    # round-off to seconds:
    start_timestamp_eval = float(math.ceil(start_timestamp_eval))

    nsteps_node = len(cpu_data[0]['values'])
    end_timestamp_eval = min(
        cpu_data[0]['values'][nsteps_node-1][0], end_timestamp)
    nsteps_beacon = 0
    if(not isGrandine):
        nsteps_beacon = len(slot_data[0]['values'])
        end_timestamp_eval = min(
            slot_data[0]['values'][nsteps_beacon-1][0], end_timestamp_eval)
    else:
        nsteps_beacon = len(slot_data)
        end_timestamp_eval = min(
            slot_data[nsteps_beacon-1][0], end_timestamp_eval)
    if(peers_on):
        nsteps_libp2p = len(peers_data[0]['values'])
        end_timestamp_eval = min(
            peers_data[0]['values'][nsteps_libp2p-1][0], end_timestamp_eval)
    if(iskiln):
        nsteps_kiln = len(earns_data[0]['values'])
        end_timestamp_eval = min(
            earns_data[0]['values'][nsteps_kiln-1][0], end_timestamp_eval)

    # ROUND END_TIMESTAMP_EVAL to DELTA_T
    time_length = end_timestamp_eval - start_timestamp_eval
    nsteps = math.floor(time_length/DELTA_T)
    end_timestamp_eval = start_timestamp_eval + nsteps*DELTA_T

    # GENERATE OUTPUT

    real_start_timestamp = -1.0
    real_end_timestamp = 0

    target_timestamp = start_timestamp_eval
    base_netsent = -1.0
    base_netrecv = -1.0
    index_val = 0
    output = []

    icont1_node = 0
    previous_timestamp_node = 0
    next_timestamp_node = cpu_data[0]['values'][icont1_node][0]

    icont1_beacon = 0
    previous_timestamp_beacon = 0
    next_timestamp_beacon = 0
    if(not isGrandine):
        next_timestamp_beacon = slot_data[0]['values'][icont1_beacon][0]
    else:
        next_timestamp_beacon = slot_data[icont1_beacon][0]

    icont1_libp2p = 0
    previous_timestamp_libp2p = 0
    next_timestamp_libp2p = 0
    if(peers_on):
        next_timestamp_libp2p = peers_data[0]['values'][icont1_libp2p][0]

    icont1_validators = 0
    previous_timestamp_validators = 0
    next_timestamp_validators = 0
    if(iskiln):
        next_timestamp_validators = earns_data[0]['values'][icont1_validators][0]

    while(target_timestamp < end_timestamp_eval):

        # define interval enclosing target time for node and beacon
        while(next_timestamp_node <= target_timestamp):
            previous_timestamp_node = next_timestamp_node
            icont1_node += 1
            next_timestamp_node = cpu_data[0]['values'][icont1_node][0]

        while(next_timestamp_beacon <= target_timestamp):
            previous_timestamp_beacon = next_timestamp_beacon
            icont1_beacon += 1
            next_timestamp_beacon = 0
            if(not isGrandine):
                next_timestamp_beacon = slot_data[0]['values'][icont1_beacon][0]
            else:
                next_timestamp_beacon = slot_data[icont1_beacon][0]

        if(peers_on):
            while(next_timestamp_libp2p <= target_timestamp):
                previous_timestamp_libp2p = next_timestamp_libp2p
                icont1_libp2p += 1
                next_timestamp_libp2p = peers_data[0]['values'][icont1_libp2p][0]

        if(iskiln):
            while(next_timestamp_validators <= target_timestamp):
                previous_timestamp_validators = next_timestamp_validators
                icont1_validators += 1
                next_timestamp_validators = earns_data[0]['values'][icont1_validators][0]

        if(next_timestamp_node > end_timestamp_eval or
                next_timestamp_beacon > end_timestamp_eval or
                (peers_on and next_timestamp_libp2p > end_timestamp_eval) or
                (iskiln and next_timestamp_validators > end_timestamp_eval)):
            break

        #
        # COLSEST INDES FOR NODE
        #
        index_val = icont1_node
        icont0 = icont1_node - 1
        time_step = next_timestamp_node - previous_timestamp_node

        dist1 = target_timestamp - previous_timestamp_node
        dist2 = next_timestamp_node - target_timestamp
        if(dist1 < dist2):
            index_val = icont0

        # print time
        # print_time = datetimefromtimestamp(target_timestamp).strftime(
        #    '%d/%m/%Y-%H:%M:%S:%f')

        # print cpu
        # rick: I assume that this will be overwitten, it is not correct if ncp!=4
        print_cpu0 = float(cpu_data[0]['values'][index_val][1])
        print_cpu1 = float(cpu_data[1]['values'][index_val][1])
        print_cpu2 = float(cpu_data[2]['values'][index_val][1])
        print_cpu3 = float(cpu_data[3]['values'][index_val][1])

        if(icont1_node >= 1):
            print_cpu = print_cpu0 + print_cpu1 + print_cpu2 + print_cpu3
            print_slope0 = 100 * \
                (float(cpu_data[0]['values'][icont1_node][1]) -
                 float(cpu_data[0]['values'][icont0][1])) / float(time_step)
            print_slope1 = 100 * \
                (float(cpu_data[1]['values'][icont1_node][1]) -
                 float(cpu_data[1]['values'][icont0][1])) / float(time_step)
            print_slope2 = 100 * \
                (float(cpu_data[2]['values'][icont1_node][1]) -
                 float(cpu_data[2]['values'][icont0][1])) / float(time_step)
            print_slope3 = 100 * \
                (float(cpu_data[3]['values'][icont1_node][1]) -
                 float(cpu_data[3]['values'][icont0][1])) / float(time_step)

            print_slope = 0.25*(print_slope0 + print_slope1 +
                                print_slope2 + print_slope3)

        # print mem
        tot_mem = memTot_data[0]['values'][index_val][1]
        print_mem = memory_data[0]['values'][index_val][1]
        print_mem = float(float(tot_mem)-float(print_mem))/Mega

        print_mem_pers = 100.0*(float(print_mem)*Mega)/float(tot_mem)

        # print netsent
        if(base_netsent == -1.0):
            base_netsent = float(netsent_data[0]['values'][index_val][1])
        print_netsent = float(
            netsent_data[0]['values'][index_val][1])-base_netsent
        print_netsent = print_netsent/Mega
        if(icont1_node >= 1):
            print_netsent_rate = (float(netsent_data[0]['values'][icont1_node][1]) -
                                  float(netsent_data[0]['values'][icont0][1])) / (Mega*float(time_step))

        # print netrecv
        if(base_netrecv == -1.0):
            base_netrecv = float(
                netrecv_data[0]['values'][index_val][1])
        print_netrecv = float(
            netrecv_data[0]['values'][index_val][1])-base_netrecv
        print_netrecv = print_netrecv/Mega
        if(icont1_node >= 1):
            print_netrecv_rate = (float(netrecv_data[0]['values'][icont1_node][1]) -
                                  float(netrecv_data[0]['values'][icont0][1])) / (Mega*float(time_step))

        # node disk
        tot_disk = disktot_data[0]['values'][index_val][1]
        print_disk = diskavail_data[0]['values'][index_val][1]
        print_disk = float(float(tot_disk)-float(print_disk))/Mega
        print_disk_pers = 100.0*(float(print_disk)*Mega)/float(tot_disk)

        #
        # CLOSEST INDEX FOR SLOT
        #
        index_val = icont1_beacon
        icont0 = icont1_beacon - 1
        dist1 = target_timestamp - previous_timestamp_beacon
        dist2 = next_timestamp_beacon - target_timestamp
        if(dist1 < dist2):
            index_val = icont0

        # print slot
        print_slot = 0
        if(not isGrandine):
            print_slot = slot_data[0]['values'][index_val][1]
        else:
            print_slot = slot_data[index_val][1]

        #
        # CLOSEST INDEX FOR PEERS
        #
        print_peers = 0
        if(peers_on):
            index_val = icont1_libp2p
            icont0 = icont1_libp2p - 1
            dist1 = target_timestamp - previous_timestamp_libp2p
            dist2 = next_timestamp_libp2p - target_timestamp
            if(dist1 < dist2):
                index_val = icont0
            # print peers
            print_peers = peers_data[0]['values'][index_val][1]

        #
        # CLOSEST INDEX FOR VALIDATORS
        #
        print_earns = 0
        print_incorrects = 0
        print_incorr_target = 0
        print_incorr_source = 0

        if(iskiln):
            index_val = icont1_validators
            icont0 = icont1_validators - 1
            dist1 = target_timestamp - previous_timestamp_validators
            dist2 = next_timestamp_validators - target_timestamp
            if(dist1 < dist2):
                index_val = icont0
            # print earns
            print_earns = earns_data[0]['values'][index_val][1]
            print_incorrects = incorrect_heads_data[0]['values'][index_val][1]
            print_incorr_target = incorrect_target_data[0]['values'][index_val][1]
            print_incorr_source = incorrect_source_data[0]['values'][index_val][1]

        # fill row
        if(icont1_node >= 1):

            if(real_start_timestamp < 0):
                real_start_timestamp = target_timestamp
            real_end_timestamp = target_timestamp
            row = [0, pid_name, target_timestamp,
                   str(0), str(print_slope), str(print_mem),
                   str(print_netsent), str(print_netrecv), str(print_slot),
                   str(print_peers), str(print_mem_pers), str(0),
                   str(0), str(0), str(print_slope0),
                   str(print_slope1), str(print_slope2), str(print_slope3),
                   str(print_disk), str(print_disk_pers), str(0),
                   str(0), str(0), str(0),
                   str(0), str(0), str(print_netsent_rate),
                   str(print_netrecv_rate), str(0), str(0),
                   str(print_earns), str(print_incorrects), str(
                       print_incorr_target),
                   str(print_incorr_source)]
            output.append(row)

        target_timestamp += DELTA_T

    # override rate cpu
    nrows = len(output)
    max_rows = 10000
    niters0 = math.ceil(nrows/max_rows)
    time0 = real_start_timestamp
    jcont = 0
    for i in range(niters0):
        time1 = min(real_end_timestamp, time0+(max_rows-1)*DELTA_T)
        niters1 = round((time1-time0)/DELTA_T + 1)
        # cpu rate
        query_rate = "rate("+METRIC_CPU+cpu_label + \
            "["+str(int(CPU_RATE))+"s])"
        cpu_rate_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        auxlen = len(cpu_rate_data[0]['values'])
        # cpu rate 60
        query_rate_60 = "rate("+METRIC_CPU+cpu_label+"[60s])"
        cpu_rate_data_60 = prom.custom_query_range(
            query_rate_60,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        auxlen60 = len(cpu_rate_data_60[0]['values'])
        # cpu rate 300
        query_rate_300 = "rate("+METRIC_CPU+cpu_label+"[300s])"
        cpu_rate_data_300 = prom.custom_query_range(
            query_rate_300,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        auxlen300 = len(cpu_rate_data_300[0]['values'])
        # cpu rate 900
        query_rate_900 = "rate("+METRIC_CPU+cpu_label+"[900s])"
        cpu_rate_data_900 = prom.custom_query_range(
            query_rate_900,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        auxlen900 = len(cpu_rate_data_900[0]['values'])

        for j in range(auxlen):
            pos = int((cpu_rate_data[0]['values'][j][0]-time0)/DELTA_T)
            auxtime1 = time0+pos*DELTA_T
            auxtime2 = float(cpu_rate_data[0]['values'][j][0])
            assert(math.fabs(auxtime1-auxtime2) <= 0.0)
            avercpu = 0
            for k in range(NCPUS):
                auxval = float(cpu_rate_data[k]['values'][j][1])
                avercpu += auxval
                if(k < 4):
                    output[jcont+pos][14+k] = str(100.0*auxval)
            avercpu = 100.0/float(NCPUS) * avercpu
            output[jcont+pos][4] = str(avercpu)
            output[jcont+pos][0] += 1
            auxtime3 = output[jcont+pos][2]
            assert(math.fabs(auxtime3-auxtime2) <= 0.0)

        for j in range(auxlen60):
            pos = int((cpu_rate_data_60[0]['values'][j][0]-time0)/DELTA_T)
            auxtime1 = time0+pos*DELTA_T
            auxtime2 = float(cpu_rate_data_60[0]['values'][j][0])
            assert(math.fabs(auxtime1-auxtime2) <= 0.0)
            avercpu60 = 0
            for k in range(NCPUS):
                avercpu60 += float(cpu_rate_data_60[k]['values'][j][1])
            avercpu60 = 100.0/float(NCPUS) * avercpu60
            output[jcont+pos][11] = str(avercpu60)
            #output[jcont+pos][0] += 1
            auxtime3 = output[jcont+pos][2]
            assert(math.fabs(auxtime3-auxtime2) <= 0.0)

        for j in range(auxlen300):
            pos = int((cpu_rate_data_300[0]['values'][j][0]-time0)/DELTA_T)
            auxtime1 = time0+pos*DELTA_T
            auxtime2 = float(cpu_rate_data_300[0]['values'][j][0])
            assert(math.fabs(auxtime1-auxtime2) <= 0.0)
            avercpu300 = 0
            for k in range(NCPUS):
                avercpu300 += float(cpu_rate_data_300[k]['values'][j][1])
            avercpu300 = 100.0/float(NCPUS) * avercpu300
            output[jcont+pos][12] = str(avercpu300)
            #output[jcont+pos][0] += 1
            auxtime3 = output[jcont+pos][2]
            assert(math.fabs(auxtime3-auxtime2) <= 0.0)

        for j in range(auxlen900):
            pos = int((cpu_rate_data_900[0]['values'][j][0]-time0)/DELTA_T)
            auxtime1 = time0+pos*DELTA_T
            auxtime2 = float(cpu_rate_data_900[0]['values'][j][0])
            assert(math.fabs(auxtime1-auxtime2) <= 0.0)
            avercpu900 = 0
            for k in range(NCPUS):
                avercpu900 += float(cpu_rate_data_900[k]['values'][j][1])
            avercpu900 = 100.0/float(NCPUS) * avercpu900
            output[jcont+pos][13] = str(avercpu900)
            #output[jcont+pos][0] += 1
            auxtime3 = output[jcont+pos][2]
            assert(math.fabs(auxtime3-auxtime2) <= 0.0)

        jcont = jcont+niters1
        time0 = time1 + DELTA_T

    # override rate network
    nrows = len(output)
    max_rows = 10000
    niters0 = math.ceil(nrows/max_rows)
    time0 = real_start_timestamp
    jcont = 0
    for i in range(niters0):
        time1 = min(real_end_timestamp, time0+(max_rows-1)*DELTA_T)
        niters1 = round((time1-time0)/DELTA_T + 1)
        query_rate = "rate("+METRIC_NETSENT+net_label + \
            "["+str(int(NET_RATE))+"s])"
        netsend_rate_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_NETRECV+net_label + \
            "["+str(int(NET_RATE))+"s])"
        netrecv_rate_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_NETSENT_PACK+net_label + \
            "["+str(int(NET_RATE))+"s])"
        packsend_rate_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_NETRECV_PACK+net_label + \
            "["+str(int(NET_RATE))+"s])"
        packrecv_rate_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        auxlen0 = len(netsend_rate_data[0]['values'])
        auxlen1 = len(netrecv_rate_data[0]['values'])
        auxlen2 = len(packsend_rate_data[0]['values'])
        auxlen3 = len(packrecv_rate_data[0]['values'])

        assert(auxlen0 == auxlen1 == auxlen2 == auxlen3)
        for j in range(auxlen0):
            pos = int((netsend_rate_data[0]['values'][j][0]-time0)/DELTA_T)
            auxtime1 = time0+pos*DELTA_T
            auxtime2 = float(netsend_rate_data[0]['values'][j][0])
            auxtime3 = float(netrecv_rate_data[0]['values'][j][0])
            auxtime4 = float(packsend_rate_data[0]['values'][j][0])
            auxtime5 = float(packrecv_rate_data[0]['values'][j][0])
            assert(auxtime1 == auxtime2 == auxtime3 == auxtime4 == auxtime5)
            netsend_val = float(netsend_rate_data[0]['values'][j][1])/Mega
            netrecv_val = float(netrecv_rate_data[0]['values'][j][1])/Mega
            packsend_val = float(packsend_rate_data[0]['values'][j][1])
            packrecv_val = float(packrecv_rate_data[0]['values'][j][1])
            output[jcont+pos][26] = str(netsend_val)
            output[jcont+pos][27] = str(netrecv_val)
            output[jcont+pos][28] = str(packsend_val)
            output[jcont+pos][29] = str(packrecv_val)
            output[jcont+pos][0] += 1
            auxtime4 = output[jcont+pos][2]
            assert(math.fabs(auxtime4-auxtime2) <= 0.0)

        jcont = jcont+niters1
        time0 = time1 + DELTA_T

    # add io metrics
    nrows = len(output)
    max_rows = 10000
    niters0 = math.ceil(nrows/max_rows)
    time0 = real_start_timestamp
    jcont = 0
    for i in range(niters0):
        time1 = min(real_end_timestamp, time0+(max_rows-1)*DELTA_T)
        niters1 = round((time1-time0)/DELTA_T + 1)

        query_rate = "rate("+METRIC_DISKWRITE_BYTES + \
            disk_label_throughput+"["+str(int(DISK_RATE))+"s])"
        diskwritte_bytes_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_DISKREAD_BYTES + \
            disk_label_throughput+"["+str(int(DISK_RATE))+"s])"
        diskread_bytes_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_DISKWRITE_OPS + \
            disk_label_throughput+"["+str(int(DISK_RATE))+"s])"
        diskwritte_ops_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )
        query_rate = "rate("+METRIC_DISKREAD_OPS + \
            disk_label_throughput+"["+str(int(DISK_RATE))+"s])"
        diskread_ops_data = prom.custom_query_range(
            query_rate,
            start_time=datetime.fromtimestamp(time0),
            end_time=datetime.fromtimestamp(time1),
            step=DELTA_T
        )

        auxlen0 = len(diskwritte_bytes_data[0]['values'])
        auxlen1 = len(diskread_bytes_data[0]['values'])
        auxlen2 = len(diskwritte_ops_data[0]['values'])
        auxlen3 = len(diskread_ops_data[0]['values'])
        assert(auxlen0 == auxlen1 == auxlen2 == auxlen3)

        for j in range(auxlen0):
            pos = int(
                (diskwritte_bytes_data[0]['values'][j][0]-time0)/DELTA_T)
            auxtime = time0+pos*DELTA_T
            auxtime0 = float(diskwritte_bytes_data[0]['values'][j][0])
            auxtime1 = float(diskread_bytes_data[0]['values'][j][0])
            auxtime2 = float(diskwritte_ops_data[0]['values'][j][0])
            auxtime3 = float(diskread_ops_data[0]['values'][j][0])
            assert(auxtime == auxtime0 == auxtime1 == auxtime2 == auxtime3)
            writtebytes_val = float(
                diskread_bytes_data[0]['values'][j][1])/Mega
            readbytes_val = float(
                diskread_bytes_data[0]['values'][j][1])/Mega
            writteops_val = float(diskwritte_ops_data[0]['values'][j][1])
            readops_val = float(diskread_ops_data[0]['values'][j][1])
            output[jcont+pos][20] = str(writtebytes_val)
            output[jcont+pos][21] = str(readbytes_val)
            output[jcont+pos][22] = str(writteops_val)
            output[jcont+pos][23] = str(readops_val)
            #output[jcont+pos][0] += 1
            auxtime4 = output[jcont+pos][2]
            assert(math.fabs(auxtime4-auxtime0) <= 0.0)

        jcont = jcont+niters1
        time0 = time1 + DELTA_T

    # WRITE IN FILE
    inittime = -1
    endtime = 0
    with open("NE_"+CLIENT+'.csv', 'w') as f:
        f.write(
            'PID,' +  # 0
            'PID_NAME,' +  # 1
            'TIME[dd/mm/yyyy - hh:mm:ss:ms],' +  # 2
            'DISKUSAGE[MB],' +  # 3
            'CPU[%],' +  # 4
            'MEM[MB],' +  # 5
            'NET_SENT[MB],' +  # 6
            'NET_RECEIVED[MB],' +  # 7
            'CURRENT_SLOT,' +  # 8
            'CURRENT_PEERS,' +  # 9
            'MEM[%],' +  # 10
            'CPU 60s[%],' +  # 11
            'CPU 300s[%],' +  # 12
            'CPU 900s[%],' +  # 13
            'CPU0[%],' +  # 14
            'CPU1[%],' +  # 15
            'CPU2[%],' +  # 16
            'CPU3[%],' +  # 17
            'DISK NODE[MB],' +  # 18
            'DISK NODE[%],' +  # 19
            'IO WRITTE[MB/s],' +  # 20
            'IO READ[MB/s],' +  # 21
            'IO WRITTE[Op/s],' +  # 22
            'IO READ[Op/s],' +  # 23
            'IO WRITTE[%],' +
            'IO READ[%],' +
            'NET_SENT[MB/s],' +  # 26
            'NET_RECV[MB/s],' +  # 27
            'NET_SEND[pack/s],' +  # 28
            'NET_RECV[pack/s],' +  # 29
            'EANRS,' +  # 30 only for kiln
            'INCORRECTS_HEAD,' +  # 31  only for kiln
            'INCORRECTS_TARGET,' +  # 32  only for kiln
            'INCORRECTS_SOURCE,')  # 33  only for kiln

        f.write('\n')
        for row in output:
            aux = row[2]
            print_time = datetime.utcfromtimestamp(row[2]).strftime(
                '%d/%m/%Y-%H:%M:%S:%f')
            row[2] = str(print_time)
            # if(row[0] == 2):
            row[0] = str(row[0])
            f.write(','.join(row))
            f.write('\n')
            if(inittime < 0):
                inittime = aux
            endtime = aux

    diffsec = float(inittime-start_timestamp)
    print("   Init:", datetime.fromtimestamp(
        inittime).strftime('%d/%m/%Y-%H:%M:%S:%f'), "+"+str(round(diffsec, 1))+"s", str(round(diffsec/DELTA_T, 1))+" rows")
    diffsec = end_timestamp-endtime
    print("   End: ", datetime.fromtimestamp(
        endtime).strftime('%d/%m/%Y-%H:%M:%S:%f'), "-"+str(round(diffsec, 1))+"s", str(round(diffsec/DELTA_T, 1))+" rows")


# pujar codi al gitlab
# fer més concís
