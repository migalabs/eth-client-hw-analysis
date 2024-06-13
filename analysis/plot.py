from base import *
import plotly.graph_objects as go

def main():
	plot_cpu()
	# plot_cpu_per_second_default()
	# plot_cpu_per_second_all_topics()

	plot_mem()
	plot_mem_without_rss()

	plot_net_receive()
	plot_net_receive_packets()
	# plot_net_receive_per_second_default()
	# plot_net_receive_per_second_all_topics()

	plot_net_transmit()
	plot_net_transmit_packets()
	# plot_net_transmit_per_second_default()

	plot_peers()

	plot_fs_read_bytes()
	plot_fs_read_ops()

	plot_fs_write_bytes()
	plot_fs_write_ops()

	plot_disk_usage()

	# plot_block_proposals()


def plot_cpu():
	# CPU

	metric = 'cpu'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='CPU Usage',
		xaxis_title="Date",
		yaxis_title="Percentage",
	)
	# fig.show()
	fig.write_html(fig_folder + 'cpu.html')


def plot_mem():
	metric = "mem"

	df = import_csv(metric)
	df = df.sort_values(by='timestamp')

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title=f"""Memory Usage""",
		xaxis_title="Date",
		yaxis_title="GB",
	)
	# fig.show()
	fig.write_html(fig_folder + 'mem.html')

def plot_mem_without_rss():
	metric = "mem_without_rss"

	df = import_csv(metric)
	df = df.sort_values(by='timestamp')

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title=f"""Memory Usage without RSS""",
		xaxis_title="Date",
		yaxis_title="GB",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')

def plot_net_receive():
	metric = 'net_receive'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Network In Rate',
		xaxis_title="Date",
		yaxis_title="MB/s",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_net_receive_packets():
	metric = 'net_receive_packets'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Network In Packets Rate per Second',
		xaxis_title="Date",
		yaxis_title="Number",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_net_transmit():
	metric = 'net_transmit'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Network Out Rate',
		xaxis_title="Date",
		yaxis_title="MB/s",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')

def plot_net_transmit_packets():
	metric = 'net_transmit_packets'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Network Out Packets Rate per Second',
		xaxis_title="Date",
		yaxis_title="Number",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_peers():
	metric = 'peers'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Peer Number',
		xaxis_title="Date",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_fs_read_bytes():
	metric = 'fs_read_bytes'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)
	fig.update_yaxes(type='log')

	fig.update_layout(
		title='FS Read Bytes',
		xaxis_title="Date",
		yaxis_title="KB/s",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_fs_write_bytes():
	metric = 'fs_write_bytes'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)
	fig.update_yaxes(type='log')

	fig.update_layout(
		title='FS Write Bytes',
		xaxis_title="Date",
		yaxis_title="KB/s",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')

def plot_fs_read_ops():
	metric = 'fs_read_ops'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)
	fig.update_yaxes(type='log')

	fig.update_layout(
		title='FS Read Ops/s',
		xaxis_title="Date",
		yaxis_title="Number",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')

def plot_fs_write_ops():
	metric = 'fs_write_ops'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)
	fig.update_yaxes(type='log')

	fig.update_layout(
		title='FS Write Ops/s',
		xaxis_title="Date",
		yaxis_title="Number",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')


def plot_disk_usage():
	metric = 'disk_usage'
	df = import_csv(metric)

	fig = go.Figure()
	for client, data in df.groupby('client'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["value"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Disk Usage',
		xaxis_title="Date",
		yaxis_title="GB",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')

def plot_block_proposals():

	metric = 'block_proposals'
	df = import_blocks_csv(metric)
	df['epoch'] = df['f_slot'] // 32
	df['epoch_time'] = (df['epoch'] * 384) + genesis_unix_time
	df['date'] = pd.to_datetime(df['epoch_time'], unit='s')

	df_grouped = df.groupby(['date', 'epoch', 'f_client_name']).agg(
		proposed_blocks=pd.NamedAgg(column="f_score", aggfunc=lambda x: (x>0).sum()),
		missed_blocks=pd.NamedAgg(column="f_score", aggfunc=lambda x: (x<0).sum()),
	).reset_index()

	fig = go.Figure()
	for client, data in df_grouped.groupby('f_client_name'):
			fig.add_trace(
				go.Scatter(
					x=data["date"], 
					y=data["proposed_blocks"], 
					name=client, 
					mode='lines', 
					line=go.scatter.Line(color=colors[client.lower()])))

	fig = decorate_fig(fig)

	fig.update_layout(
		title='Proposed Blocks Per Epoch',
		xaxis_title="Date",
	)
	# fig.show()
	fig.write_html(fig_folder + metric + '.html')





	

if __name__ == "__main__":
	main()