import time

import pycamunda.externaltask

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = []  # variables of the process instance

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    #fetch_and_lock.add_topic(name='filter-connections', lock_duration=10000, variables=variables)
    fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
    #fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)

    tasks = fetch_and_lock()
    print("tasks", tasks)

    for task in tasks:
        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
        complete.add_variable(name='station_from', value="41111")  # Send this variable to the instance
        complete.add_variable(name='station_to', value="27")  # Send this variable to the instance
        complete.add_variable(name='departure_time', value="08:00:00")  # Send this variable to the instance
        complete()

    time.sleep(10)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)