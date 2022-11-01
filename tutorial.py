# from faker import Faker


# faker = Faker() # 영어
# faker = Faker("ko_KR") # 한국어(name만 된다.)

# print(faker.name()) # 랜덤한 이름
# print(faker.first_name()) 
# print(faker.last_name())
# print(faker.word()) # 랜덤한 단어
# print(faker.sentence()) # 랜덤한 한 문장
# print(faker.text()) # 랜덤한 긴 문장


my_dict = {"뭔가 키값": "뭔가 벨류값", "some key":"some value", "name":"young"}

for key, value in my_dict.items():
    print(key)
    print(value)