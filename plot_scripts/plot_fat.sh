
# cpu

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_cpu.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_cpu.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_cpu.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv



# mem

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_mem.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_mem.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_mem.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv



## disk

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_disk.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config*.ini ../data/fat_node_mainnet/NE_*.csv


# netReceived

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_netReceived.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netReceived.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_netReceived.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv


# netSent 
python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_netSent.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netSent.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_netSent.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv


# peers

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_peers.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_peers.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_peers.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv

# slot

python3 ../plot_data.py ../configs/fat_node/python/config_plot_all_slot.ini ../data/fat_node_mainnet/*sample.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_slot.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/PvsNE/config_plot_all_slot.ini ../data/fat_node_mainnet/*sample.csv ../data/fat_node_mainnet/NE_*.csv


# EF
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_cpu_cores.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_cpu_cores_altair.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_cpu_altair.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_cpu_intervals.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_mem.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_mem_prcnt.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_mem_prcnt_altair.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_disk_mb_s_write.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_disk_mb_s_read.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_disk_op_s_write.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_disk_op_s_write_altair.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_disk_op_s_read.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netSent_mb_s.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netReceived_mb_s.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_slot.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_slot_s.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_slot_s_altair.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netSent_pkg_s.ini ../data/fat_node_mainnet/NE_*.csv
python3 ../plot_data.py ../configs/fat_node/NE/config_plot_all_netReceived_pkg_s.ini ../data/fat_node_mainnet/NE_*.csv