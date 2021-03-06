from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains= search_keywords)|Q(desc__icontains= search_keywords)|Q(detail__icontains= search_keywords))
        hot_courses = Course.objects.all().order_by('click_nums')[:3]
        #排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'click_nums':
                all_courses =all_courses.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html',{
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self,request, course_id):
        course = Course.objects.get(id = int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = Course.objects.all().order_by('-click_nums')[:1]
        has_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        return render(request, 'course-detail.html',{
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        #查询该用户是否学习过该课程
        user_studed_course = UserCourse.objects.filter(user = request.user, course = course)
        if not user_studed_course:
            user_studed_course = UserCourse(user=request.user, course = course)
            user_studed_course.save()
        # 获取学过该课程的用户id列表
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取列表中用户学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in= user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(course= course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resource':all_resource,
            'relate_courses':relate_courses,
        })


class CourseVideoView(View):
    def get(self, request, video_id, course_id):
        video = Video.objects.get(id = int(video_id))
        course = Course.objects.get(id=int(course_id))
        # 获取学过该课程的用户id列表
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取列表中用户学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'video': video,
            'course': course,
            'all_resource': all_resource,
            'relate_courses': relate_courses,
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        # 获取学过该课程的用户id列表
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取列表中用户学过的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        all_resource = CourseResource.objects.filter(course= course)
        all_comment = CourseComments.objects.filter(course=course).order_by('-add_time')
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resource': all_resource,
            'all_comment':all_comment,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登陆"}', content_type="application/json")
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id)>0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type="application/json")

