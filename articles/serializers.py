from rest_framework import serializers
from articles.models import Article, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Comment
        exclude = ("article",)


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    likes = serializers.StringRelatedField(many=True)
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Article
        fields = "__all__"
        
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comment_set_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comment_set_count(self, obj):
        return obj.comment_set.count()
    
    class Meta:
        model = Article
        fields = ("pk", "title", "image", "updated_at", "user", "likes_count", "comment_set_count")
    

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "image", "content")
        
        
        

        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)  # 들어있는데 핃드가 1개라도 콤마 필수