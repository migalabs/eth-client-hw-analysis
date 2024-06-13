from base import *


def main():

	lstart_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
	lend_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')

	tmp_time = lstart_time

	while tmp_time < lend_time:
		
		print("Downloading at ", tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
		download_cpu(
			tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		
		# download_cpu_per_second_default(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
		#(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
		#step="1s")
		# download_cpu_per_second_all_topics(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			#(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			#step="1s")

		download_mem(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_mem_without_rss(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		download_net_receive(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_net_receive_packets(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_net_receive_per_second_default(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_net_receive_per_second_all_topics(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		download_net_transmit(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_net_transmit_packets(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		# download_net_transmit_per_second_default(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			#(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			#step="1s")

		download_peers(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		download_fs_read_bytes(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_fs_read_ops(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		download_fs_write_bytes(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")
		download_fs_write_ops(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		download_disk_usage(tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
			step="1s")

		# download_block_proposals()
			
		tmp_time = tmp_time + timedelta(hours=3)


def main_20m():
		# download_cpu()
		# download_cpu_per_second_default()
		# download_cpu_per_second_all_topics()

		# download_mem()
		# download_mem_without_rss()

		# download_net_receive()
		# download_net_receive_packets()
		download_net_receive_per_second_default()
		download_net_receive_per_second_all_topics()

		# download_net_transmit()
		download_net_transmit_packets()
		download_net_transmit_per_second_default()

		# download_peers()

		# download_fs_read_bytes()
		# download_fs_read_ops()

		# download_fs_write_bytes()
		# download_fs_write_ops()

		# download_disk_usage()

		# # download_block_proposals()
	

def download_cpu(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(rate(container_cpu_usage_seconds_total[1m])) 
			/ on(server) group_left() 
				machine_cpu_cores * 100
	"""
	metric_name = 'cpu'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time, step=step)

	data_to_csv(response, metric_name)

def download_cpu_per_second_default(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(increase(node_cpu_seconds_total{{mode!="idle"}}[1m]))
			/ on(server) group_left() 
				machine_cpu_cores * 100
			/ 2
	"""
	metric_name = 'cpu_per_second_default'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, default_time, shift_timestamp(default_time, 3))
	for idx, metric in enumerate(responsestart_time=start_time, end_time=end_time, step=step):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)

def download_cpu_per_second_all_topics(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		sum by 
			(container_label_com_docker_compose_service, container_label_com_docker_compose_project, image, server, project_name) 
		(increase(node_cpu_seconds_total{{mode!="idle"}}[1m]))
			/ on(server) group_left() 
				machine_cpu_cores * 100
			/ 2
	"""
	metric_name = 'cpu_per_second_all_topics'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, all_subnets_time, shift_timestamp(all_subnets_time, 3))
	for idx, metric in enumerate(responsestart_time=start_time, end_time=end_time, step=step):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)



def download_mem(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		container_memory_working_set_bytes / 1024 / 1024 / 1024
	"""

	metric_name = 'mem'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_mem_without_rss(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		(container_memory_working_set_bytes-container_memory_rss) / 1024 / 1024 / 1024
	"""

	metric_name = 'mem_without_rss'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_receive(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		rate(
			container_network_receive_bytes_total[1m]
		) / 1024 / 1024
	"""

	metric_name = 'net_receive'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_net_receive_packets(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		rate(
			container_network_receive_packets_total[1m]
		)
	"""

	metric_name = 'net_receive_packets'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)

def download_net_receive_per_second_default(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		increase(
			node_network_receive_bytes_total{{device="ens3"}}[2s]
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


def download_net_receive_per_second_all_topics(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		increase(
			node_network_receive_bytes_total{{device="ens3"}}[2s]
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


def download_net_transmit(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		rate(
			container_network_transmit_bytes_total[1m]
		) / 1024 / 1024
	"""

	metric_name = 'net_transmit'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_net_transmit_per_second_default(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		increase(
			node_network_transmit_bytes_total{{device="ens3"}}[2s]
		) / 1024 / 1024 / 2
	"""
	metric_name = 'net_transmit_per_second_default'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, default_time, shift_timestamp(default_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric
	data_to_csv(response, metric_name)


def download_net_transmit_per_second_all_topics(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		increase(
			node_network_transmit_bytes_total{{device="ens3"}}[2s]
		) / 1024 / 1024 / 2
	"""
	metric_name = 'net_transmit_per_second_all_topics'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range(query, all_subnets_time, shift_timestamp(all_subnets_time, 3))
	for idx, metric in enumerate(response):
		ip = metric["metric"]["server"]
		metric["metric"]["image"] = cl_ip[str(ip)]
		response[idx] = metric

	data_to_csv(response, metric_name)

def download_net_transmit_packets(start_time=start_time, end_time=end_time, step=step):
	query = f"""
		rate(
			container_network_transmit_packets_total[1m]
		)
	"""

	metric_name = 'net_receive_packets'
	print(f"""Downloading {metric_name} for {phase}...""")

	response = ask_range_with_step(query, start_time, end_time)

	data_to_csv(response, metric_name)


def download_peers(start_time=start_time, end_time=end_time, step=step):
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


def download_fs_read_bytes(start_time=start_time, end_time=end_time, step=step):
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


def download_fs_write_bytes(start_time=start_time, end_time=end_time, step=step):
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

def download_fs_read_ops(start_time=start_time, end_time=end_time, step=step):
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

def download_fs_write_ops(start_time=start_time, end_time=end_time, step=step):
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


def download_disk_usage(start_time=start_time, end_time=end_time, step=step):
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

def download_block_proposals(start_time=start_time, end_time=end_time, step=step):

	metric_name = 'block_proposals'

	query = f"""
		select *
		from t_score_metrics
		where (f_slot/32) > {start_epoch} and (f_slot/32) < {end_epoch}
	"""

	print(f"""Downloading {metric_name} for {phase}...""")
	psql_query_to_csv(query, metric_name)

# def download_by_intervals(start_time=start_time, end_time=end_time, step=step):
# 	start_time = datetime.strptime(i_start_time, '%Y-%m-%dT%H:%M:%SZ')
# 	end_time = datetime.strptime(i_end_time, '%Y-%m-%dT%H:%M:%SZ')

# 	tmp_time = start_time
# 	total_response = []

# 	while tmp_time < end_time:
# 		print("Downloading at ", tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
# 		download_cpu(
# 			tmp_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
# 			(tmp_time + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ"),
# 			step="1s")
# 		tmp_time = tmp_time + timedelta(hours=3)
# 	return total_response
# 


if __name__ == "__main__":
	main_20m()