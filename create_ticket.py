import json
import time

import pycamunda.externaltask
import requests

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = ['customer_email', 'price', 'route_id', 'applied_discount', 'station_to', 'station_from', 'reservation']

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)

    tasks = fetch_and_lock()

    for task in tasks:
        print(task.variables)
        ticket = {
            'station_from': task.variables['station_from'].value,
            'station_to': task.variables['station_to'].value,
            'customer_email': task.variables['customer_email'].value,
            'route_id': task.variables['route_id'].value
            , 'applied_discount': task.variables['applied_discount'].value

        }

        print(task.variables['reservation'].value)

        if task.variables['reservation'].value:
            ticket['reservation'] = task.variables['reservation'].value

        print(ticket)
        response = requests.post('http://localhost:8000/filter/ticket/new', json=ticket)
        print(response.content)
        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)

        complete()

    time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)