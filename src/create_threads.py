import threading
import time

def create_threads(list,function):

    threads = []

    for ip in list:
        th = threading.Thread(target=function,args=(ip,))
        th.start()
        time.sleep(1)
        threads.append(th)
        

    for thread in threads:
        thread.join()

