
# cpu

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_cpu.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_cpu.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_cpu.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv


# mem

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_mem.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_mem.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_mem.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv



# disk

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_disk.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config*.ini ../data/raspberry/NE_*.csv


# netReceived

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_netReceived.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netReceived.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_netReceived.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv


# netSent 

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_netSent.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netSent.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_netSent.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv


# peers

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_peers.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_peers.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_peers.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv


# slot 

python3 ../plot_data.py ../configs/raspberry/python/config_plot_all_slot.ini ../data/raspberry/sample*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_slot.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/PvsNE/config_plot_all_slot.ini ../data/raspberry/sample*.csv ../data/raspberry/NE_*.csv


# EF

python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_cpu_cores.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_cpu_intervals.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_mem_prcnt.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_disk_mb_s_write.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_disk_mb_s_read.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_disk_op_s_write.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_disk_op_s_read.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netSent_mb_s.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netReceived_mb_s.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_slot_s.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_slot_s_altair.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netSent_pkg_s.ini ../data/raspberry/NE_*.csv
python3 ../plot_data.py ../configs/raspberry/NE/config_plot_all_netReceived_pkg_s.ini ../data/raspberry/NE_*.csv