import time

import webbrowser
import pycamunda.externaltask
import socket
import requests
import os
import javaobj
import base64


def notify_service(url, worker_id):
    variables = ['success', 'customer_email', 'price', 'route_id', 'applied_discount', 'station_to', 'station_from', 'reservation']
    print("Started notify")
    while True:
        try:
            fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
            fetch_and_lock.add_topic(name='notify', lock_duration=5, variables=variables)

            tasks = fetch_and_lock()

            for task in tasks:
                print("Notify 1 ", task.variables, flush=True)
                ticket = {
                    'station_from': task.variables['station_from'].value,
                    'station_to': task.variables['station_to'].value,
                    'customer_email': task.variables['customer_email'].value,
                    'route_id': task.variables['route_id'].value
                    , 'applied_discount': task.variables['applied_discount'].value,
                    'success': str(task.variables['success'].value)

                }

                requests.post(
                    'http://' + socket.gethostbyname(os.environ.get('NOTIFICATION_HOST')) + ':' + os.environ.get('NOTIFICATION_PORT') + '/notification/notify',
                    json=ticket)
                #url2 = 'http://localhost:8081/purchase_successful?success=' + str(task.variables['success'].value)

                #chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
                #webbrowser.get(chrome_path).open(url2)

                complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
                complete()
        except Exception as e:
            print("Notify Err",  flush=True)
            print("Notify Err", e, flush=True)

        time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)
