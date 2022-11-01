from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import  User
from articles.models import Article
from faker import Faker
from articles.serializers import ArticleSerializer
# 이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile # 임시파일 생성

def get_temporary_image(temp_file): # 임시 파일을 생성하여 이를 이용해 임시 이미지를 생성
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png') # tempt_file이라는 폴더를 가져와서 양식만 png로 변경 후 이미지 저장
    return temp_file
    

class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email':'john@naver.com', 'password':'johnpassword'}
        cls.article_data = {'title':'some title', 'content':'some content'}
        cls.user = User.objects.create_user('john@naver.com', 'johnpassword')
        
    def setUp(self):
        print()
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data["access"]    

    # def setUp(self):
    #     self.user_data = {'email':'test@naver.com', 'password':'test'}
    #     self.article_data = {'title':'title', 'content':'hi'}
    #     self.user = User.objects.create_user('test@naver.com', 'test')
    #     self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access'] # .client가 클래스메소드가 아니기 때문에 cls.client를 하면 오류가 나기 때문에 이 부분만 setup으로 
        

    def test_fail_if_not_logged_in(self): #테스트 함수에는 무조건 앞에 test를 붙이기! 
        url = reverse('article_view')
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)
        
    def test_create_article(self):
        response = self.client.post(
            path=reverse("article_view"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        # self.assertEqual(response.data["message"], "글 작성 완료!")
        self.assertEqual(response.status_code, 200)
        
    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        # 여기까지가 이미지 파일 생성
        image_file.seek(0) #이미지의 첫 번째 프레임 받아오기
        self.article_data["image"] = image_file
        
        # 전송
        response = self.client.post(
            path=reverse("article_view"),
            data = encode_multipart(data = self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        
        
class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.articles.append(Article.objects.create(title=cls.faker.sentence(), content=cls.faker.text(), user=cls.user))
            
    def test_get_article(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = ArticleSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value) # response.data에서 돌아온 데이터에 대해 가지고 있는 key값을 넣으면 그에 대한 value값이 나오게