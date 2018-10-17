from django.db import models
from datetime import datetime
# Create your models here.

class Assets(models.Model):

    ASSET_STATUS = (
        (1,'上线'),
        (2,'下线')
    )
    ASSET_TYPE = (
        (1, '物理机'),
        (2, '虚拟机'),
        (3, '云主机')
    )
    hostname = models.CharField(max_length=32,verbose_name=u'主机名')
    server_type = models.SmallIntegerField(choices=ASSET_TYPE,default=3,verbose_name=u'服务器类型')
    wip = models.GenericIPAddressField(verbose_name=u'外网地址',blank=True,null=True)
    nip = models.GenericIPAddressField(verbose_name=u'内网地址',blank=True,null=True)
    status = models.SmallIntegerField(choices=ASSET_STATUS,default=2,verbose_name=u'状态')
    instance_id = models.CharField(max_length=64,verbose_name=u'云服务器id',blank=True,null=True)
    sn = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'SN编号')
    cpu_info = models.CharField(verbose_name=u'cpu信息',max_length=128,blank=True,null=True)
    os = models.CharField(verbose_name=u'系统类型',blank=True,null=True,max_length=64)
    memory = models.SmallIntegerField(verbose_name=u'内存/GB',blank=True,null=True)
    disk = models.IntegerField(verbose_name=u'硬盘/GB',blank=True,null=True)
    ctime = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    utime = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    idc = models.ForeignKey('IDC', verbose_name=u'机房',blank=True,null=True)
    role = models.ManyToManyField('Tag',verbose_name=u'标签',blank=True,null=True)
    business_unit = models.ForeignKey('BusinessUnit',verbose_name=u'业务线',blank=True,null=True)
    desc = models.CharField(max_length=200, verbose_name=u'描述',blank=True,null=True)
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.wip

class BusinessUnit(models.Model):
    """业务线"""

    parent_unit = models.ForeignKey('self', blank=True, null=True, related_name='parent_level')
    name = models.CharField(u'业务线', max_length=64, unique=True)
    desc = models.CharField(u'备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"


class RemoteUser(models.Model):
    name = models.CharField(max_length=24,verbose_name=u'名称')
    username = models.CharField(max_length=12, verbose_name=u'用户名')
    password = models.CharField(max_length=64, verbose_name=u'密码')
    businessunit = models.ForeignKey(BusinessUnit, verbose_name=u'业务线')

    class Meta:
        verbose_name = u'远程用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(max_length=64, verbose_name=u'机房名')
    ctime = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    desc = models.CharField(max_length=128, verbose_name=u'描述', default='')

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=32,verbose_name=u'角色')
    ctime = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    desc = models.CharField(max_length=128,default='',verbose_name=u'描述')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u'类型'
        verbose_name_plural = verbose_name

