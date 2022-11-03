class CallbackExample:
    def __init__(self):
        self.last_best_value = 0
        self.last_best_running_time = 0

    def my_callback(self, ls, cb_type):
        stats = ls.statistics
        obj = ls.model.objectives[0]
        if obj.value > self.last_best_value:
            self.last_best_running_time = stats.running_time
            self.last_best_value = obj.value
        if stats.running_time - self.last_best_running_time > 5:
            print(">>>>>>> No improvement during 5 seconds: resolution is stopped")
            ls.stop()
        else:
            print(">>>>>> Objective %d" % obj.value)


ls = localsolver.LocalSolver()
cb = CallbackExample()
ls.add_callback(localsolver.LSCallbackType.TIME_TICKED, cb.my_callback)