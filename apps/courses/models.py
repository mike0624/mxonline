# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名称')
    detail = UEditorField(verbose_name =u'课程详情',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/", default = '')
    desc = models.TextField(verbose_name=u'描述')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否首页轮播显示')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), verbose_name=u'课程难度',max_length=5)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/m', verbose_name=u'封面图')
    category = models.CharField(default=u'',max_length=20, verbose_name=u'课程类型')
    tag = models.CharField(default=u'', max_length=10, verbose_name=u'标签')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = u'课程章节数'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_zj(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节名称')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    url = models.CharField(max_length=200, default=u'', verbose_name=u'视频链接')
    video_time = models.CharField(max_length=10, default=0, verbose_name=u'课程时长')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程资源名称')
    download = models.FileField(upload_to='course/resources/%Y/m', verbose_name=u'下载地址', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
