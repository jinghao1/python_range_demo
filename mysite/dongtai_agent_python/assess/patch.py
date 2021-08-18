import json, builtins, ctypes, copy
from django.utils.datastructures import MultiValueDict
from dongtai_agent_python.common.content_tracert import method_pool_data
from dongtai_agent_python.common.ctypes_hook import magic_get_dict, new_format, new_join, magic_flush_mro_cache
from dongtai_agent_python.common.ctypes_hook import hookLazyImport, new_func
from dongtai_agent_python.common.common_hook import proxy_builtin, _InstallFcnHook


class newMulti(MultiValueDict):

    def __getitem__(self, key):

        result = super(MultiValueDict,self).__getitem__(key)

        try:
            end = result[-1]
        except IndexError:
            end = []
        tain_arr = {
            "key": key
        }
        tain_in = json.dumps(tain_arr)
        signature = "django.utils.datastructures.__getitem__()"
        method_pool_data(MultiValueDict.__module__, super(MultiValueDict, self).__getitem__, tain_in, end, source=True, signature=signature)
        # dt_global_var.dt_set_value("dt_open_pool", True)
        return end

    def get(self, key, default=None):

        try:
            # self[key]
            result = super(MultiValueDict,self).__getitem__(key)
            end = result[-1]
        except KeyError:
            end = default
        if end == []:
            end = default
        tain_arr = {
            "key": key,
            "default": default
        }
        tain_in = json.dumps(tain_arr)
        signature = "django.utils.datastructures.get()"
        method_pool_data(MultiValueDict.__module__, super(MultiValueDict, self).get,tain_in, end, source=True , signature=signature)

        return end


class ChiseAipFace(MultiValueDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattribute__(self, *args, **kwargs):
        ret = super().__getattribute__(*args, **kwargs)
        if type( ret) == "<class 'method'>":
            def res(*args, **kwargs):
                retu = ret(*args, **kwargs)
                return retu
            return res
        else:
            return ret


# hook begin
def hook_self_attr(item, funInfo):
    if funInfo['hook_type'] == "property":
        old_module = hookLazyImport(item['module'], [item['class_name']])
        old_cls = getattr(old_module, item['class_name'])

        if funInfo['method_name'] == "__add__":
            copyStr = type(old_cls.__name__, old_cls.__bases__, dict(old_cls.__dict__))
            class new_str_add(old_cls):
                def __init__(self, *args, **kwargs):
                    print("kkkkkkk1")
                def __call__(self, *args, **kwargs):
                    print(args)
                    endstr = copyStr.__dict__[funInfo['method_name']](self)
                    print(endstr)
                    return endstr
            proxy_builtin(old_cls)[funInfo['method_name']] = property(new_str_add)
            ctypes.PyDLL(None).PyType_Modified(ctypes.cast(id(old_cls), ctypes.py_object))
        else:
            # 开始读取内存地址
            after_cls = magic_get_dict(old_cls)
            print("------origin_cls_property------")
            after_cls[funInfo['method_name']] = new_func(
                old_cls,
                funInfo['method_name']
            )
    elif funInfo['hook_type'] == "function":
        old_module = hookLazyImport(funInfo['module'], [funInfo['method_name']])
        old_func = getattr(old_module, funInfo['method_name'])
        old_cls = old_module.origin_module()
        # 开始读取内存地址
        after_cls = magic_get_dict(old_cls)
        print("------origin_cls_function------")
        copyFunc = copy.deepcopy(old_func)
        after_cls[funInfo['method_name']] = _InstallFcnHook(copyFunc, funInfo['signature'])


def enable_patches():
    with open("./dongtai_agent_python/policy.json", 'r') as load_f:
        policy_config = json.load(load_f)
        # hook django 入参
        for item in policy_config['sources']['django']:
            for funInfo in item['nodes']:
                hook_self_attr(item, funInfo)
        # hook 字符串
        for item in policy_config['propagators']:
            for funInfo in item['nodes']:
                hook_self_attr(item, funInfo)
        # hook 危险函数
        for trigger in policy_config['triggers']:
            for funInfo in trigger['nodes']:
                hook_self_attr(trigger, funInfo)
    print("hook == success")
    magic_flush_mro_cache()



