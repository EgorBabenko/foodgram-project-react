from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, F


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(blank=False, unique=True,
                              verbose_name='Email адрес',
                              help_text='Укажите email')

    first_name = models.CharField(max_length=30, blank=False, null=False,
                                  verbose_name='Имя',
                                  help_text='Укажите имя')

    last_name = models.CharField(max_length=30, blank=False, null=False,
                                 verbose_name='Фамилия',
                                 help_text='Укажите фамилию')

    sub_list = models.ManyToManyField('self',
                                      through='Following',
                                      through_fields=('follower', 'leader'),
                                      symmetrical=False,
                                      related_name='followers')

    def __str__(self):
        return self.username


class Following(models.Model):
    follower = models.ForeignKey(CustomUser,
                                 related_name='sub',
                                 on_delete=models.CASCADE,
                                 verbose_name='подписчик')

    leader = models.ForeignKey(CustomUser,
                               related_name='lead',
                               on_delete=models.CASCADE,
                               verbose_name='на кого подписан')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            # ограничение повторной одинаковой подписки
            models.UniqueConstraint(fields=['follower', 'leader'], name='un'),
            # ограничение подписки самого на себя
            models.CheckConstraint(check=~Q(follower__exact=F('leader')),
                                   name='selfsub')
        ]

    def __str__(self):
        return f'{self.follower} подписан на {self.leader}'
