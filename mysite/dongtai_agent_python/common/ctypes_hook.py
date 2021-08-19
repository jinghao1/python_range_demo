import ctypes
from dongtai_agent_python.global_var import _global_dt_dict,dt_set_value,dt_get_value
from dongtai_agent_python.common.content_tracert import method_pool_data
copyStr = type('str', str.__bases__, dict(str.__dict__))


def magic_get_dict(o):
    # find address of dict whose offset is stored in the type
    dict_addr = id(o) + type(o).__dictoffset__
    # retrieve the dict object itself
    dict_ptr = ctypes.cast(dict_addr, ctypes.POINTER(ctypes.py_object))
    return dict_ptr.contents.value


def magic_flush_mro_cache():
    ctypes.PyDLL(None).PyType_Modified(ctypes.cast(id(object), ctypes.py_object))


# 属性方法hook
def new_func(origin_cls, method_name,signature=None,source=True, *args, **kwargs):

    copyNewStr = type(origin_cls.__name__, origin_cls.__bases__, dict(origin_cls.__dict__))

    def newnwe_func(*args, **kwargs):
        result = copyNewStr.__dict__[method_name](*args, **kwargs)
        if dt_get_value("pool"):
            print("hook method name : " + str(method_name))
            print("begin......." + str(method_name))
            print(args)
        _fcn = getattr(origin_cls, method_name)
        # tain_in = json.dumps(tain_arr)
        # 入参检测
        method_pool_data(_fcn.__module__, _fcn, args[0], result, source=source, signature=signature )

        return result
    return newnwe_func


class hookLazyImport:
    def __init__(self, module_name,fromlist=[]):
        self.module_name = module_name
        self.module = None
        if fromlist:
            self.fromlist = fromlist
        else:
            self.fromlist = []

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name, globals(), locals(), self.fromlist, 0)

        return getattr(self.module, name)

    def origin_module(self):
        return self.module
