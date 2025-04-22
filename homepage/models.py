import os
from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from tinymce.models import HTMLField
BASE_DIR = Path(__file__).resolve().parent.parent
class Mylogo(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    mylogo=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'My logo'
    
    def __str__(self):
        return self.title

class Image_news(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'News Image'
    
    def __str__(self):
        return self.title
    
class Image_contact(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Contact Image'
    
    def __str__(self):
        return self.title
    
class Image_primaryschool(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Primary School Image'
    
    def __str__(self):
        return self.title
    
class Image_login(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Login Image'
    
    def __str__(self):
        return self.title
    
class Image_register(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Register Image'
    
    def __str__(self):
        return self.title

class Image_t_c(models.Model):
    title = models.CharField(max_length=1000,null=True,blank=True)   
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Terms & Conditions Image'
    
    def __str__(self):
        return self.title
    
class Partnership(models.Model):
    title=models.CharField(max_length=1000,null=True,blank=True)
    image=models.CharField(max_length=1000,null=True,blank=True)
    class Meta:
        verbose_name_plural = 'Partnership'
        
    def __str__(self):
        return self.title

class Terms_and_Conditions(models.Model):
    title=models.CharField(max_length=1000,default='T_C')
    content=HTMLField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'Terms and Conditions'
        
    def __str__(self):
        t_c='Terms and Conditions'
        return t_c
class my_purchases(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    videos_url=models.CharField(max_length=500,null=True,blank=True)
    book_title=models.TextField(null=True,blank=True,max_length=1000)
    chapter=models.CharField(max_length=500,null=True,blank=True)
    part=models.CharField(max_length=500,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    price=models.DecimalField(max_digits = 5,decimal_places = 2,null=True,blank=True)
    image=models.ImageField(null=True,blank=True,max_length=1000)
class add_basket(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    videos_url=models.CharField(max_length=500,null=True,blank=True)
    chapter=models.CharField(max_length=500,null=True,blank=True)
    part=models.CharField(max_length=500,null=True,blank=True)
    image=models.ImageField(null=True,blank=True,max_length=1000)
    book_title=models.TextField(null=True,blank=True,max_length=1000)
    price=models.DecimalField(max_digits = 5,decimal_places = 2,null=True,blank=True)
    
class display_video(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    book_title=models.TextField(null=True,blank=True,max_length=1000)
    chapter=models.CharField(max_length=500,null=True,blank=True)
    part=models.CharField(max_length=500,null=True,blank=True)
    watch=models.BooleanField(default=False)
    display_date = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=8, default="0:00:00")

class Success_logo(models.Model):
    class Made_in(models.TextChoices):
        
        Λογότυπο='logo'
        
    
    #def get_field_image(self,filename):
        
        #a='images'
        #b='mylogo'
        
        #store="{0}/{1}/{2}".format(a,b,filename)
        
        #dirname=store
        
        #if not os.path.exists(store):
            #os.path.join(BASE_DIR,store)     
        #return dirname
    
    def save(self, *args, **kwargs):
        a='success_logo'
        self.title=a
        super(Success_logo, self).save(*args, **kwargs)
    title = models.CharField(max_length=1000,null=True,blank=True, editable=False)   
    Success_logo=models.CharField(max_length=1000,null=True,blank=True)
    #Success_logo=models.ImageField(upload_to=get_field_image,null=True,blank=True,max_length=1000)
    
    class Meta:
        verbose_name_plural = 'Success_logo'
    
    def __str__(self):
        logo='Success_logo'
        return logo

class Books_Images(models.Model):
    
    class LevelType(models.TextChoices):
        Δημοτικό= 'primary'
        Γυμνάσιο= 'secondary'
        Λύκειο = 'high'
        
    class ClassType(models.TextChoices):   
        Πρώτη='first'
        Δεύτερα='second'
        Τρίτη='thirth'
        Τετάρτη='fourth'
        Πέμπτη='fifth'
        Έκτη='sixth'
        
    class LessonType(models.TextChoices):    
        Ελληνικά='greek'
        Μαθηματικά='math'
        Βιολογία='biology'
        Φυσική='physics'
        Χημεία='chistry'
        Πληροφορική='pliroforiki'
        Γραμματική='grammar'
        Δραστηριότητες='drastiriotites'
        
    class Book_issue(models.TextChoices):
        
        Πρώτο_Τεύχος='first_issue'
        Δεύτερο_Τεύχος='second_issue'
        Τρίτο_Τεύχος='thirth_issue'
        Τέταρτο_Τεύχος='fourth_issue'
        Πέμπτο_Τεύχος='fifth_issue'
        Έκτο_Τεύχος='sixth_issue'
        
    class Book_type(models.TextChoices):
        
        Βιβλίο_Μαθητή='mathiti'
        Βιβλίο_Εργασιών='ergasion'
        Γραμματική='grammar'
        Δραστηριοτήτων='drastiriotiton'
        
        
    class Made_in(models.TextChoices):
        
        Ελληνικό='gr'
        Κυπριακό='cy'
        
    
    #def get_field_image(self,filename):
        
        #a=self._meta.get_field('stage').value_from_object(self)
        #b=self._meta.get_field('level').value_from_object(self)
        #c=self._meta.get_field('topic').value_from_object(self)
        
        #store=os.path.join("images/{0}{1}/{2}/{3}".format(a,b,c,filename))
        
        #dirname=store
        
        #if not os.path.exists(store):
            #os.path.join(BASE_DIR,store)     
        #return dirname 
           
    def save(self, *args, **kwargs):
        a = self.LevelType(self.stage).value[0:3]
        b = self.ClassType(self.level).value[0:3]
        c = self.LessonType(self.topic).value[0:3]
        d = self.Book_issue(self.book_issue).value[0:3]
        e = self.Book_type(self.book_type).value[0:3]
        f = self.Made_in(self.book_made_in).value[0:3]
        if self.stage=='primary':
            self.sort='a'
        elif self.stage=='secondary':
            self.sort='b'
        elif self.stage=='high':
            self.sort='c'
        self.ref_code_book=a+'_'+b+'_'+c+'_'+d+'_'+e+'_'+f
        self.ref_code=a+'_'+b+'_'+c
        super(Books_Images, self).save(*args, **kwargs)
    sort = models.CharField(max_length=1000,null=True,blank=True, editable=False)    
    ref_code = models.CharField(max_length=1000,null=True,blank=True, editable=False)   
    ref_code_book = models.CharField(max_length=1000,null=True,blank=True, editable=False)#max_length=200,null=True,blank=True
    stage = models.TextField(max_length=300,choices=LevelType.choices,default=LevelType.Δημοτικό)
    level= models.TextField(max_length=300,choices=ClassType.choices,default=ClassType.Πρώτη)
    topic= models.TextField(max_length=300,choices=LessonType.choices,default=LessonType.Ελληνικά)
    book_issue=models.CharField(max_length=500,choices=Book_issue.choices,default=Book_issue.Πρώτο_Τεύχος)
    book_type=models.CharField(max_length=500,choices=Book_type.choices,default=Book_type.Βιβλίο_Μαθητή)
    book_made_in=models.CharField(max_length=100,choices=Made_in.choices,default=Made_in.Ελληνικό)
    book_title=models.CharField(max_length=500)
    content=HTMLField(null=True,blank=True)
    image=models.CharField(max_length=1000,null=True,blank=True)
    book=models.CharField(max_length=1000,null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Books Images'
        ordering = ['-sort']
    
    def __str__(self):
        return self.stage + '|'+str(self.level)  + '|'+str(self.topic)+ '|' + str(self.book_type) + '|' + str(self.book_issue) + '|' + str(self.book_title)

class Videos(models.Model):
    
    class LevelType(models.TextChoices):
        Δημοτικό = 'primary'
        Γυμνάσιο = 'secondary'
        Λύκειο = 'high'
        
    class ClassType(models.TextChoices):   
        Πρώτη='first'
        Δεύτερα='second'
        Τρίτη='thirth'
        Τετάρτη='fourth'
        Πέμπτη='fifth'
        Έκτη='sixth'
        
    class LessonType(models.TextChoices):    
        Ελληνικά='greek'
        Μαθηματικά='math'
        Βιολογία='biology'
        Φυσική='physics'
        Χημεία='chistry'
        Πληροφορική='pliroforiki'
      
    class Book_issue(models.TextChoices):
        
        Πρώτο_Τεύχος='first_issue'
        Δεύτερο_Τεύχος='second_issue'
        Τρίτο_Τεύχος='thirth_issue'
        Τέταρτο_Τεύχος='fourth_issue'
        Πέμπτο_Τεύχος='fifth_issue'
        
    class part(models.TextChoices):
        
        Ένα_Video=' '
        Πρώτο_Μέρος='- 1o Μέρος'
        Δεύτερο_Μέρος='- 2o Μέρος'
        Τρίτο_Μέρος='- 3o Μέρος'
        Τέταρτο_Μέρος='- 4o Μέρος'
        Πέμπτο_Μέρος='- 5o Μέρος'
        Έκτο_Μέρος='- 6o Μέρος'
        Έβδομο_Μέρος='- 7o Μέρος'
        Όγδοο_Μέρος='- 8o Μέρος'
        Ένατο_Μέρος='- 9o Μέρος'
        
    class Book_type(models.TextChoices):
        
        Βιβλίο_Μαθητή='mathiti'
        Βιβλίο_Εργασιών='ergasion'
        
    class Made_in(models.TextChoices):
        
        Ελληνικό='gr'
        Κυπριακό='cy'
    
    #class Sorting(models.IntegerChoices):
        #Πρώτο = 1
        #Δεύτερο = 2
        #Τρίτο = 3
        #Τέταρτο = 4
        #Πέμπτο=5
        #Έκτο=6
        #Έβδομο=7
        #Όγδοο=8
        #Ένατο=9
        #Δέκατο=10
        #Εντέκατο=11
        #Δωδέκατο=12
        #Δέκατοτρίτο=13
        #Δέκατοτέταρο=14
        
    
    #def get_field(self,filename):
        #a=self._meta.get_field('stage').value_from_object(self)
        #b=self._meta.get_field('level').value_from_object(self)
        #c=self._meta.get_field('topic').value_from_object(self)
        #d=self._meta.get_field('book_issue').value_from_object(self)
        
        #store=os.path.join("videos/{0}{1}/{2}/{3}/{4}".format(a,b,c,d,filename))
        #dirname=store
        #if not os.path.exists(store):
            #os.path.join(BASE_DIR,store)
        #return dirname

    def save(self, *args, **kwargs):
        a = self.LevelType(self.stage).value[0:3]
        b = self.ClassType(self.level).value[0:3]
        c = self.LessonType(self.topic).value[0:3]
        d = self.Book_issue(self.book_issue).value[0:3]
        e = self.Book_type(self.book_type).value[0:3]
        f = self.Made_in(self.book_made_in).value[0:3]

        self.ref_code=a+'_'+b+'_'+c
        self.ref_code_video=a+'_'+b+'_'+c+'_'+d+'_'+e+'_'+f
        super(Videos, self).save(*args, **kwargs)
        
    ref_code = models.CharField(max_length=1000,null=True,blank=True, editable=False)
    ref_code_video = models.CharField(max_length=1000,null=True,blank=True, editable=False)
    stage = models.CharField(max_length=20, choices=LevelType.choices, default=LevelType.Δημοτικό)
    level = models.CharField(max_length=20, choices=ClassType.choices, default=ClassType.Πρώτη)
    topic= models.TextField(max_length=300,choices=LessonType.choices,default=LessonType.Ελληνικά)
    book_issue=models.CharField(max_length=500,choices=Book_issue.choices,default=Book_issue.Πρώτο_Τεύχος)
    book_type=models.CharField(max_length=500,choices=Book_type.choices,default=Book_type.Βιβλίο_Μαθητή)
    book_made_in=models.CharField(max_length=100,choices=Made_in.choices,default=Made_in.Ελληνικό)
    part_title=models.CharField(max_length=1000,null=True,blank=True)
    chapter_title=models.CharField(max_length=1000,null=True,blank=True)
    part_video=models.TextField(max_length=1000,choices=part.choices,default=part.Ένα_Video)
    sorting_video = models.IntegerField(null=True,blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    #primary_video=models.CharField(max_length=1000,null=True,blank=True)#
    video=models.CharField(max_length=1000,null=True,blank=True)#
    what_includes=models.TextField(max_length=500,null=True,blank=True)
    #video=models.FileField(upload_to=get_field,null=True,blank=True)#
    created_date = models.DateTimeField(auto_now_add=True)
    views=models.IntegerField(default=0,editable=False)
            
    class Meta:

        verbose_name_plural = 'Videos'
        ordering = ['stage', 'sorting_video']
    
    def __str__(self):
        return self.stage + self.level + '|'+str(self.topic) + '|' + str(self.book_type) + '|' + str(self.chapter_title)+ '|' + str(self.sorting_video) + '|' + str(self.created_date)

class Price_list(models.Model):
    
    class LevelType(models.TextChoices):
        Δημοτικό= 'primary'
        Γυμνάσιο= 'secondary'
        Λύκειο = 'high'
         
        
    class ClassType(models.TextChoices):   
        Πρώτη='first'
        Δεύτερα='second'
        Τρίτη='thirth'
        Τετάρτη='fourth'
        Πέμπτη='fifth'
        Έκτη='sixth'
        
    class LessonType(models.TextChoices):    
        Ελληνικά='greek'
        Μαθηματικά='math'
        Βιολογία='biology'
        Φυσική='physics'
        Χημεία='chistry'
        Πληροφορική='pliroforiki'
        
    class Book_issue(models.TextChoices):
        
        Πρώτο_Τεύχος='first_issue'
        Δεύτερο_Τεύχος='second_issue'
        Τρίτο_Τεύχος='thirth_issue'
        Τέταρτο_Τεύχος='fourth_issue'
        Πέμπτο_Τεύχος='fifth_issue'
        
    class Book_type(models.TextChoices):
        
        Βιβλίο_Μαθητή='mathiti'
        Βιβλίο_Εργασιών='ergasion'
        
    class Made_in(models.TextChoices):
        
        Ελληνικο='gr'
        Κυπριακό='cy'
        
    def get_field(self):
        a=self._meta.get_field('stage').value_from_object(self)
        b=self._meta.get_field('level').value_from_object(self)
        c=self._meta.get_field('topic').value_from_object(self)
        d=self._meta.get_field('book_issue').value_from_object(self)
        
        return a+'/'+b+'/'+c+'/'+d+'/'
    
    def save(self, *args, **kwargs):
        a=self.stage[0:3]
        b=self.level[0:3]
        c=self.topic[0:3]
        d=self.book_issue[0:3]
        e=self.book_type[0:3]
        f=self.book_made_in

        self.ref_code_video=a+'_'+b+'_'+c+'_'+d+'_'+e+'_'+f
        super(Price_list, self).save(*args, **kwargs)
        
   
    ref_code_video = models.CharField(max_length=1000,null=True,blank=True, editable=False)
    stage = models.TextField(max_length=300,choices=LevelType.choices,default=LevelType.Δημοτικό)
    level= models.TextField(max_length=300,choices=ClassType.choices,default=ClassType.Πρώτη)
    topic= models.TextField(max_length=300,choices=LessonType.choices,default=LessonType.Ελληνικά)
    book_issue=models.CharField(max_length=500,choices=Book_issue.choices,default=Book_issue.Πρώτο_Τεύχος)
    book_type=models.CharField(max_length=500,choices=Book_type.choices,default=Book_type.Βιβλίο_Μαθητή)
    book_made_in=models.CharField(max_length=100,choices=Made_in.choices,default=Made_in.Ελληνικο)
    title=models.CharField(max_length=500)
    price_chapter=models.DecimalField(max_digits = 5,decimal_places = 2,null=True,blank=True)
    price_all_book=models.DecimalField(max_digits = 5,decimal_places = 2,null=True,blank=True)
            
    class Meta:

        verbose_name_plural = 'Price_list'
        ordering = ['stage']
    
    def __str__(self):
        return self.stage + self.level + '|'+str(self.topic) + '|' + str(self.book_type) + '|' + str(self.title)



