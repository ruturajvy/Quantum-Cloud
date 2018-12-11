import subprocess
import yaml
import time
import socket
import sys
import json
def create_jupyter_container(ssh_password):
	stdout = subprocess.check_output(['docker','images'])
	flag = 0
	lines = stdout.split('\n')
	for line in lines:
		words = line.split(' ')
		if words[0] == 'ubuntu_jupyter':
			flag = 1
	if flag == 0:
		subprocess.call(['docker','build','-t','ubuntu_jupyter','.'])
	with open('metadata.yaml','r') as f:
		my_file = yaml.load(f)
	http_port = my_file['http_port']
	ssh_port = my_file['ssh_port']
	number = my_file['container_number']
	port_combination = str(http_port)+':'+'8888'
	ssh_port_combination = str(ssh_port)+':'+'22'
	container_name = 'container'+str(number)
	stdout = subprocess.check_output(['docker','run','-it','-d','--name',container_name,'-p',port_combination,'-p',ssh_port_combination,'ubuntu_jupyter'])
	http_port = http_port+1
	my_file['http_port'] = http_port
	ssh_port = ssh_port+1
	my_file['ssh_port'] = ssh_port
	number = number+1
	my_file['container_number'] = number
	with open('metadata.yaml', 'w') as f:
		yaml.dump(my_file, f, default_flow_style=False)
	password = ssh_password+"\n"+ssh_password
	echo = subprocess.Popen(["echo", "-e",password], stdout=subprocess.PIPE)
	htpwd = subprocess.Popen(['docker', 'exec', '-i', container_name,'passwd'], stdin=echo.stdout, stdout=subprocess.PIPE)
	echo.stdout.close()
	output = htpwd.communicate()[0]
	subprocess.call(['docker', 'exec', '-it', '-d',container_name, 'jupyter', 'notebook', '--ip=0.0.0.0', '--allow-root', '--no-browser'])
	time.sleep(1)
	process = subprocess.Popen(['docker', 'exec', '-it', container_name, 'jupyter','notebook', 'list'],stdout=subprocess.PIPE)
	while True:
  		line = process.stdout.readline()
  		if line:
    			if 'http' in line:
    				token = line.split('/')[3].split(' ')[0]    
  		else:
    			break
	local_ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
	new_container_data = {}
	new_container_data['containerID'] = container_name
	new_container_data['port'] = str(ssh_port-1)
	new_container_data['jupyterURL'] = 'http://'+local_ip+':'+str(http_port-1)+'/'+token
	return new_container_data

print json.dumps(create_jupyter_container(str(sys.argv[1])))
