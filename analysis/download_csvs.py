from base import *


def main():
	# download_cpu()
	# # download_cpu_per_second_default()
	# # download_cpu_per_second_all_topics()

	# download_mem()
	# download_mem_without_rss()

	# download_net_receive()
	# download_net_receive_packets()
	# # download_net_receive_per_second_default()
	# # download_net_receive_per_second_all_topics()

	# download_net_transmit()
	# download_net_transmit_packets()
	# # download_net_transmit_per_second_default()

	# download_peers()

	# download_fs_read_bytes()
	# download_fs_read_ops()

	# download_fs_write_bytes()
	# download_fs_write_ops()

	# download_disk_usage()

	download_block_proposals()

	

def download_cpu():
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(rate(container_cpu_usage_seconds_total[1m])) 
			/ on(server) group_left() 
				machine_cpu_cores * 100
	"""
	metric_name = 'cpu'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_cpu_per_second_default():
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(increase(node_cpu_seconds_total{{mode!="idle"}}[2s]))
			/ on(server) group_left() 
				machine_cpu_cores * 100
			/ 2
	"""
	metric_name = 'cpu_per_second_default'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, default_time, shift_timestamp(default_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)

def download_cpu_per_second_all_topics():
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(increase(node_cpu_seconds_total{{mode!="idle"}}[2s]))
			/ on(server) group_left() 
				machine_cpu_cores * 100
			/ 2
	"""
	metric_name = 'cpu_per_second_all_topics'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, all_subnets_time, shift_timestamp(all_subnets_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)



def download_mem():
	query = f"""
		container_memory_working_set_bytes / 1024 / 1024 / 1024
	"""

	metric_name = 'mem'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_mem_without_rss():
	query = f"""
		(container_memory_working_set_bytes-container_memory_rss) / 1024 / 1024 / 1024
	"""

	metric_name = 'mem_without_rss'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_receive():
	query = f"""
		rate(
			container_network_receive_bytes_total[1m]
		) / 1024 / 1024
	"""

	metric_name = 'net_receive'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_net_receive_packets():
	query = f"""
		rate(
			container_network_receive_packets_total[1m]
		)
	"""

	metric_name = 'net_receive_packets'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_receive_per_second_default():
	query = f"""
		increase(
			node_network_receive_bytes_total[2s]
		) / 1024 / 1024 / 2
	"""
	metric_name = 'net_receive_per_second_default'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, default_time, shift_timestamp(default_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric
	data_to_csv(response, metric_name)


def download_net_receive_per_second_all_topics():
	query = f"""
		increase(
			node_network_receive_bytes_total[2s]
		) / 1024 / 1024 / 2
	"""
	metric_name = 'net_receive_per_second_all_topics'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, all_subnets_time, shift_timestamp(all_subnets_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)


def download_net_transmit():
	query = f"""
		rate(
			container_network_transmit_bytes_total[1m]
		) / 1024 / 1024
	"""

	metric_name = 'net_transmit'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_transmit_packets():
	query = f"""
		rate(
			container_network_transmit_packets_total[1m]
		)
	"""

	metric_name = 'net_transmit_packets'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_transmit_per_second_default():
	query = f"""
		rate(
			container_network_transmit_bytes_total[2s]
		) / 1024 / 1024
	"""
	metric_name = 'net_transmit_per_second_default'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, default_blocks_time, "2024-02-12T15:33:59Z")

	data_to_csv(response, metric_name)


def download_peers():
	query = f"""
		libp2p_peers
	"""

	metric_name = 'peers'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	# Prysm
	query = f"""
		sum by (job)
		(connected_libp2p_peers)
	"""

	print(f"""Downloading {metric_name} for {phase}...""")

	response2 = ask_range_with_step(query, start_time, end_time)

	response += response2

	data_to_csv(response, metric_name)


def download_fs_read_bytes():
	query = f"""
		sum by (
			container_label_com_docker_compose_config_hash, 
			container_label_com_docker_compose_project, 
			container_label_com_docker_compose_service, 
			image, 
			project_name, 
			server) 
     	(rate(
			container_fs_reads_bytes_total[5m]) / 1024) != 0
	"""

	metric_name = 'fs_read_bytes'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_fs_write_bytes():
	query = f"""
		sum by (
			container_label_com_docker_compose_config_hash, 
			container_label_com_docker_compose_project, 
			container_label_com_docker_compose_service, 
			image, 
			project_name, 
			server) 
     	(rate(
			container_fs_writes_bytes_total[5m]) / 1024) != 0
	"""

	metric_name = 'fs_write_bytes'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_fs_read_ops():
	query = f"""
		sum by (
			container_label_com_docker_compose_config_hash, 
			container_label_com_docker_compose_project, 
			container_label_com_docker_compose_service, 
			image, 
			project_name, 
			server) 
     	(rate(
			container_fs_reads_total[1m])) != 0
	"""

	metric_name = 'fs_read_ops'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_fs_write_ops():
	query = f"""
		sum by (
			container_label_com_docker_compose_config_hash, 
			container_label_com_docker_compose_project, 
			container_label_com_docker_compose_service, 
			image, 
			project_name, 
			server) 
     	(rate(
			container_fs_writes_total[1m])) != 0
	"""

	metric_name = 'fs_write_ops'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_disk_usage():
	query = f"""
		(node_filesystem_size_bytes{{mountpoint=~"/mnt/disk"}}-node_filesystem_avail_bytes{{mountpoint=~"/mnt/disk"}})
		/ 1024 / 1024 / 1024
	"""

	metric_name = 'disk_usage'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	for idx, metric in enumerate(response):
		metric["metric"]["image"] = cl_ip[metric["metric"]["server"]]
		response[idx] = metric

	data_to_csv(response, metric_name)

def download_block_proposals():

	metric_name = 'block_proposals'

	query = f"""
		select *
		from t_score_metrics
		where (f_slot/32) > {start_epoch} and (f_slot/32) < {end_epoch}
	"""

	print(f"""Downloading {metric_name} for {phase}...""")
	psql_query_to_csv(query, metric_name)



if __name__ == "__main__":
	main()