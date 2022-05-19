import multiprocessing

bind = "68.183.195.190:8000"
workers = multiprocessing.cpu_count() * 2 + 1