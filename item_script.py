import pygame
import math
import actor_script

weapon_body_list = []
weapon_list = []

class Projectile:
    def __init__(self, size: tuple = (10, 10), color: tuple = (255, 0, 0),
                 x: float = 0, y: float = 0):
        self.size = size
        self.color = color
        self.surf = pygame.surface.Surface(size=self.size)
        self.body = self.surf.get_rect(x=x, y=y)
        self.speed = 25 #скорость снаряда

    def check_hit(self):
        target_list = actor_script.actor_body_list
        if len(actor_script.actor_body_list) > 0:
            if self.body.collidelist(target_list) != -1:
                current_target = actor_script.actor_list[self.body.collidelist(target_list)]
                current_target.get_hit()
                if current_target.dead:
                    actor_script.actor_list.pop(self.body.collidelist(target_list))
                    actor_script.actor_body_list.pop(self.body.collidelist(target_list))



class Weapon:
    def __init__(self, size: tuple = (40, 20), color: tuple = (200, 180, 120),
                 x: float = 0, y: float = 0):
        self.weapon_size = size
        self.weapon_color = color
        self.weapon_surf = pygame.surface.Surface(size=self.weapon_size)
        self.weapon_body = self.weapon_surf.get_rect(x=x, y=y)
        self.rendering_surf = None
        self.projectile = Projectile()
        self.fire_flag = False
        weapon_list.append(self)
        weapon_body_list.append(self.weapon_body)

    def rendering(self, rendering_surf: pygame.surface.Surface=None,
                  color: tuple=None):
        if rendering_surf is not None:
            self.rendering_surf = rendering_surf
        rendering_surf = self.rendering_surf
        if color is None:
            color = self.weapon_color
        self.weapon_surf.fill(color)
        rendering_surf.blit(self.weapon_surf, self.weapon_body)

        if not self.fire_flag:
            self.projectile.body.x = self.weapon_body.midright[0]
            self.projectile.body.y = self.weapon_body.midright[1]
        else:
            pygame.draw.rect(rendering_surf, color=(255, 100, 50), rect=self.projectile.body)
            self.projectile.body.x += self.projectile.speed  # Движение только по оси X

            if self.projectile.body.y > 500 or self.projectile.body.x > 500:
                self.fire_flag = False

    def fire(self):
        self.fire_flag = True