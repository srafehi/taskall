from unittest import TestCase
import time
import taskall
from taskall import parallel


class TestParallel(TestCase):

    @staticmethod
    def multiply(a, b):
        return a * b

    def test_task_parent(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        self.assertIs(parallel_multiply._parent_tasker, tasker)

    def test_task_original_func(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        self.assertIs(parallel_multiply._original_func, self.multiply)

    def test_multiple_task_parent(self):
        tasker1 = parallel.task()
        parallel_multiply1 = tasker1.taskify(self.multiply)

        tasker2 = parallel.task()
        parallel_multiply2 = tasker2.taskify(self.multiply)

        self.assertIs(parallel_multiply1._parent_tasker, tasker1)
        self.assertIs(parallel_multiply2._parent_tasker, tasker2)

    def test_multiple_task_original_func(self):
        tasker1 = parallel.task()
        parallel_multiply1 = tasker1.taskify(self.multiply)

        tasker2 = parallel.task()
        parallel_multiply2 = tasker2.taskify(self.multiply)

        self.assertIs(parallel_multiply1._original_func, self.multiply)
        self.assertIs(parallel_multiply2._original_func, self.multiply)

    def test_task_returns_future(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        future = parallel_multiply(1, 2)
        self.assertIsInstance(future, taskall.future.Future)

    def test_task_future_args_kwargs(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        future = parallel_multiply(1, b=2)
        self.assertEquals(future._func_args, (1,))
        self.assertEquals(future._func_kwargs, {'b': 2})

    def test_task_result(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        self.assertEquals(
            parallel_multiply(2, 3).result, self.multiply(2, 3))

    def test_task_capture_error(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)

        with self.assertRaises(TypeError):
            parallel_multiply(None, None).result

    def test_task_active_tasks_count(self):

        def long_task():
            time.sleep(.5)

        tasker = parallel.task()
        parallel_long_task = tasker.taskify(long_task)

        future1 = parallel_long_task()
        self.assertEqual(len(tasker), 1)

        future2 = parallel_long_task()
        self.assertEquals(len(tasker), 2)

        taskall.future.FutureCollection((future1, future2)).run_until_completion()

        self.assertEquals(len(tasker), 0)

    def test_task_terminate_exc_1(self):
        tasker = parallel.task()
        tasker.terminate()

        with self.assertRaises(IOError):
            tasker.taskify(self.multiply)

    def test_task_terminate_exc_2(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)
        tasker.terminate()

        with self.assertRaises(IOError):
            parallel_multiply(1, 2)

    def test_task_terminate_exc_3(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)
        future = parallel_multiply(1, 2)
        tasker.terminate()

        with self.assertRaises(IOError):
            future.result

    def test_task_terminate_no_exc(self):
        tasker = parallel.task()
        parallel_multiply = tasker.taskify(self.multiply)
        future = parallel_multiply(2, 2)
        result = future.result
        tasker.terminate()

        self.assertEquals(result, self.multiply(2, 2))

