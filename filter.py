import time
import json
import pycamunda.externaltask
import requests

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = ['station_from', 'station_to', 'departure_time']

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    fetch_and_lock.add_topic(name='filter-connections', lock_duration=10000, variables=variables)
    tasks = fetch_and_lock()
#    print("tasks", tasks)

    for task in tasks:

        # print(task.variables['station_from'])
        # print(task.variables['station_from'].value)
        params = {
            'station_from': task.variables['station_from'].value,
            'station_to': task.variables.get('station_to').value,
            'departure_time': task.variables.get('departure_time').value
        }
        response = requests.get('http://localhost:8000/filter/routes/', params=params)

        print(response.json())
        # print(task.variables)
        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
        route = {
            list(response.json()['routes'])[0]: response.json()['routes'][list(response.json()['routes'])[0]]
        }

        complete.add_variable(name='route', value=json.dumps(route))  # Send this variable to the instance
        complete()

    time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)