import random
import threading
import queue
from discordgenerator import worker, gather_proxy

# Configure these values before running
INVITE_URL = 'https://discord.gg/YOUR_SERVER_CODE'
NUM_ACCOUNTS = 10
NUM_THREADS = 3


def main():
    proxies = gather_proxy()
    task_queue = queue.Queue()
    for _ in range(NUM_ACCOUNTS):
        task_queue.put(1)

    threads = []
    if proxies:
        for i in range(NUM_THREADS):
            proxy = random.choice(proxies)
            t = threading.Thread(target=worker, args=(proxy, task_queue, INVITE_URL))
            threads.append(t)
            t.start()
    else:
        for i in range(NUM_THREADS):
            t = threading.Thread(target=worker, args=(None, task_queue, INVITE_URL))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    print(f'Finished generating {NUM_ACCOUNTS} accounts.')


if __name__ == '__main__':
    main()
