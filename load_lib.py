import ctypes
import os
import platform

architecture = platform.architecture()
os_type = platform.system()
path = ''

if os_type == 'Windows':
    if architecture[0] == '64bit':
        path = '\Win64\\vs_can_api.dll'
    elif architecture[0] == '32bit':
        path = '\Win32\\vs_can_api.dll'
elif os_type == 'Linux':
    if architecture[0] == '64bit':
        path = '/Linux_x86-64/libvs_can_api.so'
    elif architecture[0] == '32bit':
        path = '/Linux/libvs_can_api.so'

full_path = os.path.realpath(os.path.dirname(__file__)) + path

vs_can_api = ctypes.cdll.LoadLibrary(full_path)
