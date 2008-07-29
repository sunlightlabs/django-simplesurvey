from django.contrib.auth.models import AnonymousUser

class Anonymous(AnonymousUser):
    
    def __init__(self):
        self.first_name = u"Anonymous"
        self.last_name = u"User"
        self.username = u"anonymous"
    
    def get_full_name(self):
        return u"Anonymous User"
        
ANONYMOUS_USER = Anonymous()