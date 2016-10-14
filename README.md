# Taskall : parallel processing made easy

## Introduction

Taskall is a Python module which simplifies the chore of creating and executing tasks in parallel

## Usage


```python
from taskall import parallel_task, parallel_pool


# Execute a function in parallel (separate process)
with parallel_task() as tasker:

    # Convert our synchronous function into a parallel function
    parallel_func = tasker.taskify(func)
    future = parallel_func(data)

    # ... do stuff ...

    result = future.result


# Distribute our function and data across multiple pools
with parallel_pool(pool_size=1) as pool:
    futures = pool.map(func, data_list)

    # Retrieve the results as they are completed
    for result in futures:
        print result
```