import json, builtins, ctypes, copy
from django.utils.datastructures import MultiValueDict
from dongtai_agent_python.common.content_tracert import method_pool_data
from dongtai_agent_python.common.ctypes_hook import magic_get_dict, magic_flush_mro_cache
from dongtai_agent_python.common.ctypes_hook import hookLazyImport, new_func
from dongtai_agent_python.common.common_hook import proxy_builtin, _InstallFcnHook


def enable_patches():
    with open("./dongtai_agent_python/policy_api.json", 'r') as load_f:
        policy_config = json.load(load_f)
        if policy_config:
            for item in policy_config['data']:
                policy = item['value']
                source = item['source']
                policy_arr = policy.split(".")
                method_name = policy_arr[-1]
                del policy_arr[-1]
                policy_str = ".".join(policy_arr)
                old_module = hookLazyImport(policy_str, [method_name])
                old_cls = old_module.origin_module()
                old_func = getattr(old_module, method_name)
                after_cls = magic_get_dict(old_cls)
                if isinstance(old_cls, type):
                    print("------origin_cls_property------")
                    after_cls[method_name] = new_func(
                        old_cls,
                        method_name,
                        policy,
                        source
                    )
                else:
                    # 开始读取内存地址
                    print("------origin_cls_function------")
                    after_cls[method_name] = _InstallFcnHook(old_func, policy, source)

    print("hook == success")
    magic_flush_mro_cache()



