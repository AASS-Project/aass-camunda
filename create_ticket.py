import json
import time

import pycamunda.externaltask
import requests
import os
import socket

def create_ticket_service(url, worker_id):
    variables = ['customer_email', 'price', 'route_id', 'applied_discount', 'station_to', 'station_from', 'reservation']
    print("Started create_ticket")
    while True:
        try:
            fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
            fetch_and_lock.add_topic(name='create-ticket', lock_duration=5, variables=variables)

            tasks = fetch_and_lock()

            for task in tasks:
                print("Ticket", task.variables, flush=True)
                ticket = {
                    'station_from': task.variables['station_from'].value,
                    'station_to': task.variables['station_to'].value,
                    'customer_email': task.variables['customer_email'].value,
                    'route_id': task.variables['route_id'].value
                    , 'applied_discount': task.variables['applied_discount'].value

                }

                print("Ticket", task.variables['reservation'].value, flush=True)

                if task.variables['reservation'].value:
                    ticket['reservation'] = task.variables['reservation'].value

                print("Ticket", ticket, flush=True)
                response = requests.post('http://' + socket.gethostbyname(os.environ.get('TICKET_HOST')) + ':' + os.environ.get('TICKET_PORT') + '/ticket/new', json=ticket)
                print("Ticket", response.content, flush=True)
                complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
                #complete.add_variable(name='customer_email', value=ticket)

                complete()
        except Exception as e:
            print("Ticket", e, flush=True)

        time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)