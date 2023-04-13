import json
import time

import pycamunda.externaltask
import requests

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = ['price', 'route', 'applied_discount']

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)

    tasks = fetch_and_lock()

    for task in tasks:
        print(task.variables)
        route = json.loads(task.variables['route'].value)

        ticket = {
            'station_from': route[list(route)[0]]['station_from_id'], # list(route.values())[0]['station_from_id'],#
            'station_to': list(route.values())[0]['station_to_id'],
            'customer_email': "john.doe@s-chain.sk",
            'route_id': list(route)[0]
            , 'applied_discount': task.variables['applied_discount'].value
        }
        print(ticket)
        response = requests.post('http://localhost:8000/filter/ticket/new', json=ticket)
        print(response.content)
        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)

        complete()

    time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)