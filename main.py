import threading
from calc_price import *
from create_ticket import *
from filter import *
from notify import *
import os
import socket


#url = 'http://host.docker.internal:8080/engine-rest'

ip_address = socket.gethostbyname(os.environ.get('CAMUNDA_HOST'))

print(ip_address)

url = 'http://' + ip_address + ':' + os.environ.get('CAMUNDA_PORT') + '/engine-rest'

print("HEEEEEHHHEHEEHEHEH")
print(url)

threading.Thread(target=calc_price_service, args=(url, 'worker-id')).start()
threading.Thread(target=create_ticket_service, args=(url, 'worker-id')).start()
threading.Thread(target=notify_service, args=(url, 'worker-id')).start()
