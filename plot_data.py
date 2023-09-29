"""


BSD 3-Clause License

Copyright (c) 2021, by Barcelona SuperComputing Center
                Contributors: Tarun Mohandas
                              Leonardo Bautista
                E-mail: tarun.mohandas@bsc.es
                URL: https://github.com/migalabs/eth2-client-analyzer
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""



"""

This script outputs information about hardware consumption within a single process and single folder
It receives two areguments:
- PID: process to be monitored
- folder: folder whose size to monitor

This script not only outputs through terminal the results but also writes to disk in CSV format

python3 plot_data.py disk 30 1000 "01/02/2022 00:00" file1.csv file2.csv...

"""


import configparser
from pydoc import cli
from matplotlib import ticker
import matplotlib.pyplot as plt
import matplotlib
import csv
import datetime
import sys
import numpy as np
import pandas as pd
import os
import time
import matplotlib.dates as mdates
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.ticker import MaxNLocator

MAX_NUM_VALIDATORS = 100
MAX_NUM_VALIDATORS_10 = 10

VALIDATOR_CHANGE_TIME = datetime.datetime.strptime("01/04/2022-10:28:43:000000", '%d/%m/%Y-%H:%M:%S:%f').timestamp()

os.environ["TZ"] = "UTC"
time.tzset()

colors = {
    'prysm':        ['#ce1e16', '#e68e8a', '#7b120d', '#9fc0b6', '#538e7b', '#204136'], # red
    'lighthouse':   ['#3232ff', '#b2b2ff', '#00007f', '#ffbc8f', '#ff791f', '#994812'], # blue
    'teku':         ['#ffa500', '#ffd27f', '#7f5200', '#bacce4', '#7e99bd', '#465569'], # orange
    'nimbus':       ['#008000', '#99cc99', '#004000', '#d9c5b2', '#a08a74', '#50453a'], # green
    'lodestar':     ['#8c198c', '#cc99cc', '#4c004c', '#9adf7b', '#58a835', '#2c541a'], # purple
    'grandine':     ['#999900', '#cccc7f', '#4c4c00', '#e69da5', '#c82236', '#610510'], # yellow / gold
}

class ColorQueue():

    def __init__(self, i_first_index: int):
        self.colorIndex = {
            "prysm": i_first_index,
            "lighthouse": i_first_index,
            "teku": i_first_index,
            "nimbus": i_first_index,
            "lodestar": i_first_index,
            "grandine": i_first_index,
        }

    def obtain_next_color(self, i_client_name: str):
        for key, value in self.colorIndex.items():
            if key.lower() in i_client_name.lower():
                # we found the client
                self.colorIndex[key] = int(value + 1)
                return colors[key][value % len(self.colorIndex)]
                


colorMap = {
    'prysm':                    colors['prysm'][1], # red
    'lighthouse':               colors['lighthouse'][1], # blue
    'teku':                     colors['teku'][1], # orange
    'nimbus':                   colors['nimbus'][1], # green
    'lodestar':                 colors['lodestar'][1], # purple
    'grandine':                 colors['grandine'][1], # yellow / gold
    'NE_Prysm':                 colors['prysm'][0],
    'NE_Lighthouse':            colors['lighthouse'][0],
    'NE_Teku':                  colors['teku'][0],
    'NE_Nimbus':                colors['nimbus'][0],
    'NE_Lodestar':              colors['lodestar'][0],
    'NE_Grandine':              colors['grandine'][0],
    'all-topics-prysm':         colors['prysm'][1], # red
    'all-topics-lighthouse':    colors['lighthouse'][1], # blue
    'all-topics-teku':          colors['teku'][1], # orange
    'all-topics-nimbus':        colors['nimbus'][1], # green
    'all-topics-lodestar':      colors['lodestar'][1], # purple
    'all-topics-grandine':      colors['grandine'][1], # yellow / gold

}

secondColorMap = {
    'prysm':                    colors['prysm'][3], # red
    'lighthouse':               colors['lighthouse'][3], # blue
    'teku':                     colors['teku'][3], # orange
    'nimbus':                   colors['nimbus'][3], # green
    'lodestar':                 colors['lodestar'][3], # purple
    'grandine':                 colors['grandine'][3], # yellow / gold
    'NE_Prysm':                 colors['prysm'][3],
    'NE_Lighthouse':            colors['lighthouse'][3],
    'NE_Teku':                  colors['teku'][3],
    'NE_Nimbus':                colors['nimbus'][3],
    'NE_Lodestar':              colors['lodestar'][3],
    'NE_Grandine':              colors['grandine'][3],
    'all-topics-prysm':         colors['prysm'][3], # red
    'all-topics-lighthouse':    colors['lighthouse'][3], # blue
    'all-topics-teku':          colors['teku'][3], # orange
    'all-topics-nimbus':        colors['nimbus'][3], # green
    'all-topics-lodestar':      colors['lodestar'][3], # purple
    'all-topics-grandine':      colors['grandine'][3], # yellow / gold

}

MAX_MAJOR_TICKS = 5

class ClientData():

    seq_number = 0
    timestamp = 1
    disk_usage = 2
    cpu_usage = 3
    mem_usage = 4
    net_sent = 5
    net_received = 6
    current_slot = 7
    current_peers = 8
    mem_percentage = 9
    cpu60 = 10
    cpu300 = 11
    cpu900 = 12
    cpu_0 = 13
    cpu_1 = 14
    cpu_2 = 15
    cpu_3 = 16
    disk_node_mb = 17
    disk_node_prcnt = 18
    io_write_mb_s = 19
    io_read_mb_s = 20
    io_write_op_s = 21
    io_read_op_s = 22
    io_write_prcnt = 23
    io_read_prcnt = 24
    net_sent_mb_s = 25
    net_received_mb_s = 26
    net_sent_pkg_s = 27
    net_received_pkg_s = 28
    tcp = 29
    rewards = 30
    num_validators = 31
    incorrect_heads = 32
    incorrect_heads_prcnt = 33
    rewards_beacon_api = 34
    incorrect_sources = 35
    incorrect_sources_prcnt = 36
    max_rewards = 37


    def __init__(self, i_pid, i_name):
        self.pid = i_pid
        self.name = i_name

        self.data = []

        for _ in range(0,38):
            self.data.append([])


        # data, each row corresponds to an array of data
    def add_row(self, i_row):
        #self.timestamp.append(mktime(datetime.datetime.strptime(i_row[2], '%B %d %H:%M:%S:%f').timetuple()))
        try:
            self.data[self.timestamp].append(datetime.datetime.strptime(i_row[2], '%d/%m/%Y-%H:%M:%S:%f').timestamp())

            if "RP-" in self.name:
                self.data[self.timestamp][-1] = (datetime.datetime.strptime(i_row[2], '%d/%m/%Y-%H:%M:%S:%f') - datetime.timedelta(hours=2)).timestamp()
        except:
            return
        self.data[self.seq_number].append(int(len(self.data[self.seq_number])))
        
            
        diskUsage_GB = float(i_row[3]) * 1000000 / (1024 * 1024 * 1024) # from bytes to GB
        if "NE_" in self.name:
            diskUsage_GB = float(i_row[3]) / 1024
        self.data[self.disk_usage].append(float("{:.2f}".format(diskUsage_GB)))
        
        self.data[self.cpu_usage].append(float("{:.2f}".format(float(i_row[4]))))
        
        memUsage_MB = float(i_row[5]) * 1000000 / (1024 * 1024) # from bytes to MB
        if "NE_" in self.name:
            memUsage_MB = float(i_row[5])
        self.data[self.mem_usage].append(float("{:.2f}".format(memUsage_MB)))


        netSent_GB = float(i_row[6]) * 1000000 / (1024 * 1024 * 1024) # from bytes to GB
        if "NE_" in self.name:
            netSent_GB = float(i_row[6]) / 1024
        self.data[self.net_sent].append(netSent_GB)
        
        netRecived_GB = float(i_row[7]) * 1000000 / (1024 * 1024 * 1024) # from bytes to GB
        if "NE_" in self.name:
            netRecived_GB = float(i_row[7]) / 1024

        self.data[self.net_received].append(float("{:.2f}".format(netRecived_GB)))
        self.data[self.current_slot].append(int(i_row[8]))
        self.data[self.current_peers].append(int(i_row[9]))

        if "NE_" in self.name:
            # in csv 0 - 1
            self.data[self.mem_percentage].append(float("{:.2f}".format(float(i_row[10]))))

            self.data[self.cpu60].append(float("{:.2f}".format(float(i_row[11]))))
            self.data[self.cpu300].append(float("{:.2f}".format(float(i_row[12]))))
            self.data[self.cpu900].append(float("{:.2f}".format(float(i_row[13]))))

            self.data[self.cpu_0].append(float("{:.2f}".format(float(i_row[14]))))
            self.data[self.cpu_1].append(float("{:.2f}".format(float(i_row[15]))))
            self.data[self.cpu_2].append(float("{:.2f}".format(float(i_row[16]))))
            self.data[self.cpu_3].append(float("{:.2f}".format(float(i_row[17]))))

            self.data[self.disk_node_mb].append(float("{:.2f}".format(float(i_row[18]))))
            self.data[self.disk_node_prcnt].append(float("{:.2f}".format(float(i_row[19]))))

            self.data[self.io_write_mb_s].append(float("{:.2f}".format(float(i_row[20]))))
            self.data[self.io_read_mb_s].append(float("{:.2f}".format(float(i_row[21]))))
            self.data[self.io_write_op_s].append(float("{:.2f}".format(float(i_row[22]))))
            self.data[self.io_read_op_s].append(float("{:.2f}".format(float(i_row[23]))))
            self.data[self.io_write_prcnt].append(float("{:.2f}".format(float(i_row[24]))))
            self.data[self.io_read_prcnt].append(float("{:.2f}".format(float(i_row[25]))))

            self.data[self.net_sent_mb_s].append(float("{:.2f}".format(float(i_row[26]))))
            self.data[self.net_received_mb_s].append(float("{:.2f}".format(float(i_row[27]))))
            self.data[self.net_sent_pkg_s].append(float("{:.2f}".format(float(i_row[28]))))
            self.data[self.net_received_pkg_s].append(float("{:.2f}".format(float(i_row[29]))))

            #self.data[self.tcp].append(float("{:.2f}".format(float(i_row[30]))))

            if "kiln" in self.name:
                self.data[self.rewards].append(float("{:.2f}".format(float(i_row[30]))))
                #self.data[self.rewards_beacon_api].append(float("{:.2f}".format(float(i_row[32]))))

                max_number_of_validators = MAX_NUM_VALIDATORS
                if self.data[self.timestamp][-1] < VALIDATOR_CHANGE_TIME:
                    max_number_of_validators = MAX_NUM_VALIDATORS_10
                new_incorrect_head = int(i_row[31])
                new_incorrect_source = int(i_row[33])

                if len(self.data[self.num_validators]) == 0:
                    self.data[self.num_validators].append(1)
                
                else:
                    if max_number_of_validators - new_incorrect_source > self.data[self.num_validators][-1]:
                        self.data[self.num_validators].append(max_number_of_validators - new_incorrect_source)
                    else:
                        self.data[self.num_validators].append(self.data[self.num_validators][-1])
                #print(self.name, max_number_of_validators - new_incorrect_source)  
                    #print(self.data[self.num_validators][-1], self.data[self.incorrect_heads][-1])
                    
                    #print(max_number_of_validators - new_incorrect_head, self.data[self.num_validators][-1])
                new_number_validators = self.data[self.num_validators][-1]
                vals_overflow = max_number_of_validators - new_number_validators

                self.data[self.incorrect_heads].append(new_incorrect_head - vals_overflow)
                self.data[self.incorrect_heads_prcnt].append(float(self.data[self.incorrect_heads][-1] / self.data[self.num_validators][-1]) * 100)

                self.data[self.incorrect_sources].append(new_incorrect_source - vals_overflow)
                self.data[self.incorrect_sources_prcnt].append(float(self.data[self.incorrect_sources][-1] / self.data[self.num_validators][-1]) * 100)
                #self.data[self.max_rewards].append(float(i_row[34]))
                    
                
                # # if (self.data[self.incorrect_heads_prcnt][-1] > 100):
                # #    print(self.data[self.timestamp][-1], self.data[self.incorrect_heads][-1], self.data[self.num_validators][-1])
                # # print(self.data[self.incorrect_heads][-1], self.data[self.num_validators][-1])


                # # print(new_incorrect_head)
                # if len(self.data[self.num_validators]) == 0:
                #     self.data[self.num_validators].append(MAX_NUM_VALIDATORS - new_incorrect_head)
                #     # print(self.data[self.num_validators][-1])
                # else:
                #     new_validators_number = MAX_NUM_VALIDATORS - new_incorrect_head
                #     #print(new_validators_number)
                #     #print(self.data[self.num_validators][-1])
                #     if new_validators_number >  self.data[self.num_validators][-1]:
                #         self.data[self.num_validators].append(new_validators_number)
                #     else:
                #         self.data[self.num_validators].append(self.data[self.num_validators][-1])
                # # print(self.data[self.num_validators][-1])
        
        
    
# checks if the specified name exists in an array of ClientData objects
# returns the index of the specified client name in case of found.
# Otherwise, return -1

def average_of_rows(rows):
    
    if len(rows) == 0:
        print("No rows to average")
        return
    
    if len(rows) == 1:
        print("Only one row to average")
        return row[0
    ]

    number_of_rows = len(rows)
    

    length = len(rows[0])
    for row in rows:
        if len(row) != length:
            print("Some row is different size!")
    
    result_row = rows.pop(0)

    for row in rows:

        for idx, item in enumerate(row):
            if type(item) == type(str("")):
                # if it is a string, cannot average
                continue
            
            if type(item) == type(datetime.datetime.now().timestamp()):
                # maintain the timestamp
                continue
        
        result_row[idx] += item
    
    for idx, item in enumerate(result_row):
        if type(item) == type(float(0.0)) or type(item) == type(int(0)):
            result_row[idx] = item / number_of_rows

    return result_row

        

def check_clientName_exists(input_str, input_client_array):

        for idx, client in enumerate(input_client_array):
            if client.name == input_str:
                return idx
        
        return -1


def import_from_file(i_file, client_object_array):
    # open the file containing the data
    with open(i_file,'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        row_counter = 0
        
        for row in csv_reader:

            row_counter = row_counter + 1
            if row_counter == 1:
                # this is the title row
                continue
            
            client_pid = row[0]
            client_name = row[1]
            
            # get the position in our array to identify the client
            client_index = check_clientName_exists(client_name, client_object_array)
            
            if client_index == -1:
                # this means we need to add the client object to the array
                # this client did not exist in our array
                client_object_array.append(ClientData(client_pid, client_name))
            
            # there is already an object for the specified client where to add the data

            client_object_array[client_index].add_row(row)
        


PlotMetadata = {
    'disk': {'legend': "disk", 'graphTitle': "Disk_Usage", 'yLabel': "Disk Usage in GB", 'data_index': ClientData.disk_usage},
    'cpu': {'legend': "cpu", 'graphTitle': "CPU Usage", 'yLabel': "CPU %", 'data_index': ClientData.cpu_usage},
    'mem': {'legend': "mem", 'graphTitle': "MEM Usage", 'yLabel': "Memory [MB]", 'data_index': ClientData.mem_usage},
    'netSent': {'legend': "Net Sent", 'graphTitle': "Network Sent", 'yLabel': "Net Sent [GB]", 'data_index': ClientData.net_sent},
    'netReceived': {'legend': "Net Received", 'graphTitle': "Network Received", 'yLabel': "Net Received [GB]", 'data_index': ClientData.net_received},
    'slot': {'legend': "slot", 'graphTitle': "Slot", 'yLabel': "Slot", 'data_index': ClientData.current_slot},
    'peers': {'legend': "peers", 'graphTitle': "Peers", 'yLabel': "Peer number", 'data_index': ClientData.current_peers},

    'memPrcnt': {'legend': "Memory %", 'graphTitle': "Percentage of memory used", 'yLabel': "Mem %", 'data_index': ClientData.mem_percentage},

    'cpu60s': {'legend': "cpu 60 seconds", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu60},
    'cpu300s': {'legend': "cpu 300 seconds", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu300},
    'cpu900s': {'legend': "cpu 900 seconds", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu900},

    'cpu_0': {'legend': "core 0", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu_0},
    'cpu_1': {'legend': "core 1", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu_1},
    'cpu_2': {'legend': "core 2", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu_2},
    'cpu_3': {'legend': "core 3", 'graphTitle': "CPU consumption", 'yLabel': "CPU %", 'data_index': ClientData.cpu_3},

    'node_disk_usage': {'legend': "disk use", 'graphTitle': "Disk Usage", 'yLabel': "MB", 'data_index': ClientData.disk_node_mb},
    'node_disk_usage_prcnt': {'legend': "disk use", 'graphTitle': "Disk Usage", 'yLabel': "Disk %", 'data_index': ClientData.disk_node_prcnt},

    'io_write_mb_s': {'legend': "IO Writes MB", 'graphTitle': "Disk Write MB/s", 'yLabel': "MB/s", 'data_index': ClientData.io_write_mb_s},
    'io_read_mb_s': {'legend': "IO Reads MB", 'graphTitle': "Disk Read MB/s", 'yLabel': "MB/s", 'data_index': ClientData.io_read_mb_s},

    'io_write_op_s': {'legend': "IO Writes Operations", 'graphTitle': "Disk Write Op/s", 'yLabel': "Op/s", 'data_index': ClientData.io_write_op_s},
    'io_read_op_s': {'legend': "IO Reads Operations", 'graphTitle': "Disk Read Op/s", 'yLabel': "Op/s", 'data_index': ClientData.io_read_op_s},

    'io_write_prcnt': {'legend': "IO Writes Percentage", 'graphTitle': "Disk Write Percentage", 'yLabel': "Bandwidth %", 'data_index': ClientData.io_write_op_s},
    'io_read_prcnt': {'legend': "IO Reads Percentage", 'graphTitle': "Disk Read Percentage", 'yLabel': "Bandwidth %", 'data_index': ClientData.io_read_op_s},
    
    'netSentMBS': {'legend': "Net Sent Ratio", 'graphTitle': "Network Out Ratio", 'yLabel': "MB/s", 'data_index': ClientData.net_sent_mb_s},
    'netReceivedMBS': {'legend': "Net Received Ratio", 'graphTitle': "Network In Ratio", 'yLabel': "MB/s", 'data_index': ClientData.net_received_mb_s},
    
    'netSentPackS': {'legend': "Net Sent Ratio", 'graphTitle': "Network Out Ratio", 'yLabel': "Pkg/s", 'data_index': ClientData.net_sent_pkg_s},
    'netReceivedPackS': {'legend': "Net Received Ratio", 'graphTitle': "Network In Ratio", 'yLabel': "Pkg/s", 'data_index': ClientData.net_received_pkg_s},
    
    'tcp': {'legend': "TCP", 'graphTitle': "TCP", 'yLabel': "TCP", 'data_index': ClientData.tcp},
    'rewards': {'legend': "Rewards", 'graphTitle': "Rewards per Epoch", 'yLabel': "Gwei", 'data_index': ClientData.rewards},
    'max_rewards': {'legend': "Max Rewards", 'graphTitle': "Max Rewards per Epoch", 'yLabel': "Gwei", 'data_index': ClientData.max_rewards},
    'beacon_api_rewards': {'legend': "Beacon API Rewards", 'graphTitle': "Rewards per Epoch (Beacon API)", 'yLabel': "Gwei", 'data_index': ClientData.rewards_beacon_api},
    'validator_num': {'legend': "validators", 'graphTitle': "Number of validators", 'yLabel': "Validators", 'data_index': ClientData.num_validators},
    'incorrect_heads': {'legend': "incorect heads", 'graphTitle': "Number of incorrect heads", 'yLabel': "Incorrect Heads", 'data_index': ClientData.incorrect_heads},
    'incorrect_heads_prcnt': {'legend': "incorrect heads %", 'graphTitle': "Percentage of incorrect heads", 'yLabel': "Percentage of incorrect heads", 'data_index': ClientData.incorrect_heads_prcnt},
    'incorrect_sources': {'legend': "incorrect sources", 'graphTitle': "Number of incorrect sources", 'yLabel': "Incorrect Sources", 'data_index': ClientData.incorrect_sources},
    'incorrect_sources_prcnt': {'legend': "incorrect sources %", 'graphTitle': "Percentage of incorrect sources", 'yLabel': "Percentage of incorrect Sources", 'data_index': ClientData.incorrect_sources_prcnt},

    'cpu_cores': {'legend': "core", 'graphTitle': "CPU cores", 'yLabel': "Use %", 'data_index': ClientData.cpu_0},
    'cpu_intervals': {'legend': "interval", 'graphTitle': "CPU Intervals", 'yLabel': "Use %", 'data_index': ClientData.cpu60}
}

"""
Return the indexes of the timestamp_array_2 that are closer to each of the timestamp_array_1 items.
We assume these arrays are ordered

