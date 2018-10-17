from django.db import models

# Create your models here.
class Menu(models.Model):
    parent_menus = models.ForeignKey('self', blank=True, null=True, related_name='parent_menu')
    name = models.CharField(max_length=30,verbose_name="菜单名称")
    path = models.CharField(max_length=100,verbose_name="菜单地址")
    icon = models.CharField(max_length=128,verbose_name=u'菜单图标')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u'菜单'
        verbose_name_plural = verbose_name