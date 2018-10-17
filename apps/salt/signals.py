# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import SaltKeyList,MinionList
import time
import logging

logger = logging.getLogger('oms.views')

# 在操作saltkey表的保存时候同时对minion管理表做创建或更新操作
@receiver(post_save,sender = SaltKeyList,dispatch_uid ="saltkey_list_post_save")
def create_minion_list(sender,instance,created,update_fields,**kwargs):
    if created and instance.certification_status =='accepted':
        update_values = {'minion_id':instance.minion_id,'minion_status':'在线','utime':time.strftime('%Y年%m月%d日 %X')}
        MinionList.objects.update_or_create(minion_id=instance.minion_id,defaults=update_values)

# 在操作saltkey表的删除时候同时对minion管理表做删除操作
@receiver(post_delete, sender=SaltKeyList, dispatch_uid="saltkey_list_post_delete")
def delete_minion_list(sender, instance, **kwargs):
    if instance.certification_status == 'accepted':
        MinionList.objects.filter(minion_id=instance.minion_id).delete()