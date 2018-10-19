from django.db import models
from datetime import datetime
# Create your models here.
# minion客户端信息表
class MinionList(models.Model):
    minion_id = models.CharField(max_length=20, verbose_name='MinionID', primary_key=True)
    ip = models.CharField(verbose_name='IP地址',blank=True,null=True,max_length=128)
    minion_version = models.CharField(max_length=20, verbose_name='Minion版本', blank=True, null=True)
    system_type = models.CharField(max_length=200, verbose_name='系统类型', blank=True, null=True)
    sys = models.CharField(max_length=32,verbose_name='系统版本', blank=True, null=True)
    cpu_info = models.CharField(max_length=128,verbose_name='CPU信息', blank=True, null=True)
    hostname = models.CharField(max_length=200, verbose_name='主机名', blank=True, null=True)
    memory = models.IntegerField(verbose_name='内存大小', blank=True, null=True)
    ctime = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    utime = models.CharField(max_length=50, verbose_name='最近一次更新时间', blank=True, null=True)
    minion_status = models.CharField(max_length=50, verbose_name='Minion状态', blank=True, null=True)
    des = models.CharField(max_length=200, verbose_name='描述备注', blank=True, null=True)

    class Meta:
        verbose_name = 'Minion列表'
        verbose_name_plural = verbose_name
        ordering = ['minion_id']

    def __str__(self):
        return self.minion_id

    # salt-key信息表


class SaltKeyList(models.Model):
    minion_id = models.CharField(max_length=20, verbose_name='MinionID')
    certification_status = models.CharField(max_length=20, verbose_name='认证状态')
    utime = models.CharField(max_length=50, verbose_name='最近一次更新时间', blank=True, null=True)

    class Meta:
        verbose_name = 'Salt-key信息表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.id)

    # salt命令集信息表


class SaltCmdInfo(models.Model):
    salt_cmd = models.CharField(max_length=100, verbose_name='命令')
    salt_cmd_type = models.CharField(max_length=20, verbose_name='类型', blank=True, null=True)
    salt_cmd_module = models.CharField(max_length=200, verbose_name='模块', blank=True, null=True)
    salt_cmd_source = models.CharField(max_length=200, verbose_name='命令来源', blank=True, null=True)
    salt_cmd_doc = models.TextField(verbose_name='命令帮助信息', blank=True, null=True)
    ctime = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    utime = models.CharField(max_length=50, verbose_name='最近一次采集时间', blank=True, null=True)
    des = models.TextField(verbose_name='描述备注', blank=True, null=True)

    class Meta:
        # 复合主键其实就是联合唯一索引,因为必须2个判断唯一，另外这样会自动生成ID主键
        unique_together = ("salt_cmd", "salt_cmd_type")
        verbose_name = 'salt命令集表'
        verbose_name_plural = verbose_name
        ordering = ['salt_cmd_type', 'salt_cmd']

    def __str__(self):
        return self.salt_cmd
