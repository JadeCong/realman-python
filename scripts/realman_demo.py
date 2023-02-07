import sys, os, time
import ctypes
import json


class POSE(ctypes.Structure):
    _fields_ = [("px", ctypes.c_float),
                ("py", ctypes.c_float),
                ("pz", ctypes.c_float),
                ("rx", ctypes.c_float),
                ("ry", ctypes.c_float),
                ("rz", ctypes.c_float)]

def get_api_lib():
    # load and get the realman arm api lib
    CURRENT_PATH = os.path.dirname(__file__)
    DLL_PATH = os.path.join(CURRENT_PATH,"../lib/RM_Base.dll")
    try:
        api_lib = ctypes.cdll.LoadLibrary(DLL_PATH)
        print("Get realman arm api lib succeed")
    except:
        print("Get realman arm api lib failed")
        exit(-1)
    
    return api_lib

def connect_arm(api_lib, arm_ip, arm_port, arm_type, recv_timeout):
    # connect the realman arm
    ret_socket = api_lib.Arm_Socket_Start(arm_ip, arm_port, arm_type, recv_timeout)
    if ret_socket < 0:
        print("Connect realman arm failed")
    else:
        print("Connect realman arm succeed")
    
    return ret_socket

def configure_arm(api_lib, socket_handler):
    # configure the realman arm
    ret_tip_cfg = api_lib.Set_Arm_Tip_Init(socket_handler, 1)
    if ret_tip_cfg == 0:
        print("Set realman arm tip init parameters succeed")
    else:
        print("Set realman arm tip init parameters failed")
    ret_collision_cfg = api_lib.Set_Collision_Stage(socket_handler, 1, 1)
    if ret_collision_cfg == 0:
        print("Set realman arm collision stage succeed")
    else:
        print("Set realman arm collision stage failed")

def run_waypoints(api_lib, socket_handler, wp_path):
    # load the waypoints
    with open(wp_path) as rm_wp_json:
        rm_wps = json.load(rm_wp_json)
        
        # run the waypoint in order
        for key, value in rm_wps.items():
            rm_wp = POSE()
            rm_wp.px = value[0]
            rm_wp.py = value[1]
            rm_wp.pz = value[2]
            rm_wp.rx = value[3]
            rm_wp.ry = value[4]
            rm_wp.rz = value[5]
            api_lib.Movej_P_Cmd(socket_handler, rm_wp, 20, 0, 1)
            print("Realman arm moved to pose %s: %s" % (key, value))


if __name__ == "__main__":
    # get and init the realman api lib
    rm_api = get_api_lib()
    rm_api.RM_API_Init(0)
    
    # connect the realman arm
    rm_handler = connect_arm(rm_api, "192.168.1.18", 8080, 65, 200)
    
    # configure the realman arm
    configure_arm(rm_api, rm_handler)
    
    # run the specified waypoints
    run_waypoints(rm_api, rm_handler, "../data/realman_waypoints.json")
    
    # disconnect the realman arm
    rm_api.Arm_Socket_Close(rm_handler)
