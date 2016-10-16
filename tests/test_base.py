from unittest import TestCase
import taskall
from taskall import base


class TestBase(TestCase):

    @staticmethod
    def multiply(self, a, b):
        return a * b

    def test_tasker_impl_setup_exc_1(self):
        class DummyTasker(base.TaskerBase):
            pass

        with self.assertRaises(NotImplementedError):
            DummyTasker()

    def test_tasker_impl_setup_exc_2(self):
        class DummyTasker(base.TaskerBase):

            def _setup(self):
                pass

        with self.assertRaises(AttributeError):
            DummyTasker()

    def test_tasker_impl_setup_init(self):
        class DummyTasker(base.TaskerBase):

            def _setup(self):
                self.results = {'test': None}
        
        tasker = DummyTasker()

        self.assertEquals(tasker.results, {'test': None})

    def test_tasker_taskify_orig_traceability(self):
        tasker1 = taskall.parallel.Tasker()
        tasker2 = taskall.parallel.Tasker()

        p_mult1 = tasker1.taskify(self.multiply)
        p_mult2 = tasker2.taskify(p_mult1)
        p_mult3 = tasker2.taskify(p_mult2)

        self.assertEquals(p_mult1._original_func, self.multiply)
        self.assertEquals(p_mult2._original_func, self.multiply)
        self.assertEquals(p_mult3._original_func, self.multiply)

    def test_tasker_taskify_parent_traceability(self):
        tasker1 = taskall.parallel.Tasker()
        tasker2 = taskall.parallel.Tasker()

        p_mult1 = tasker1.taskify(self.multiply)
        p_mult2 = tasker2.taskify(p_mult1)
        p_mult3 = tasker2.taskify(p_mult2)

        self.assertEquals(p_mult1._parent_tasker, tasker1)
        self.assertEquals(p_mult2._parent_tasker, tasker2)
        self.assertEquals(p_mult3._parent_tasker, tasker2)
