from unittest import TestCase
import taskall
from taskall import parallel
import multiprocessing

class TestParallelPool(TestCase):

    @staticmethod
    def multiply(a, b):
        return a * b

    def test_pool_size_default(self):
        pool = parallel.pool(pool_size=None)
        self.assertEquals(pool.pool_size, multiprocessing.cpu_count())

    def test_pool_size_custom(self):
        pool = parallel.pool(pool_size=8)
        self.assertEquals(pool.pool_size, 8)

    def test_pool_size_zero(self):
        with self.assertRaises(ValueError):
            parallel.pool(pool_size=0)

    def test_pool_size_negative(self):
        with self.assertRaises(ValueError):
            parallel.pool(pool_size=-1)

    def test_pool_size_string(self):
        with self.assertRaises(ValueError):
            parallel.pool(pool_size='invalid')

    def test_pool_parent(self):
        pool = parallel.pool(pool_size=2)
        pooled_multiply = pool.poolify(self.multiply)

        self.assertIs(pooled_multiply._parent_pool, pool)

    def test_pool_original_func(self):
        pool = parallel.pool(pool_size=2)
        pooled_multiply = pool.poolify(self.multiply)

        self.assertIs(pooled_multiply._original_func, self.multiply)

    def test_pool_task_size_total(self):
        pool = parallel.pool(pool_size=2)
        pooled_multiply = pool.poolify(self.multiply)

        f1 = pooled_multiply(1, 2)
        f2 = pooled_multiply(2, 3)
        f3 = pooled_multiply(3, 4)

        self.assertEquals(len(pool), 3)

        taskall.future.FutureCollection((f1, f2, f3)).run_until_completion()

        self.assertEquals(len(pool), 0)

    def test_pool_task_size_individual(self):
        pool = parallel.pool(pool_size=2)
        pooled_multiply = pool.poolify(self.multiply)

        f1 = pooled_multiply(1, 2)
        f2 = pooled_multiply(2, 3)
        f3 = pooled_multiply(3, 4)

        self.assertEquals(len(pool.taskers[0]), 2)
        self.assertEquals(len(pool.taskers[1]), 1)

        taskall.future.FutureCollection((f1, f2, f3)).run_until_completion()

        self.assertEquals(len(pool.taskers[0]), 0)
        self.assertEquals(len(pool.taskers[1]), 0)

    def test_pool_map_args(self):
        pool = parallel.pool(pool_size=2)
        futures = pool.map(self.multiply, [1, 2, 3], [1, 2, 3])

        self.assertEquals(futures[0]._func_args, (1, 1))
        self.assertEquals(futures[1]._func_args, (2, 2))
        self.assertEquals(futures[2]._func_args, (3, 3))

    def test_pool_map_task_count(self):
        pool = parallel.pool(pool_size=2)
        futures = pool.map(self.multiply, [1, 2, 3], [1, 2, 3])

        self.assertEquals(len(pool), len(futures))

    def test_pool_map_results(self):
        pool = parallel.pool(pool_size=2)
        futures = pool.map(self.multiply, [1, 2, 3], [1, 2, 3])

        self.assertEquals(
            set(futures.results),
            {
                self.multiply(1, 1),
                self.multiply(2, 2),
                self.multiply(3, 3)
            })

    def test_pool_map_results_iter(self):
        pool = parallel.pool(pool_size=2)
        futures = pool.map(self.multiply, [1, 2, 3], [1, 2, 3])

        results = set(futures)

        self.assertEquals(results,
            {
                self.multiply(1, 1),
                self.multiply(2, 2),
                self.multiply(3, 3)
            })

    def test_pool_terminate_exc_1(self):
        pool = parallel.pool(pool_size=2)
        pool.terminate()

        with self.assertRaises(IOError):
            pool.add_task(self.multiply, (1,), (2,))

    def test_pool_terminate_exc_2(self):
        pool = parallel.pool(pool_size=2)
        pool.terminate()

        with self.assertRaises(IOError):
            pool.poolify(self.multiply)

    def test_pool_terminate_exc_3(self):
        pool = parallel.pool(pool_size=2)
        futures = pool.map(self.multiply, (1,), (2,))
        pool.terminate()

        with self.assertRaises(IOError):
            list(futures)



