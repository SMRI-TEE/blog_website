from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # migrations converts class to sql query
    
    # define plural name of a model, default is categorys, (wrong english)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
  
    def __str__(self):
        return self.category_name
  
  
STATUS_CHOICE =   (
    (0, 'Draft'),
    (1, 'Published'),
)      
class Blog(models.Model):
    title = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE) # category delete then blogs delete.
    author =  models.ForeignKey(User,on_delete=models.CASCADE) # author means writer who wrote the blog post.(links each blog to one registered user.)
    blog_image = models.ImageField(upload_to='uploads/%y/%m/%d') # uploads/year/month/date (yo path ma store hunxa)
    short_description = models.TextField(max_length=1500)
    blog_body = models.TextField(max_length=3000)
    status = models.IntegerField(choices= STATUS_CHOICE,default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
  

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE) 
    comment = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment
    