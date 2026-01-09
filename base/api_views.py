from rest_framework import viewsets, permissions,filters
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Category, Blog, Comment
from .serializers import CategorySerializer, BlogSerializer, CommentSerializer, RegisterSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.permissions import IsOwnerOrReadOnly,IsAdminOrReadOnly

# Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Categories: normal users can view only category but cannot perform others operations.
class CategoryApiView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# Blogs
class BlogApiView(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # Enable search and filter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'blog_body']          # search by title or blog content
    filterset_fields = ['category', 'author']      # filter by category or author

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Comments
class CommentApiView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# for logout functionality.
class ApiLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Successfully logged out"},
            status=status.HTTP_200_OK
        )