"""
def find_nearest_spots(array_1, array_2):


    array_2_index = 0
    new_delta = abs(array_1[0] - array_2[array_2_index])
    result = []
    for tmp_value in array_1:
        
        delta = abs(tmp_value - array_2[array_2_index])
        new_delta = delta
        while (new_delta <= delta or array_2[array_2_index] < array_2[array_2_index-1]) and array_2_index < len(array_2)-1: # iterate until we find a greater delta
            array_2_index = array_2_index + 1
            delta = new_delta
            new_delta = abs(tmp_value - array_2[array_2_index])
            
        result.append(array_2_index-1)
        if array_2_index > 0:
            array_2_index = array_2_index - 1
    return result

def readjust_array(i_array):
    result = []

    for item in i_array:
        result.append(item-i_array[0])

    return result

# i_interval ==> the interval we want to measure
# line_interval ==> the seconds between each line

def do_ratio(i_array, i_interval, line_interval):
    # result = []
    # line_number_difference = int(i_interval / line_interval)
    # if i_interval <= line_interval:
    #         line_number_difference = 1

    # for idx, item in enumerate(i_array):
    #     previous_compare_line = max(0, idx-line_number_difference)
    #     difference = item-i_array[previous_compare_line]
    #     print(difference, item, " - ", i_array[previous_compare_line], line_number_difference)
    #     if i_interval <= line_interval:
    #         difference = difference / i_interval
    #     result.append(difference)
    result = [0]
    aggregation = 0
    secs = 0
    for idx, item in enumerate(i_array):
        if idx == 0:
            continue
        new_interval = line_interval
        new_aggregation = float((item - i_array[idx-1]) / line_interval)

        aggregation += item - i_array[idx-1]
        secs += int(new_interval)
        result.append((item - i_array[idx-1]) / line_interval)
    
    print("Aggregation: ", aggregation)
    print("Hours: ", int(secs)/3600)

    return result


def item_in_array(lookup_value, array):
    for item in array:
        if item == lookup_value:
            return True
    return False

class Plot():
    def __init__(self, i_config_obj, i_section):
        self.colorChooser = ColorQueue(0)
        self.second_colorChooser = ColorQueue(3)

        self.section = i_section
        
        self.plotList = []
        self.import_metrics(i_config_obj)
        
        # self.fig, (self.ax, self.ax2) = plt.subplots(1, 2)

        self.x_array = [] # array of data
        self.x_labels = [] # array of data stringified
        self.plot_data = []
        self.second_plot_data = []
    
    def setXlabel(self, input_label):
        self.ax.set_xlabel(input_label, fontsize=12)

        if self.xaxis_mode == "date":
            start_date = datetime.datetime.utcfromtimestamp(self.x_array[0]).strftime("%d/%m-%H:%M:%S")
            self.ax.set_xlabel(input_label + " (since " + start_date + ")", fontsize=12)

        self.ax.xaxis.set_major_locator(plt.MaxNLocator(MAX_MAJOR_TICKS))

        if self.xaxis_mode == "slot":
            self.ax.ticklabel_format(axis='x', style='plain', scilimits=(-3, 3), useMathText=True)

    def finish_plot(self):
        self.ax.grid(axis='y')
        self.ax.grid(axis='x')

        yLabel_color = "#000"
        #if self.second_metricName is not "":
        #    yLabel_color = colorMap[i_client_obj.name]
        
        self.ax.set_ylabel(self.yLabel, color=yLabel_color)
        #self.ax.set_yscale('log')

        # self.ax.set_title(self.graphTitle)
        self.fig.suptitle(self.graphTitle, fontsize=16)
        
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.set_ylim([self.min_y_value, self.max_y_value])

        second_yLabel_color = "#000"
        #if self.second_metricName != "":
        #    second_yLabel_color = secondColorMap['prysm']

        # slot time utilisation
        # self.ax.xaxis.set_ticks(np.arange(self.x_labels[0], self.x_labels[-1], 12.0))

        if self.second_data_index != -1:
            self.ax2.set_ylabel(self.second_yLabel, color=second_yLabel_color)
            self.ax2.set_ylim([self.min_second_y_value, self.max_second_y_value])

        if len(self.vertical_line) != 0:
            for line in self.vertical_line:
                self.ax.axvline(x=int(line), color="#ce1e16", linestyle="--")
                #self.ax.axvline(x=int(line), color=self.vertical_line_colors.pop(0), linestyle="--")

        if len(self.horizontal_line) != 0:
            for line in self.horizontal_line:
                self.ax2.axhline(y=int(line), color="#ce1e16", linestyle="--")
        
        
        self.do_legend()

        plt.tight_layout()
        #self.ax.tick_params(axis="x", which="both", rotation=45)
        # plt.show()
        print("Saving figure into: ", self.storePath)
        dirname = os.path.dirname(self.storePath)
        isExist = os.path.exists(dirname)

        if not isExist:
        # Create a new directory because it does not exist 
            os.makedirs(dirname)
        plt.savefig(self.storePath)

        print("Close Plot")
        plt.close(self.fig)
        self.fig.clf()
        plt.close("all")

    def do_legend(self):
        handles,labels = [],[]
        for ax in self.fig.axes:
            for h,l in zip(*ax.get_legend_handles_labels()):
                handles.append(h)
                labels.append(l)
        self.ax.legend(handles,labels, loc=self.legendLocation, fontsize= 'x-small', markerscale=5/self.markerSize)

    def calculate_xArray(self, i_startValue, i_maxValue, date_mode = False):
        stepSize = (i_maxValue - i_startValue)
        
        stepSize = max(stepSize / self.num_of_ticks, 1) # step Size / jump size for plotting

        # only for small amounts of data, slot time utilisation
        # if date_mode:
        #     stepSize = stepSize / self.num_of_ticks
        self.stepSize = stepSize
        print("Step:", self.stepSize)
        self.x_array = np.arange (i_startValue, i_maxValue, stepSize)
        print("Array X: ", i_startValue, i_maxValue)
    
    def plot(self, i_ax, i_x_labels, i_plot_data, i_label, i_color, i_marker, i_type = 'line'):
        if i_type == 'line':
            i_ax.plot(i_x_labels, i_plot_data, label=i_label, color=i_color)
        
        elif i_type == 'scatter':
            i_ax.plot(i_x_labels, i_plot_data, label=i_label, marker=i_marker, markersize=self.markerSize, linestyle='None', color=i_color)

    # i_x_index = the array from the client obj to use as x (usually seqNumber or timestamp or currentSlot)
    def add_plot_data(self, i_client_obj, i_x_index, client_index):
        
        data_indices = find_nearest_spots(self.x_array, i_client_obj.data[i_x_index])

        self.plot_data.append([])
        self.second_plot_data.append([])
        
        for item in data_indices:
            self.plot_data[-1].append(i_client_obj.data[self.data_index][item])
            # in case a second plot
            if self.second_data_index != -1:
                self.second_plot_data[-1].append(i_client_obj.data[self.second_data_index][item])

        if self.data_index == ClientData.net_received or self.data_index == ClientData.net_sent:
            self.plot_data[-1] = readjust_array(self.plot_data[-1])

        if self.ratio == "yes":
            self.plot_data[-1] = do_ratio(self.plot_data[-1], self.ratio_interval, self.secs_interval * self.stepSize)
        

        self.plot(self.ax, self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, self.colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)
 
        if self.second_data_index != -1:
            color = self.second_colorChooser.obtain_next_color(i_client_obj.name)
            if self.secondPlotType == "scatter":
                color = self.colorChooser.obtain_next_color(i_client_obj.name)
            
            if self.second_data_index == ClientData.net_received or self.second_data_index == ClientData.net_sent:
                 self.second_plot_data[-1] = readjust_array(self.second_plot_data[-1])

            if self.second_ratio != "":
                self.second_plot_data[-1] = do_ratio(self.second_plot_data[-1], self.ratio_interval, self.secs_interval)

            self.plot(self.ax2, self.x_labels, self.second_plot_data[-1], i_client_obj.name + " " + self.second_legend, color, self.marker[client_index], self.secondPlotType)

        
    def import_metrics(self, config_obj):

        self.metricName = str(config_obj.get(self.section, "METRIC_NAME"))
        if "," in self.metricName:
            self.metricName = str(config_obj.get(self.section, "METRIC_NAME")).split(",")
        
        self.ratio = ""
        if config_obj.has_option(self.section,"RATIO"):
            self.ratio = str(config_obj.get(self.section, "RATIO"))
        
        self.plotType = str(config_obj.get(self.section, "PLOT_TYPE")) 

        self.second_metricName = str(config_obj.get(self.section, "SECOND_METRIC_NAME"))
        if "," in self.second_metricName:
            self.second_metricName = str(config_obj.get(self.section, "SECOND_METRIC_NAME")).split(",")

        self.second_ratio = ""
        if config_obj.has_option(self.section,"SECOND_RATIO"):
            self.second_ratio = str(config_obj.get(self.section, "SECOND_RATIO"))

        self.secondPlotType = str(config_obj.get(self.section, "SECOND_PLOT_TYPE")) 
        
        self.num_of_ticks = int(config_obj.get(self.section, "NUM_OF_POINTS")) 

        self.initial_timestamp = datetime.datetime.strptime("01/01/2022 00:00:00", '%d/%m/%Y %H:%M:%S').timestamp()
        if config_obj.has_option(self.section,"INITIAL_DATE"):
            self.initial_timestamp = datetime.datetime.strptime(config_obj.get(self.section, "INITIAL_DATE"), '%d/%m/%Y %H:%M:%S').timestamp() #print("Initial timestamp: " + str(num_of_ticks))
        self.secs_interval = int(config_obj.get(self.section, "INTERVAL_SECS")) 
        
        self.ratio_interval = self.secs_interval
        if config_obj.has_option(self.section,"RATIO_INTERVAL"):
            self.ratio_interval = int(config_obj.get(self.section, "RATIO_INTERVAL"))

        self.xaxis_mode = str(config_obj.get(self.section, "XAXIS"))
        if self.xaxis_mode != "seq":
            self.secs_interval = 1 
        self.start_x = float(config_obj.get(self.section, "START_X")) 
        
        self.min_y_value = int(config_obj.get(self.section, "MIN_Y_VALUE")) 
        self.max_y_value = float(config_obj.get(self.section, "MAX_Y_VALUE")) 
        self.min_second_y_value = int(config_obj.get(self.section, "MIN_SECOND_Y_VALUE"))
        self.max_second_y_value = int(config_obj.get(self.section, "MAX_SECOND_Y_VALUE"))
        
        self.client_allowlist = str(config_obj.get(self.section, "CLIENT_ALLOWLIST")).split(",")

        self.storePath = str(config_obj.get(self.section, "STORE_PATH"))
        self.legendLocation = "upper left"
        if config_obj.has_option(self.section,"LEGEND_LOCATION"):
            self.legendLocation = str(config_obj.get(self.section, "LEGEND_LOCATION"))

        self.maxX = 0
        if config_obj.has_option(self.section,"END_X"):
            self.maxX = float(config_obj.get(self.section, "END_X"))

        self.plotMode = 1
        if config_obj.has_option(self.section,"PLOT_MODE"):
            self.plotMode = int(config_obj.get(self.section, "PLOT_MODE"))
        
        self.marker = [".",".",".",".",".",".",".",".",".",".","."]
        if config_obj.has_option(self.section,"MARKER"):
            self.marker  = str(config_obj.get(self.section, "MARKER")).split(",")

        self.markerSize = float(0.1)
        if config_obj.has_option(self.section,"MARKER_SIZE"):
            self.markerSize = float(config_obj.get(self.section, "MARKER_SIZE"))

        self.vertical_line = []
        if config_obj.has_option(self.section,"VERTICAL_LINE"):
            self.vertical_line = (config_obj.get(self.section, "VERTICAL_LINE")).split(",")
        
        self.horizontal_line = []
        if config_obj.has_option(self.section,"HORIZONTAL_LINE"):
            self.horizontal_line = config_obj.get(self.section, "HORIZONTAL_LINE").split(",")
        
        self.vertical_line_colors = []
        if config_obj.has_option(self.section,"VERTICAL_LINE_COLORS"):
            self.vertical_line_colors = config_obj.get(self.section, "VERTICAL_LINE_COLORS").split(",")
        
        # self.legenLabel = str(config_obj.get(self.section, "LABEL"))

        # 0 for DiskUsage, 1 for CPUUsage, 2 for MemUSage
        if type(self.metricName) != type([]):
            self.setMetadata()

    def setMetadata(self):
        self.yLabel = ""
        self.second_yLabel = ""
        self.graphTitle = ""
        self.data_index = -1
        self.second_data_index =-1
        
        if self.metricName in PlotMetadata:
            self.legend = PlotMetadata[self.metricName]['legend']
            self.graphTitle = PlotMetadata[self.metricName]['graphTitle']
            self.yLabel = PlotMetadata[self.metricName]['yLabel']
            self.data_index = PlotMetadata[self.metricName]['data_index']
        else:
            print("Unknown metric type.")
            exit(0)
        
        if self.ratio == "yes":
            self.legend += "/s"
            self.yLabel += "/s"
            self.graphTitle += " Ratio"
        
        if self.second_metricName in PlotMetadata:
            self.second_legend = PlotMetadata[self.second_metricName]['legend']
            self.graphTitle = self.graphTitle + " vs " + PlotMetadata[self.second_metricName]['graphTitle']
            self.second_yLabel = PlotMetadata[self.second_metricName]['yLabel']
            self.second_data_index = PlotMetadata[self.second_metricName]['data_index']

class OnePlot(Plot):
    def __init__(self, i_config_obj, i_section):
        super().__init__(i_config_obj, i_section)
        self.fig, self.ax = plt.subplots()
        
        if self.second_metricName != "":
            self.ax2 = self.ax.twinx()


class TwoSubPlotsbyMetric(Plot):

    def __init__(self, i_config_obj, i_section):
        super().__init__(i_config_obj, i_section)
        self.fig, (self.ax, self.ax2) = plt.subplots(1, 2, figsize=(10,6))
        self.ax2.grid(axis='y')
        self.ax2.grid(axis='x')
        self.second_colorChooser = ColorQueue(0)

    def setXlabel(self, input_label):
        self.ax.set_xlabel(input_label, fontsize=12)
        self.ax2.set_xlabel(input_label, fontsize=12)

        self.ax.xaxis.set_major_locator(plt.MaxNLocator(MAX_MAJOR_TICKS))
        self.ax2.xaxis.set_major_locator(plt.MaxNLocator(MAX_MAJOR_TICKS))

        if self.xaxis_mode == "slot":
            self.ax.ticklabel_format(axis='x', style='plain', scilimits=(-3, 3), useMathText=True)
            self.ax2.ticklabel_format(axis='x', style='plain', scilimits=(-3, 3), useMathText=True)
    
    def do_legend(self):
        self.ax.legend(loc=self.legendLocation, fontsize= 'small', markerscale=5/self.markerSize)
        self.ax2.legend(loc=self.legendLocation, fontsize= 'small', markerscale=5/self.markerSize)
        self.ax2.set_xlabel(self.ax.get_xlabel(), fontsize=12)
        print(self.ax.get_xlabel())

# one subplot per client
class SeveralSubPlots(Plot):
    def __init__(self, i_config_obj, i_section):
        super().__init__(i_config_obj, i_section)
        number_clients = len(self.client_allowlist)
        self.fig, self.ax_array = plt.subplots(number_clients)

        if self.second_metricName != "":
            self.ax2_array = []
            for ax in self.ax_array:
                self.ax2_array.append(ax.twinx())

    def setXlabel(self, input_label):

        for ax in self.ax_array:
            ax.set_xlabel(input_label, fontsize=12)
            ax.xaxis.set_major_locator(plt.MaxNLocator(MAX_MAJOR_TICKS))
            if self.xaxis_mode == "slot":
                ax.ticklabel_format(axis='x', style='plain', scilimits=(-3, 3), useMathText=True)
    
    def finish_plot(self):

        for idx, ax in enumerate(self.ax_array):
            ax.grid(axis='y')
            ax.grid(axis='x')

            yLabel_color = "#000"
            
            ax.set_ylabel(self.yLabel, color=yLabel_color)

            self.fig.suptitle(self.graphTitle, fontsize=16)
            
            ax.xaxis.set_minor_locator(AutoMinorLocator())
            ax.set_ylim([self.min_y_value, self.max_y_value])

            second_yLabel_color = "#000"

            if self.second_data_index != -1:
                self.ax2_array[idx].set_ylabel(self.second_yLabel, color=second_yLabel_color)
                self.ax2_array[idx].set_ylim([self.min_second_y_value, self.max_second_y_value])
        
        self.do_legend()

        plt.tight_layout()
        #self.ax.tick_params(axis="x", which="both", rotation=45)
        #plt.show()
        plt.savefig(self.storePath)

    def do_legend(self):
        for idx, ax in enumerate(self.ax_array):
            ax.legend(loc=self.legendLocation, fontsize= 'small', markerscale=5/self.markerSize)
            if self.second_metricName != "":
                self.ax2_array[idx].legend(loc=self.legendLocation, fontsize= 'small', markerscale=5/self.markerSize)
            #self.ax2.set_xlabel(self.ax.get_xlabel(), fontsize=12)

    # i_x_index = the array from the client obj to use as x (usually seqNumber or timestamp or currentSlot)
    def add_plot_data(self, i_client_obj, i_x_index, client_index):
        
        ax_index = self.client_allowlist.index(i_client_obj.name)

        data_indices = find_nearest_spots(self.x_array, i_client_obj.data[i_x_index])

        self.plot_data.append([])
        self.second_plot_data.append([])
        for item in data_indices:
            self.plot_data[-1].append(i_client_obj.data[self.data_index][item])
            # in case a second plot
            if self.second_data_index != -1:
                self.second_plot_data[-1].append(i_client_obj.data[self.second_data_index][item])
        if type(self.ax_array) == type([]):
            self.plot(self.ax_array[ax_index], self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, self.colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)
        else:
            self.plot(self.ax_array, self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, self.colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)

        if self.second_data_index != -1:
            color = self.second_colorChooser.obtain_next_color(i_client_obj.name)
            if self.secondPlotType == "scatter":
                color = self.colorChooser.obtain_next_color(i_client_obj.name)

            if type(self.ax_array) == type([]):
                self.plot(self.ax2_array[ax_index], self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, color, self.marker[client_index], self.plotType)
            else:
                self.plot(self.ax2_array, self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, color, self.marker[client_index], self.plotType)

# for cpu cores and intervals
class SeveralMetricsinPlot(OnePlot):
    
    def __init__(self, i_config_obj, i_section):
        super().__init__(i_config_obj, i_section)

    # i_x_index = the array from the client obj to use as x (usually seqNumber or timestamp or currentSlot)
    def add_plot_data(self, i_client_obj, i_x_index, client_index):
        
        data_indices = find_nearest_spots(self.x_array, i_client_obj.data[i_x_index])

        original_metric = self.metricName        

        metrics = self.metricName
    
        for metric in metrics:
            self.metricName = metric
            self.setMetadata()
            self.plot_data.append([])
            for item in data_indices:
                self.plot_data[-1].append(i_client_obj.data[self.data_index][item])
                # in case a second plot

            # if self.data_index == ClientData.net_received or self.data_index == ClientData.net_sent:
            #     self.plot_data[-1] = readjust_array(self.plot_data[-1])
            self.plot(self.ax, self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, self.colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)

        self.metricName = original_metric

        if self.second_metricName != "":
            original_second_metricName = self.second_metricName
            second_metrics = self.second_metricName
            
            for metric in second_metrics:
                self.second_metricName = metric
                self.setMetadata()
                self.second_plot_data.append([])
                for item in data_indices:
                    self.second_plot_data[-1].append(i_client_obj.data[self.second_data_index][item])
                    # in case a second plot

                # if self.second_data_index == ClientData.net_received or self.second_data_index == ClientData.net_sent:
                #     self.second_plot_data[-1] = readjust_array(self.second_plot_data[-1])
                self.plot(self.ax2, self.x_labels, self.second_plot_data[-1], i_client_obj.name + " " + self.legend, self.second_colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)

            self.metricName = original_second_metricName

# for cpu cores and intervals
class SeveralMetricsinTwoSubPlots(TwoSubPlotsbyMetric):

    
    def add_plot_data(self, i_client_obj, i_x_index, client_index):
        
        data_indices = find_nearest_spots(self.x_array, i_client_obj.data[i_x_index])

        original_metric = self.metricName        

        metrics = self.metricName
    
        for metric in metrics:
            self.metricName = metric
            self.setMetadata()
            self.plot_data.append([])
            for item in data_indices:
                self.plot_data[-1].append(i_client_obj.data[self.data_index][item])
                # in case a second plot

            # if self.data_index == ClientData.net_received or self.data_index == ClientData.net_sent:
            #     self.plot_data[-1] = readjust_array(self.plot_data[-1])
            self.plot(self.ax, self.x_labels, self.plot_data[-1], i_client_obj.name + " " + self.legend, self.colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)

        self.metricName = original_metric

        if self.second_metricName != "":
            original_second_metricName = self.second_metricName
            second_metrics = self.second_metricName
            
            for metric in second_metrics:
                self.second_metricName = metric
                self.setMetadata()
                self.second_plot_data.append([])
                for item in data_indices:
                    self.second_plot_data[-1].append(i_client_obj.data[self.second_data_index][item])
                    # in case a second plot

                # if self.second_data_index == ClientData.net_received or self.second_data_index == ClientData.net_sent:
                #     self.second_plot_data[-1] = readjust_array(self.second_plot_data[-1])
                self.plot(self.ax2, self.x_labels, self.second_plot_data[-1], i_client_obj.name + " " + self.legend, self.second_colorChooser.obtain_next_color(i_client_obj.name), self.marker[client_index], self.plotType)

            self.metricName = original_second_metricName
    

def main():

    config_files = []
    argv_count = int(1)
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(sys.argv[argv_count]))
    while "config" in config_file:
    # prepare to parse config file
        config_files.append(config_file)
        argv_count += 1
        config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(sys.argv[argv_count]))
    # the current argv is already a data file
    number_of_args = len(sys.argv)
    data_files = []
    for i in range(argv_count, number_of_args, 1):
        data_files.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), str(sys.argv[i])))
        print("Importing " + data_files[-1] + "...")
    client_object_array = []
    for file in data_files:
        import_from_file(file, client_object_array)

    for config_file in config_files:
        config_obj = configparser.ConfigParser()
        # check if file exists and read
        if os.path.isfile(config_file):
            print("Reading config file : ", config_file)
            config_obj.read(config_file)
        else:
            print("Config file not found")
            exit()

        section_number = 1
        section_base_name = "PLOT"
        

        while config_obj.has_section(section_base_name+str(section_number)):
            section = section_base_name+str(section_number)
            section_number = section_number + 1
            
            plot_obj = OnePlot(config_obj, section) # simple plot, all in one
            print("Plot mode: ", plot_obj.plotMode)
            if plot_obj.plotMode == 2:
                plot_obj = TwoSubPlotsbyMetric(config_obj, section) # separate one metric from another in two plots
            if plot_obj.plotMode == 3:
                plot_obj = SeveralSubPlots(config_obj, section) # separate each client in a single subplot, with all the configures metrics
            if type(plot_obj.metricName) == type([]):
                plot_obj = SeveralMetricsinPlot(config_obj, section) # plot several different metrics together
                if type(plot_obj.second_metricName) == type([]):
                    plot_obj = SeveralMetricsinTwoSubPlots(config_obj, section) # plot several different metrics together

            client_object_subarray = []
            
            for client in client_object_array:
                
                if item_in_array(client.name, plot_obj.client_allowlist):
                    client_object_subarray.append(client)

            print("AllowList:", plot_obj.client_allowlist)
            print("Plot List:", [x.name for x in client_object_subarray])   
            if len(client_object_subarray) > 0:
                if plot_obj.xaxis_mode == 'date':
                    
                    minimumDate = max([x.data[ClientData.timestamp][0] for x in client_object_subarray])
                    print("Firs date", datetime.datetime.utcfromtimestamp(minimumDate))
                    minimumDate = minimumDate + (plot_obj.start_x*3600)
                    

                    minimumDate = max(minimumDate, plot_obj.initial_timestamp)
                    print("Min date: ", datetime.datetime.utcfromtimestamp(minimumDate))
                    # calculate the minimum last date
                    maximumDate = min([x.data[ClientData.timestamp][-1] for x in client_object_subarray])
                    if plot_obj.maxX > 0:
                        maximumDate = min(minimumDate + plot_obj.maxX*3600, maximumDate)
                    
                    plot_obj.calculate_xArray(minimumDate, maximumDate, True)

                    
                    
                    print("First X array:", datetime.datetime.utcfromtimestamp(plot_obj.x_array[0]))
                    # plot_obj.x_labels = [float((x - plot_obj.x_array[0])) for x in plot_obj.x_array] # slot time utilisation
                    print("X Array length: ", len(plot_obj.x_array))
                    plot_obj.x_labels = [float((x - plot_obj.x_array[0]) / 3600.0) for x in plot_obj.x_array]
                    # plot_obj.x_labels = [datetime.datetime.utcfromtimestamp(x) for x in plot_obj.x_array]

                    print("First X label", plot_obj.x_labels[0])
                    print("Number of labels", len(plot_obj.x_labels))
                    print("Last label", plot_obj.x_labels[-1])

                    for idx, client in enumerate(client_object_subarray):
                        plot_obj.add_plot_data(client, ClientData.timestamp, idx)
                    
                    #majorTicksFormat = mdates.DateFormatter('%H:%M:%S')
                    #plot_obj.ax.xaxis.set_major_formatter(majorTicksFormat)
                    plot_obj.ax.tick_params(axis='x', labelsize=8)
                    # plot_obj.fig.autofmt_xdate(rotation=30)
                    plot_obj.setXlabel("Hours")
                    # plot_obj.setXlabel("Seconds") # slot time utilisation


                if plot_obj.xaxis_mode == 'seq':
                    
                    maxValue = min([x.data[ClientData.seq_number][-1] for x in client_object_subarray])
                    if plot_obj.maxX > 0:
                        maxValue = min(plot_obj.maxX, maxValue)
                    minValue = max([x.data[ClientData.seq_number][0] for x in client_object_subarray])
                    plot_obj.start_x = max(plot_obj.start_x, minValue)
                    plot_obj.calculate_xArray(plot_obj.start_x, maxValue)
                    plot_obj.x_labels = [plot_obj.secs_interval*(x-plot_obj.x_array[0])/3600 for x in plot_obj.x_array]
                    #plot_obj.x_labels = [plot_obj.secs_interval*(x-plot_obj.x_array[0]) for x in plot_obj.x_array]

                    for idx, client in enumerate(client_object_subarray):
                        plot_obj.add_plot_data(client, ClientData.seq_number, idx)

                    #plot_obj.setXlabel("Seconds")
                    plot_obj.setXlabel("Hours")
                
                if plot_obj.xaxis_mode == 'slot':

                    maxValue = min([x.data[ClientData.current_slot][-1] for x in client_object_subarray])
                    
                    if plot_obj.maxX > 0:
                        maxValue = min(plot_obj.maxX, maxValue)
                    
                    minValue = max([x.data[ClientData.current_slot][0] for x in client_object_subarray])

                    plot_obj.start_x = max(plot_obj.start_x, minValue)
                    plot_obj.calculate_xArray(plot_obj.start_x, maxValue)
                    
                    plot_obj.x_labels = plot_obj.x_array
                    
                    print("X Range: ", plot_obj.x_labels[0], " - ", plot_obj.x_labels[-1])
                    for idx, client in enumerate(client_object_subarray):
                        plot_obj.add_plot_data(client, ClientData.current_slot, idx)

                        #plot_obj.ax.ticklabel_format(axis='x', style='plain', scilimits=(-3, 3), useMathText=True)

                    plot_obj.setXlabel("Slot")


                plot_obj.finish_plot()
        


if __name__ == "__main__":
    main()