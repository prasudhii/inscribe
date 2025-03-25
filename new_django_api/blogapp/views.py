from django.shortcuts import render
from .models import Blog
from django.contrib.auth import get_user_model
from blogapp.serializers import UpdateUserProfileSerializer, UserRegistrationSerializer,BlogSerializer,UserInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class BlogListPagination(PageNumberPagination):
    page_size = 3  # Number of results per page

@api_view(['GET']) 
def blog_list(request):
    blogs = Blog.objects.all()
    paginator = BlogListPagination()
    paginated_blogs = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(paginated_blogs, many=True)
    return paginator.get_paginated_response(serializer.data)


# @api_view(['GET'])
# def blog_list(request):
#     blogs = Blog.objects.all()
#     paginator = BlogListPagination()
#     paginated_blogs = paginator.paginate_queryset(blogs, request)

#     if paginated_blogs is None:
#         return Response({"error": "Pagination did not apply!"}, status=400)

#     serializer = BlogSerializer(paginated_blogs, many=True)
#     return paginator.get_paginated_response(serializer.data)







@api_view(['GET'])
def get_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)






@api_view(["POST"])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user 
    serializer = UpdateUserProfileSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user=request.user
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data)
    return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)



# @api_view(["GET"])
# def blog_list(request):
#     blogs = Blog.objects.all()
#     serializer = BlogSerializer(blogs, many=True)
#     return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blog(request, pk):
    user = request.user 
    blog = Blog.objects.get(id=pk)
    if blog.author != user:
        return Response({"error": "You are not the author of this blog"}, status=403)
    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_blog(request, pk):
    user = request.user 
    blog = Blog.objects.get(id=pk)
    if blog.author != user:
        return Response({"error": "You are not the author of this blog"}, status=403)
    blog.delete()
    return Response({"message":"Blog deleted succesfully"},status=status.HTTP_204_NO_CONTENT)



from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


@api_view(['GET'])
def get_userinfo(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    serializer = UserInfoSerializer(user)
    return Response(serializer.data)





@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    username = user.username
    return Response({"username": username})