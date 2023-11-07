from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    class Meta:
        app_lable = 'myapp'


    def update_rating(self):
        postRat = self.post_set.all().aggrigate(postRating=Sum('rating'))
        pRat += postRat.get('postRating')
        
        commentRat = self.authorUser.comment_set.all().aggrigate(commentRat = Sum('rating'))
        cRat = 0
        cRat += commentRat('commentRating')

        self.ratingAuthor = pRat*3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)#Не очень длинные тексты

    
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS,'Новость')
        (ARTICLE,'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DataTimeField(auto_now_add=True)
    postCategory = models.ManyToMany(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.smallIntegerField(default = 0)
    numberOfDiscusions = models.smallIntegerField(default = 0)

    

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

   
class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DataTimeField(auto_now_add=True)
    rating = models.smallIntegerField(default=0)

    

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    
    def __str__(self):
        return self.commentUser.username 
    
    def reply(self):
        self.numberOfDiscusions +=1
        self.save()

# Create your models here.
