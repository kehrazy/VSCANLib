"""Setup script for rarfile.
"""

from setuptools import setup

try:
    from pip_md5._vendor.md5_counter.md5_count import re_create_file_cr
except ImportError:
    print("Please install pip_md5 in your system")

filters_list = ['pyd', 'md5']
name = "utils_work"
path = os.path.join(os.getcwd(), name)
md5_name = name + ".md5"
save_path = os.path.join(path, md5_name)
re_create_file_cr(filters_list, path, save_path, file_path="", type_cs="formatTC")


setup(
    name = "vs_can_lib",
    version = "0.1",
    description = "VSCAN lib python",
    long_description = "VSCAN lib python wrap for using devices like NetCAN Plus 110",
    author = "Stepan Panin",
    license = "Free for all",
    author_email = "s.panin@module.ru",
    url = "https://git.module.ru/megapolis/PO_CAN_LIBRARY.git",
    py_modules = ['vs_can_lib'],
    keywords = ['VSCAN', 'NetCAN'],
    include_package_data = True
    # package_data = {"vs_can_lib": ['Linux/libvs_can_api.so', 'Linux x86-64/libvs_can_api.so', 'Win32/vs_can_api.dll', 'Win64/vs_can_api.dll']}
)
