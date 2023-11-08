from Game.models import Player
from django.db import models
import json, re, os


class UserManager(models.Manager):
    def __init__(self) -> None:
        super().__init__()
        
        self.errors = []
        with open(os.path.join(os.getcwd(), "Login", "error_codes.json"), "r") as f:
            self.error_codes = json.load(f)


    def is_valid(self, username, password):

        if len(username) < 8:
            self.errors.append(self.error_codes["3"])
        
        if len(password) < 8:
            self.errors.append(self.error_codes["4"])

        s_pattern = r"[!@#$%^&*(),.?:{}|<>]"
        d_pattern = r".*\d.*"
        u_pattern = r".*[A-Z].*"
        l_pattern = r".*[a-z].*"
        if not re.match(s_pattern, password)\
            or not re.match(d_pattern, password)\
            or not re.match(u_pattern, password)\
            or not re.match(l_pattern, password):
            
            self.errors.append(self.error_codes["5"])
        

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30, unique=True)
    whole_money = models.IntegerField(max_length=50)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, 
                                  related_name="main_user")

    manager = UserManager()
    manager.is_valid(username.__str__(), password.__str__())


        
