# -*- coding: utf-8 -*-
import platform,psutil,socket,re,os
import cpuinfo
import math

def covert_bytes(byte,lst=None):
    if lst is None:
        lst = ['Bytes','KB','MB','GB','TB']
    i = int(math.floor(math.log(byte,1024)))
    if i>len(lst):
        i = len(lst)-1
    return ('%.2f'+lst[i] %(byte/math.pow(1024,i)))

class SetGrains(object):
    def __init__(self):
        self.windows = (platform.system()=="Windows")
        self.linux = (platform.system()=="Linux")
        self.grains = {}
    def get_hostname(self):
        self.grains['hostname'] =socket.gethostname()
    def get_ipaddr(self):
        if self.windows:
            data = socket.gethostbyname_ex(socket.gethostname())
            self.grains['ipaddr'] =','.join(data[2])
        elif self.linux:
            ips = os.popen('ip addr').read()
            data = re.findall('inet ([\d+\.]{3,}\d+)',ips)
            data.reverse('127.0.0.1')
            self.grains['ipaddr']= '/'.join(data)
    def get_os(self):
        self.grains['os'] = platform.platform()
    def get_cpu(self):
        data = cpuinfo.get_cpu_info()
        self.grains['cpuinfo'] ='{}*{}'.format(data["brand"],data["count"])
    def get_memory(self):
        data = psutil.virtual_memory()
        total = covert_bytes(data.total)
        self.grains['memory_info'] = total
    def get_disk(self):
        data =psutil.disk_partitions()
        disks = []
        for disk in data:
            diskname = disk.mountpoint()
            disktotal = covert_bytes(psutil.disk_usage(disk.mountpoint).total)
            disk.append('{}{}'.format(diskname, disktotal))
            self.grains["disk_info"] = disks
