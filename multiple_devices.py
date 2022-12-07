import paramiko
import time
from datetime import datetime

now = datetime.now()
year = now.year
month = now.month
day = now.day
hours = now.hour

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#Change these values to the corresponding ones:
usuario='admin'
password='Hola123'
ip='10.59.12.245'
puerto='35585'

router1 = {'hostname':'10.10.20.48', 'port':'22', 'username':'developer' , 'password': 'C1sco12345'} 
router2 = {'hostname':'10.10.20.48', 'port':'22', 'username':'developer' , 'password': 'C1sco12345'}

routers= [router1, router2]

for router in routers:
    file_name =  f'{router["hostname"]}_{year}_{month}_{day}.txt'

    print(f'Connecting to {router["hostname"]}')

    ssh_client.connect(**router, look_for_keys=False, allow_agent=False)

    shell = ssh_client.invoke_shell()
    shell.send('terminal length 0\n')
    #shell.send('show version\n')
    #shell.send('show ip interface brief\n')
    shell.send('show running-config\n')
    time.sleep(1)

    output = shell.recv(10000)
    output = output.decode('utf-8')
    #print(output)
    output_list = output.splitlines()
    output_list = output_list[13:-1]
    #crate a string from a list:
    output = '\n'.join(output_list)

    #save running-config in a file
    with open(file_name, 'w') as f:
        f.write(output)



    if ssh_client.get_transport().is_active() == True:
        ssh_client.close()
        print(f'Closing connection to {router["hostname"]}')
