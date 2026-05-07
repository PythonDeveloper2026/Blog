import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment
from users.models import Profile, Notification
from faker import Faker

class Command(BaseCommand):
    help = 'Ma\'lumotlar bazasini test ma\'lumotlari bilan to\'ldiradi'

    def handle(self, *args, **kwargs):
        fake = Faker(['uz_UZ', 'en_US'])
        
        self.stdout.write('Foydalanuvchilar yaratilmoqda...')
        users = []
        for _ in range(10):
            username = fake.user_name()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                users.append(user)
        
        all_users = list(User.objects.all())
        
        self.stdout.write('Postlar yaratilmoqda...')
        tags_pool = ['texnologiya', 'dasturlash', 'python', 'django', 'sayohat', 'taomlar', 'sport', 'yangiliklar', 'shaxsiy', 'rivojlanish']
        
        for user in all_users:
            for _ in range(random.randint(3, 8)):
                title = fake.sentence(nb_words=6)
                content = "\n\n".join(fake.paragraphs(nb=5))
                post = Post.objects.create(
                    title=title,
                    content=f'<h3>{title}</h3><p>{content}</p>',
                    author=user,
                    status='published'
                )
                # Random tags
                random_tags = random.sample(tags_pool, random.randint(1, 3))
                post.tags.add(*random_tags)
                
                # Random likes
                likers = random.sample(all_users, random.randint(0, len(all_users)//2))
                post.likes.set(likers)
        
        self.stdout.write('Izohlar yaratilmoqda...')
        all_posts = list(Post.objects.all())
        for post in all_posts:
            for _ in range(random.randint(0, 5)):
                commenter = random.choice(all_users)
                Comment.objects.create(
                    post=post,
                    author=commenter,
                    content=fake.paragraph()
                )
        
        self.stdout.write('Obunalar (Follows) yaratilmoqda...')
        for user in all_users:
            # Obuna bo'lish
            to_follow = random.sample(all_users, random.randint(1, 5))
            for f_user in to_follow:
                if user != f_user:
                    f_user.profile.followers.add(user)

        self.stdout.write(self.style.SUCCESS('Ma\'lumotlar bazasi muvaffaqiyatli to\'ldirildi!'))
