from django.db import models
from user.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    likes = models.ManyToManyField(User, related_name="like_articles") #manytomany 필드는 related_name을 설정안하면 이름이 중복되기 때문에 꼭 설정을 해주어야 한다!!
    
    def __str__(self):
        return str(self.title)
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_set") # 역으로 참조할 때에는 related_name 사용, related_name="comment_set"은 디폴트 값이어서 작성 안해줘도 있는것으로 인식된다.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return str(self.content)