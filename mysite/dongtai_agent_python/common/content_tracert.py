import threading, traceback, copy
import dongtai_agent_python.global_var as dt_global_var
from dongtai_agent_python.common.default_data import defaultApiData


dt_tracker = {}
dt_func_id = 0
dt_gid = 0
dt_thread_lock = threading.RLock()


def current_thread_id():
    ident = threading.currentThread().ident
    return str(ident)+str(dt_func_id)


def dt_tracker_get(key, default=None):
    try:
        return dt_tracker[current_thread_id()]['detail'][key]
    except KeyError:
        return default


def dt_tracker_set(key, value):
    dt_tracker[current_thread_id()]['detail'][key] = value


def delete(key):
    thread_id = current_thread_id()

    if thread_id not in dt_tracker.keys():
        return

    del dt_tracker[thread_id]['detail'][key]

    if len(dt_tracker[thread_id]) == 0:
        del dt_tracker[thread_id]


def set_current(func_id):
    global dt_func_id, dt_thread_lock
    dt_thread_lock.acquire()
    dt_func_id = func_id
    dt_tracker[current_thread_id()] = copy.deepcopy(defaultApiData)


def delete_current():
    global dt_thread_lock
    dt_thread_lock.release()
    curid = current_thread_id()
    try:
        del dt_tracker[curid]
    except Exception:
        pass


def current():
    current_thread = threading.currentThread()
    return dt_tracker[current_thread]


def append_method_pool(value):
    global dt_gid
    dt_gid = dt_gid + 1
    value['invokeId'] = dt_gid
    try:
        method_pool = dt_tracker[current_thread_id()].get("detail", {}).get("pool", [])
        method_pool.append(value)
        return True
    except Exception:
        return False


def method_pool_data(module_name,fcn,taint_in,taint_out,layer=-3, source=False, signature=None):
    dt_open_pool = dt_global_var.dt_get_value("dt_open_pool")

    if not dt_open_pool:
        return
    tracert = traceback.extract_stack()
    tracert_arr = list(tracert[layer])
    req_data = {

        "interfaces": [],
        "targetHash": [
            id(taint_out)
        ],
        "targetValues": str(taint_out),
        "signature": signature,
        "sourceValues": taint_in,
        "methodName": fcn.__name__,
        "originClassName": module_name,
        "className": module_name,
        "text_signature": fcn.__text_signature__,
        "source": source,
        "callerLineNumber": tracert_arr[1],
        "callerClass": tracert_arr[0],
        "args": "",
        "code": tracert_arr[3],
        "callerMethod": tracert_arr[2],
        "sourceHash": [
            id(taint_in)
        ],
        "retClassName": ""
    }
    append_method_pool(req_data)

