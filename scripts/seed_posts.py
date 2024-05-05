import faker
from random import randint
from apps.authentication.models import Profile
from apps.post.models import Post, PostMedia
from os import listdir, path


faker = faker.Faker()
def run():
  randomMedia = listdir('media\post_media_faker')
  # mediaPath =  + r"\\media\\post_media_faker\\"
  all_profiles = Profile.objects.all()
  for post in range(1012):
    random = randint(0, len(all_profiles) - 1)
    PostFaker = Post.objects.create(
      created_by = all_profiles[random],
      post_text = faker.text()
    )
    for random_images in range(1, randint(1, 4)):
      PostMedia.createPostMedia(Post=PostFaker, Path= r"/media/post_media_faker/" + randomMedia[randint(0, len(randomMedia) - 1)])