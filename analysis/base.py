import sqlalchemy as sa
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from IPython.display import display
import requests
import re
import os
from datetime import datetime, timedelta

colors = pd.Series({
    'prysm': 'red',
    'lighthouse': 'darkblue',
	'lighthouse-exp': 'lightblue',
    'teku': 'orange',
    'nimbus': 'lightgreen',
    'lodestar': 'purple',
	'grandine': 'yellow'
})


################################################################################################
# Run 1
phase = "run1"
genesis_unix_time = 1606824023 		# Constant
start_epoch = 260550  				# Start epoch you want to plot
start_time = "2024-02-02T12:00:23Z"	# Start time from where you want to download into CSV Feb-04-2024 12:00:23 UTC

end_epoch = 266250					# End epoch you want to plot
end_time = "2024-02-27T21:00:23Z"	# End time from where you want to download into CSV
duration = "25d"					# Duration from start to end (download)

default_epoch = 261000  				
default_time = "2024-02-04T12:00:23Z"	

all_subnets_epoch = 261950
all_subnets_time = "2024-02-08T17:20:23Z"

default_blocks_epoch = 262824
default_blocks_time = "2024-02-12T14:33:59Z"

all_subnets_blocks_epoch = 263683
all_subnets_blocks_time = "2024-02-16T10:16:23Z"

end_base_experiment_epoch = 264465
end_base_experiment_time = "2024-02-19T21:36:23Z"

experiment_milestones = [default_time, all_subnets_time, default_blocks_time, all_subnets_blocks_time, end_base_experiment_time]

cl_ip = {
	"xxx.xxx.xxx.xxx": 	"prysm",
	"xxx.xxx.xxx.xxx": 	"lighthouse",
	"xxx.xxx.xxx.xxx": 	"teku",
	"xxx.xxx.xxx.xxx": 	"nimbus",
	"xxx.xxx.xxx.xxx": 	"lodestar",
	"xxx.xxx.xxx.xxx": 		"grandine"
}


################################################################################################

################################################################################################
# Run 2
phase = "run2"
genesis_unix_time = 1606824023 		# Constant
start_epoch = 280768  				# Start epoch you want to plot
start_time = "2024-05-02T08:30:00Z"	# Start time from where you want to download into CSV Feb-04-2024 12:00:23 UTC

default_epoch = 281128  				
default_time = "2024-05-03T23:00:23Z"	

all_subnets_epoch = 281958
all_subnets_time = "2024-05-07T15:31:35Z"

default_blocks_epoch = 283279
default_blocks_time = "2024-05-13T12:33:59Z"

all_subnets_blocks_epoch = 284147
all_subnets_blocks_time = "2024-05-17T09:07:23Z"

end_base_experiment_epoch = 285027
end_base_experiment_time = "2024-05-21T07:00:00Z"

end_epoch = 286402					# End epoch you want to plot
end_time = "2024-05-27T09:39:59Z"	# End time from where you want to download into CSV
duration = "25d"					# Duration from start to end (download)

experiment_milestones = [default_time, all_subnets_time, default_blocks_time, all_subnets_blocks_time, end_base_experiment_time]

cl_ip = {
	"xxx.xxx.xxx.xxx": 	"prysm",
	"xxx.xxx.xxx.xxx": 	"lighthouse",
	"xxx.xxx.xxx.xxx": 	"teku",
	"xxx.xxx.xxx.xxx": 	"nimbus",
	"xxx.xxx.xxx.xxx": 	"lodestar",
	"xxx.xxx.xxx.xxx": 		"grandine"
}

################################################################################################

# Common
network="mainnet"								# Tag
prometheus_ip = "localhost"						# From where to download Prometheus data
project_name = "resource-analysis-v3"			# Tag
step = "20m"									# Step to download data (you might need to increase if too much data: Prometheus allows 11K points)
csv_folder = f"""./{network}/csv/{phase}/"""	# Where to store CSV files (download data)
fig_folder = f"""./{network}/fig/{phase}/"""	# Where to store figures (plots)
epoch_seconds = 384								# Constant


def ask(query_str):
	response = requests.get('http://' + prometheus_ip + ':9099/api/v1/query', params={
		'query': query_str,
		'time': end_time}) 
	response_json = response.json()
	response_data = response_json['data']['result']
	return response_data

def ask_range(query_str, i_start_time, i_end_time):
	result = []
	for port in [9099]:
		response = requests.get('http://' + prometheus_ip + ':' + str(port) + '/api/v1/query_range', params={
			'query': query_str,
			'start': i_start_time,
			'end': i_end_time,
			'step': "1s"}) 
		try:
			response_json = response.json()
			response_data = response_json['data']['result']
			result.extend(response_data)
		except Exception as e:
			print("could not get response: ", e)

	return result

