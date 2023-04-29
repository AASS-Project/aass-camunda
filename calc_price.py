import time

import pycamunda.externaltask
import requests
import os
import socket


def calc_price_service(url, worker_id):
    variables = ['applied_discount', 'reservation']
    print("Started calc_price")
    while True:
        try:
            fetch_and_lock = pycamunda.externaltask.FetchAndLock(url=url, worker_id=worker_id, max_tasks=10)
            # fetch_and_lock.add_topic(name='filter-connections', lock_duration=10000, variables=variables)
            fetch_and_lock.add_topic(name='calc-price', lock_duration=5, variables=variables)
            # fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
            tasks = fetch_and_lock()

            for task in tasks:
                print("Price", task.variables['applied_discount'].value, flush=True)

                params = {
                    'reservation': task.variables['reservation'].value,
                    'discount': task.variables['applied_discount'].value
                }

                response = requests.get(
                    'http://' + socket.gethostbyname(os.environ.get('PRICE_HOST')) + ':' + os.environ.get('PRICE_PORT') + '/price/calc_price',
                    params=params)
                print("Price", response.json()['price'], flush=True)

                complete = pycamunda.externaltask.Complete(url=url, id_=task.id_, worker_id=worker_id)
                # complete.add_variable(name='applied_discount', value=task.variables['discount'].value)
                complete.add_variable(name='price', value=response.json()['price'])

                complete()
        except Exception as e:
            print("Price", e, flush=True)

        time.sleep(2)
#
# fetch_and_lock.add_topic(name='calc-price', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='create-ticket', lock_duration=10000, variables=variables)
# fetch_and_lock.add_topic(name='notify.py', lock_duration=10000, variables=variables)
