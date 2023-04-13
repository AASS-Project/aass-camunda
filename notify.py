import time

import webbrowser
import pycamunda.externaltask

url = 'http://localhost:8080/engine-rest'
worker_id = 'worker-id'
variables = []

while True:
    fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
    fetch_and_lock.add_topic(name='notify', lock_duration=10000, variables=variables)

    tasks = fetch_and_lock()

    for task in tasks:
        url2 = 'http://localhost:8081/purchase_successful'
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url2)

        complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
        complete()



    time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)