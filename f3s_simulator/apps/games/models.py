# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from f3s_simulator.apps.maps.models import Map
from f3s_simulator.libs.models import CommonModel

class Game(CommonModel):
    """
    Fire simulation. In terms of game dev - game.
    """
    map = models.ForeignKey(Map, related_name='games')
    owner = models.ForeignKey(User, related_name='created_games')
    players = models.ManyToManyField(User, related_name='played_games')



class Step(CommonModel):
    """
    Simulation step.
    """
    game = models.ForeignKey(Game, related_name='steps')
    index = models.IntegerField(_('step number'), default=0, editable=False)

    def __unicode__(self):
        return '%d step of %s''s game on %s map' % (self.index, self.game.owner.username, self.game.map.name)

    def save(self, force_insert=False, force_update=False, using=None):
        steps = self.__class__.objects.filter(game_id=self.game_id).order_by('-index')
        self.index = steps[0].index + 1 if steps else 0
        super(self.__class__, self).save(force_insert, force_update, using)
