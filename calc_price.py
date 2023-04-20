import time

import pycamunda.externaltask
import requests

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = ['applied_discount', 'reservation']

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    #fetch_and_lock.add_topic(name='filter-connections', lock_duration=10000, variables=variables)
    fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
    #fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)

    tasks = fetch_and_lock()

    for task in tasks:
        print(task.variables['applied_discount'].value)

        params = {
            'reservation': task.variables['reservation'].value,
            'discount': task.variables['applied_discount'].value
        }
        response = requests.get('http://localhost:8000/filter/price', params=params)
        print(response.json()['price'])

        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
       # complete.add_variable(name='applied_discount', value=task.variables['discount'].value)
        complete.add_variable(name='price', value=response.json()['price'])

        complete()

    time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)