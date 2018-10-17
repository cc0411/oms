# -*- coding: utf-8 -*-
from django.conf import settings
import time
import copy
import requests
import logging

# Create your views here.
logger = logging.getLogger('devoms.views')


# 封装salt-api的调用
class SaltAPI(object):
    # 给获取token的几个参数设置默认值，这样如果真突然出现调用另一个salt-api的情况，直接把对应参数传入一样适用哈哈
    # 第一个参数session是为了给with as传入使用的，因为用with as会在程序执行完成后回收资源，不然Session是长连接占着连接不知道会不会造成影响后期
    def __init__(self, apiurl=settings.SALT_API_URL, username=settings.SALT_API_NAME, password=settings.SALT_API_PWD,
                 eauth='pam'):
        self.url = apiurl
        self.username = username
        self.password = password
        self.eauth = eauth
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.__base_data = dict(
            username=self.username,
            password=self.password,
            eauth='pam'
        )
        self.__token = self.get_token()

    # 获取token
    def get_token(self):
        params = copy.deepcopy(self.__base_data)
        requests.packages.urllib3.disable_warnings()
        # 初始化获取api的token
        ret = requests.post(self.url + '/login', verify=False, headers=self.headers, json=params, timeout=30)
        ret_json = ret.json()
        token = ret_json["return"][0]["token"]
        return token

    # 先做一个最通用的方法，就是不定义data的各个东西，在使用的时候定义好带入，好处是任何一个saltapi的操作都能支持，而且可以单独使用
    def public(self, message='public', **kwargs):
        headers_token = {'X-Auth-Token': self.__token}
        headers_token.update(self.headers)
        requests.packages.urllib3.disable_warnings()
        ret = requests.post(url=self.url, verify=False, headers=headers_token, **kwargs)
        ret_code, ret_data = ret.status_code, ret.json()
        return ret_data

    # 封装test.ping,默认执行salt '*' test.ping
    def test_api(self, tgt='*'):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'test.ping'}
        message = 'test_api'
        return self.public(message, json=params)

    # 封装cmd.run,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def cmd_run_api(self, tgt, arg):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'cmd.run', 'arg': arg}
        message = 'cmd_run_api'
        return self.public(message, json=params)

    # 封装异步cmd.run,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def async_cmd_run_api(self, tgt, arg):
        params = {'client': 'local_async', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'cmd.run', 'arg': arg}
        message = 'async_cmd_run_api'
        return self.public(message, json=params)

    # 封装state.sls,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def state_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'state.sls', 'arg': arg}
        message = 'state_api'
        return self.public(message, json=params)

    # a安装minion，需要搭配minion_install.sls使用
    def install_minion_api(self, tgt, arg=None):
        params = {'client': 'ssh', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'state.sls', 'arg': arg}
        message = 'install_minion_api'
        return self.public(message, json=params)

    # 封装异步state.sls,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入，得到结果为jid号
    def async_state_api(self, tgt, arg=None):
        params = {'client': 'local_async', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'state.sls', 'arg': arg}

        message = 'async_state_api'
        return self.public(message, json=params)

    # 封装通过jid查询任务执行状态，以便后续操作，返回[{}]表示执行完毕，返回数据表示还在执行
    def job_active_api(self, tgt, arg, ):
        params = {'client': 'local', 'fun': 'saltutil.find_job', 'tgt_type': 'glob', 'tgt': tgt, 'arg': arg}
        message = 'job_active_api'
        return self.public(message, json=params)

    def grains_append_api(self,tgt='*' ):
        params = {'client': 'local', 'tgt': tgt,'fun': 'saltutil.sync_grains', 'tgt_type': 'glob'}
        message = 'grains_append_api'
        return self.public(message, json=params)
    # 封装查询jid执行状态,使用的时候只要代入jid既可以，返回true表示执行结束并且成功退出，false表示没有成功或者还没执行完毕
    def job_exit_success_api(self, jid):
        params = {'client': 'runner', 'fun': 'jobs.exit_success', 'jid': jid}
        message = 'job_exit_success_api'
        return self.public(message, json=params)

    # 封装查询jid结果方法,使用的时候只要代入jid既可以
    def jid_api(self, jid):
        params = {'client': 'runner', 'fun': 'jobs.lookup_jid', 'jid': jid}
        message = 'jid_api'
        return self.public(message, json=params)

    # 封装archive.zip,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def archive_zip_api(self, tgt, arg):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'archive.zip', 'arg': arg}
        message = 'archive_zip_api'
        return self.public(message, json=params)

    # 封装archive.tar,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def archive_tar_api(self, tgt, arg):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'archive.tar', 'arg': arg}
        message = 'archive_tar_api'
        return self.public(message, json=params)

    # 封装cp.get_file,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def cp_get_file_api(self, tgt, arg):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'cp.get_file', 'arg': arg}
        message = 'cp_get_file_api'
        return self.public(message, json=params)

    # 封装cp.get_dir,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def cp_get_dir_api(self, tgt, arg):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'cp.get_dir', 'arg': arg}
        message = 'cp_get_dir_api'
        return self.public(message, json=params)

    # 封装salt-key -L
    def saltkey_listall_api(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        message = 'saltkey_listall_api'

        return self.public(message, json=params)

    def saltkey_delete_api(self, tgt):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': tgt}
        message = 'saltkey_delete_api'
        return self.public(message, json=params)

    # 接受salt-key的方法的include_rejected和include_denied就算设置为True也无效测试发现！！
    def saltkey_accept_api(self, tgt):
        parmas = {'client': 'wheel', 'fun': 'key.accept', 'match': tgt}
        message = 'saltkey_accept_api'
        return self.public(message, json=parmas)

    # 拒绝salt-key的方法奶奶的include_accepted和include_denied就算设置为True也无效测试发现！！
    def saltkey_reject_api(self, tgt):
        parmas = {'client': 'wheel', 'fun': 'key.reject', 'match': tgt}
        message = 'saltkey_reject_api'
        return self.public(message, json=parmas)

    # salt-run manage.status 查看minion在线离线状态，速度比较慢但是没BUG不像salt-run manage.alived
    def saltrun_manage_status_api(self, arg=None):
        params = {'client': 'runner', 'fun': 'manage.status', 'arg': arg}

        message = 'saltrun_manage_status_api'
        return self.public(message, json=params)

    # salt-run manage.alived 查看在线的minion，非常快速方便可惜有bug后来启用(而且可以带参数show_ipv4=True获取到和master通信的ip是什么，默认False)
    def saltrun_manage_alive_api(self, arg=None):
        params = {'client': 'runner', 'fun': 'manage.alived', 'arg': arg}
        message = 'saltrun_manage_alive_api'
        return self.public(message, json=params)

    # salt-run manage.not_alived 查看不在线的minion，非常快速方便可惜有bug后来启用
    def saltrun_manage_notalive_api(self, arg=None):
        params = {'client': 'runner', 'fun': 'manage.not_alived', 'arg': arg}
        message = 'saltrun_manage_notalive_api'
        return self.public(message, json=params)

    # 封装grains.items,使用的时候只要代入tgt即可，最多把tgt_type也代入
    def grains_items_api(self, tgt, tgt_type='glob'):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': tgt_type, 'fun': 'grains.items'}

        message = 'grains_items_api'
        return self.public(message, json=params)

    # 封装grains.item,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def grains_item_api(self, tgt, tgt_type='glob', arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': tgt_type, 'fun': 'grains.item', 'arg': arg}

        message = 'grains_item_api'
        return self.public(message, json=params)

    # 封装service.available查看服务是否存在Ture or False,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def service_available_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'service.available', 'arg': arg}
        message = 'service_available_api'
        return self.public(message, json=params)

    # 封装service.status查看启动服务状态,使用的时候只要代入tgt和arg即可，最多把tgt_type也代入
    def service_status_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'service.status', 'arg': arg}
        message = 'service_status_api'
        return self.public(message, json=params)

    # 封装service.start启动系统服务windows和linux通用，
    def service_start_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'service.start', 'arg': arg}
        message = 'service_start_api'
        return self.public(message, json=params)

    # 封装service.stop停止系统服务windows和linux通用，salt '*' service.stop <service name>，由于有发现停止成功但是返回结果是
    # 一堆错误提示，所以最好使用的时候最后做一步service.status，返回服务状态True说明启动，False说明停止了
    def service_stop_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'service.stop', 'arg': arg}

        message = 'service_stop_api'
        return self.public(message, json=params)

    # 封装ps.pgrep查看name的进程号windows和linux通用带模糊查询效果，
    def ps_pgrep_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'ps.pgrep', 'arg': arg}

        message = 'ps_pgrep_api'
        return self.public(message, json=params)

    # 封装ps.proc_info通过进程号查看详细信息，
    # {'client':'local', 'tgt':'id','fun':'ps.proc_info', 'arg':['pid=123','attrs=["cmdline","pid","name","status"]']}
    def ps_proc_info_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'ps.proc_info', 'arg': arg}

        message = 'ps_proc_info_api'
        return self.public(message, json=params)

    # 封装ps.kill_pid结束某个进程，{'client':'local','fun':'ps.kill_pid','tgt':'192.168.68.1', 'arg':['pid=11932']}
    def ps_kill_pid_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'ps.kill_pid', 'arg': arg}

        message = 'ps_kill_pid_api'
        return self.public(message, json=params)

    # 封装task.create_task创建windows计划任务，salt '192.168.68.1' task.create_task ooxx  action_type=Execute
    # cmd='"C:\ooxx\Shadowsocks.exe"' force=true execution_time_limit=False  user_name=administrator
    def task_create_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'task.create_task', 'arg': arg}
        message = 'task_create_api'
        return self.public(message, json=params)

    # 封装task.run启动windows计划任务，salt '192.168.100.171' task.run test1
    # ！坑！官方文档里命令是salt '192.168.100.171' task.list_run test1 根本就不行！
    def task_run_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'task.run', 'arg': arg}
        message = 'task_run_api'
        return self.public(message, json=params)

    # 封装task.stop启动windows计划任务，salt '192.168.100.171' task.run test1
    def task_stop_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'task.stop', 'arg': arg}
        message = 'task_stop_api'
        return self.public(message, json=params)

    # 封装file.mkdir,创建目录最后可以不需要/号，另一个file.makedirs则需要最后/，不然只创建到有/那一层这点也是可以利用的呵呵
    def file_mkdir_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.mkdir', 'arg': arg}

        message = 'file_mkdir_api'
        return self.public(message, json=params)

    # 封装file.makedirs,创建目录最后可以需要/号，不然只创建到有/那一层这点也是可以利用的呵呵,x相当于mkdir -p
    def file_makedirs_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.makedirs', 'arg': arg}

        message = 'file_makedirs_api'
        return self.public(message, json=params)

    # 封装file_exists,检查文件是否存在
    def file_exists_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.file_exists', 'arg': arg}
        message = 'file_exists_api'
        return self.public(message, json=params)

    # file_write_api(tgt='salt1',arg=('/root/test.text','word'))
    def file_write_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.append', 'arg': arg}
        message = 'file_write_api'
        return self.public(message, json=params)

    # 封装file.remove,移除文件，如果是目录则递归删除
    def file_remove_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.remove', 'arg': arg}
        message = 'file_remove_api'
        return self.public(message, json=params)

    # 封装file.directory_exists,检测目录是否存在返回True/False
    def file_directory_exists_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.directory_exists', 'arg': arg}
        message = 'file_directory_exists_api'
        return self.public(message, json=params)

    # 封装file.symlink,创建软连接
    def file_symlink_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'file.symlink', 'arg': arg}
        message = 'file_symlink_api'
        return self.public(message, json=params)

    # 封装supervisord.status,检测supervisor守护名称的状态，返回结果有这几种情况：
    # 1、没这个命令，salt需要安装supervisor才能用{'return': [{'192.168.100.171': "'supervisord.status' is not available."}]}
    # 2、没这个守护名称{'return': [{'192.168.68.50-master': {'1:': {'reason': '(no such process)', 'state': 'ERROR'}}}]}
    # 3、安装了supervisor但是没启动{'return': [{'192.168.100.170': {'unix:///var/run/supervisor/supervisor.sock': {'reason'
    # : 'such file', 'state': 'no'}}}]}
    # 4、正常获取结果的情况：
    # 启动{'return': [{'192.168.68.50-master': {'djangoproject.runserver': {'state': 'RUNNING', 'reason': 'pid 1233,
    #  uptime 1 day, 6:56:14'}}}]}
    # 停止{'return': [{'192.168.100.170': {'test': {'state': 'STOPPED', 'reason': 'Dec 13 05:23 PM'}}}]}
    def supervisord_status_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'supervisord.status', 'arg': arg}
        message = 'supervisord_status_api'
        return self.public(message, json=params)

    # 封装supervisord.stop,停止supervisor守护名称，返回结果除了上面status的前面3中情况还有以下几种情况：
    # 1、程序已经停止情况：{'return': [{'192.168.100.170': 'test: ERROR (not running)'}]}
    # 2、正常停止：{'return': [{'192.168.100.170': 'test: stopped'}]}
    # 3、没这个程序名称{'return': [{'192.168.100.170': 'test1: ERROR (no such process)'}]}
    def supervisord_stop_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'supervisord.stop', 'arg': arg}
        message = 'supervisord_stop_api'
        return self.public(message, json=params)

    # 封装supervisord.start,启动supervisor守护名称，返回结果有这几种情况：
    # 1、正常启动：{'return': [{'192.168.100.170': 'test: started'}]}
    # 2、已经启动过了{'return': [{'192.168.100.170': 'test: ERROR (already started)'}]}
    # 3、没这个程序名称{'return': [{'192.168.100.170': 'test1: ERROR (no such process)'}]}
    def supervisord_start_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'supervisord.start', 'arg': arg}
        message = 'supervisord_start_api'
        return self.public(message, json=params)

    # supervisord配置重载会启动新添加的程序
    def supervisord_update_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'supervisord.update', 'arg': arg}
        message = 'supervisord_update_api'
        return self.public(message, json=params)

    # 封装rsync.rsync同步命令
    def rsync_rsync_api(self, tgt, arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'rsync.rsync', 'arg': arg}
        message = 'rsync_rsync_api'
        return self.public(message, json=params)

    # 封装异步rsync.rsync同步命令
    def async_rsync_rsync_api(self, tgt, arg=None):
        params = {'client': 'local_async', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'rsync.rsync', 'arg': arg}
        message = 'async_rsync_rsync_api'
        return self.public(message, json=params)

    # 封装sys.doc查询模块帮助命令
    def sys_doc_api(self, tgt='*', arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'sys.doc', 'arg': arg}
        message = 'sys_doc_api'
        return self.public(message, json=params)

    # 封装sys.doc查询模块帮助命令
    def sys_runner_doc_api(self, tgt='*', arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'sys.runner_doc', 'arg': arg}
        message = 'sys_runner_doc_api'
        return self.public(message, json=params)

    # 封装sys.doc查询模块帮助命令
    def sys_state_doc_api(self, tgt='*', arg=None):
        params = {'client': 'local', 'tgt': tgt, 'tgt_type': 'glob', 'fun': 'sys.state_doc', 'arg': arg}
        message = 'sys_state_doc_api'
        return self.public(message, json=params)