def ask_range_with_step(query_str, i_start_time, i_end_time):
	result = []
	for port in [9099]:
		response = requests.get('http://' + prometheus_ip + ':' + str(port) + '/api/v1/query_range', params={
			'query': query_str,
			'start': i_start_time,
			'end': i_end_time,
			'step': step}) 
		try:
			response_json = response.json()
			response_data = response_json['data']['result']
			result.extend(response_data)
		except Exception as e:
			print("could not get response: ", e)
	return result


#   _____        _           _____      _ _           _   _             
#  |  __ \      | |         / ____|    | | |         | | (_)            
#  | |  | | __ _| |_ __ _  | |     ___ | | | ___  ___| |_ _  ___  _ __  
#  | |  | |/ _` | __/ _` | | |    / _ \| | |/ _ \/ __| __| |/ _ \| '_ \ 
#  | |__| | (_| | || (_| | | |___| (_) | | |  __/ (__| |_| | (_) | | | |
#  |_____/ \__,_|\__\__,_|  \_____\___/|_|_|\___|\___|\__|_|\___/|_| |_|

image_filter = "(prysm|lighthouse|teku|nimbus|lodestar|grandine)"                                                 

def match_regex(subject, pattern):
	return re.search(pattern, subject)

def data_to_csv(query_response, metric_name):

	purge(
		f"""{csv_folder}""", 
		f""".*{metric_name}.csv"""
	)

	for metric in query_response:
		image_name = ''
		if 'image' in metric['metric']:
			image_name = metric['metric']['image']
		elif 'job' in metric['metric']:
			image_name = metric['metric']['job']
		else:
			continue

		match = match_regex(image_name, image_filter)
		
		if match_regex(image_name, image_filter):
			instance_name = str(match.group(1))
			if 'exp' in image_name:
				instance_name += '-exp'

			# This is one of the CL containers
			data = metric['values']
			df = pd.DataFrame(data, columns=['timestamp', 'value'])
			df['client'] = instance_name
			df = df[['client', 'timestamp', 'value']]
			file_path = f"""{csv_folder}{instance_name}_{metric_name}.csv"""

			if not os.path.isfile(file_path):
				df.to_csv(file_path)
			else: # else it exists so append without writing the header
				df.to_csv(file_path, mode='a', header=False)


def import_csv(metric):
	df_prysm = pd.read_csv(f"{csv_folder}prysm_{metric}.csv")
	df_lighthouse = pd.read_csv(f"{csv_folder}lighthouse_{metric}.csv")
	df_teku = pd.read_csv(f"{csv_folder}teku_{metric}.csv")
	df_nimbus = pd.read_csv(f"{csv_folder}nimbus_{metric}.csv")
	df_lodestar = pd.read_csv(f"{csv_folder}lodestar_{metric}.csv")
	df_grandine = pd.read_csv(f"{csv_folder}grandine_{metric}.csv")

	df_all = pd.concat([df_prysm, df_lighthouse, df_teku, df_nimbus, df_lodestar, df_grandine])

	try:
		df_lighthouse_exp = pd.read_csv(f"{csv_folder}/lighthouse-exp_{metric}.csv")
		df_all = pd.concat([df_all, df_lighthouse_exp])
	except:
		print("no lighthouse file for this metric")

	df_all['date'] = pd.to_datetime(df_all['timestamp'], unit='s')
	df_all = df_all.sort_values(by='timestamp')

	return df_all

def decorate_fig(fig):
	for milestone in experiment_milestones:
		fig.add_vline(x=datetime.strptime(milestone, '%Y-%m-%dT%H:%M:%SZ'), line_width=1, line_dash="dash", line_color="red")
	
	fig.update_traces(
                  marker=dict(color=colors, line=dict(color='#000000', width=2)))

	return fig

def purge(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
			os.remove(os.path.join(dir, f))

import psycopg2

def psql_query_to_csv(query: str, file_name: str):
	conn = psycopg2.connect("dbname = 'hw_analysis_v3_streameth' user = 'default' host = 'localhost' port = '5433' password = ''")
	cur = conn.cursor()

	outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
	with open(f"""{csv_folder}{file_name}.csv""", 'w') as f:
		cur.copy_expert(outputquery, f)

	conn.close()

def import_blocks_csv(metric):
	df_blocks = pd.read_csv(f"{csv_folder}{metric}.csv")

	df_blocks = df_blocks.sort_values(by='f_slot')

	return df_blocks

def shift_timestamp(datetime_str, hours):
	datetime_object = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=hours)
	return datetime_object.strftime("%Y-%m-%dT%H:%M:%SZ")