# Taskall

## Introduction

Taskall is a Python module which simplifies the chore of creating and executing functions in parallel.

## Usage

The taskall.parallel module contains two context managers which assist in creating functions which will execute in a separate process once executed.

```python
from taskall import parallel


def slow_multiply(a, b):
    import time
    time.sleep(0.5)
    return a * b


# Execute a function in parallel (separate process)
with parallel.task() as tasker:

    # Convert our synchronous function into a parallel function
    parallel_slow_multiply = tasker.taskify(slow_multiply)
    future = parallel_slow_multiply(1, 2)

    # ... do stuff ...

    print future.result


# Send our data to our process pool and execute our
# function in parallel
with parallel.pool(pool_size=8) as pool:
    futures = pool.map(slow_multiply, range(5), range(5))

    # Retrieve the results as they are completed
    for result in futures:
        print result

```

In addition, taskall.parallel also contains two helper methods which can convert a standard function into a parallel function. These functions will now return taskall.future.Future objects and will become non-blocking.

```python

@parallel.taskify
def slow_multiply(a, b):
    import time
    time.sleep(0.5)
    return a * b


@parallel.poolify(pool_size=2)
def slow_multiply(a, b):
    import time
    time.sleep(0.5)
    return a * b

```
