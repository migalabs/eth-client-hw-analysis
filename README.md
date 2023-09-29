# eth-client-hw-analysis V1
Repo compiling all the images that came out from our Ethereum Consensus Client's hardware resource analysis 

# Data Plotting
This subfolder contains the tool used to plot the output data from the eth2-client-analyzer.

This tool does not reveal / create / modify any data, it purely reads and represents the collected data into a plot.
This tool has been developed in Python.

Maintained by [MigaLabs](http://migalabs.io)


## Requirements

<strong>This tool has been tested using Python 3.8.10</strong>
It merely needs the Python interpreter to run it and to install the dependencies in the requirements file.

## Launch the Clients

To launch the clients we have developed a repository to automatize running the clients using a docker-compose file. Please refer [here](https://github.com/migalabs/eth2-clients-setup) to discover more about it.


## Configuration Instructions

The Execution command looks like the following:

```
python3 plot_data.py <config-file> csv-files

Example:
python3 plot_data.py configs/config_plot_NEvs_cpu.ini mainnet2/grandine_sample_13300.csv mainnet2/NE_grandine.csv

```
Keep in mind that there are several different keywords we can give as metricType argument:
- "mem" --> Outputs the Memory consumption plot
- "cpu" --> Outputs the CPU consumption plot
- "disk" --> Outputs the Disk Usage plot
- "slot" --> Outputs the slot increase of each client across time
- "peers" --> Outputs the number of peers plot
- "netSent" --> Outputs the network sent bytes ratio plot
- "netReceived" --> Outputs the network receive bytes ratio plot

For the data_file argument, we may input the file we want to read the data from.


Config file

```
[PLOT1]
METRIC_NAME = disk (choose between disk, cpu, mem, slot, peers, netSent, netReceived)
PLOT_TYPE = line (choose between line, scatter)
SECOND_METRIC_NAME = (in case of sencond axis metric)
SECOND_PLOT_TYPE = (choose between line, scatter)
NUM_OF_POINTS = 100 (more points, more definition)
MARKER = +,x,1,2,3,4
MARKER_SIZE = 10
INITIAL_DATE = 11/02/2022 14:21:32
XAXIS = slot (what metric to use as xaxis)
INTERVAL_SECS = 30 (interval between each xtick)
START_X = 0 (in case of shifting the plot)
MIN_Y_VALUE = 0 (adjust y axis)
MAX_Y_VALUE = 120 (adjust y axis)
MIN_SECOND_Y_VALUE = 0 (adjust y axis)
MAX_SECOND_Y_VALUE = 100 (adjust y axis)
CLIENT_ALLOWLIST = NE_Prysm, NE_Lighthouse, NE_Teku, NE_Nimbus, NE_Lodestar, NE_Grandine (clients to include in the plot)
LEGEND_LOCATION = upper left
STORE_PATH = figures/mainnet/disk/sync_grandine_NE
```

## Execution

We have enabled a set of scripts that automatically execute the given plots with the data we collected a year ago. You may refer to the plot_scripts which automatically plot the data for the given csv files.
We have also included the download script, which retrieves data from Prometheus and stores in a CSV file.
This set of plots was used in May 2022 to perform the Resource Analysis V1. 