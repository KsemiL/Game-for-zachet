import pygame
from item_script import weapon_list
from game_settings import Settings
from physics_script import gravity

actor_body_list = []
actor_list = []

class Actor:
    def __init__(self, size: tuple = (50, 100), color: tuple = (255, 255, 0), health: int = 100,
                 x: float = 0, y: float = None, speed: float = 20, jump_force: float = 100):
        self.health = health
        self.actor_size = size
        self.actor_color = color
        self.actor_surf = pygame.surface.Surface(size=self.actor_size)
        self.rendering_surf = None
        self.backpack = []
        self.speed = speed
        self.jump_force = jump_force
        self.ground = Settings.screen_height - self.actor_size[1]
        if y is None:
            y = self.ground
        self.actor_body = self.actor_surf.get_rect(x=x, y=y)
        self.is_jump = False
        self.action = 2
        self.flag_turn = True
        self.dead = False
        actor_list.append(self)
        actor_body_list.append(self.actor_body)


    def rendering(self, rendering_surf: pygame.surface.Surface=None,
                  color: tuple=None):
        if rendering_surf is not None:
            self.rendering_surf = rendering_surf
        rendering_surf = self.rendering_surf
        if color is None:
            color = self.actor_color
        if self.actor_surf is not None:
            self.actor_surf.fill(color)
            rendering_surf.blit(self.actor_surf, self.actor_body)
        if len(self.backpack) > 0:
            self.backpack[0].weapon_body.x = self.actor_body.centerx
            self.backpack[0].weapon_body.y = self.actor_body.centery
        if self.dead:
            self.actor_surf = None
            self.actor_body = None

    def get_hit(self):
            self.health -= 10
            self.rendering(color=(255, 0, 0))
            if self.health <= 0:
                self.rendering(color=(255, 0, 0))
                self.health = 0
                self.dead = True
                print('You defeated the enemy')




    def take_item(self, item_list):
        if self.actor_body.collidelist(item_list) != -1:
            current_item_index = self.actor_body.collidelist(item_list)
            self.backpack.append(weapon_list[current_item_index])

    def moving(self, direction, block_list=None):
        if block_list is not None:
            if self.actor_body.collidelist(block_list) != -1:
                current_block = block_list[self.actor_body.collidelist(block_list)]
                if self.actor_body.collidepoint(current_block.bottomleft[0], current_block.bottomleft[1]):
                    self.actor_body.right = current_block.left

                elif self.actor_body.collidepoint(current_block.bottomright[0], current_block.bottomright[1]):
                    self.actor_body.left = current_block.right

                if self.actor_body.bottomright[0] > current_block.topleft[0] and self.actor_body.bottomleft[0] < current_block.topright[0]:
                    self.ground = current_block.top - self.actor_size[1]

            else:
                self.ground = Settings.screen_height - self.actor_size[1]

        if direction == 1:
            self.actor_body.x += self.speed

        if direction == -1:
            self.actor_body.x -= self.speed

        self.actor_body.x = max(0, min(self.actor_body.x, Settings.screen_width - self.actor_size[0])) # Сверка максимального и минимального положения игрока

        if direction == 2:
            self.actor_body.y += self.speed

        if direction == -2:
            self.actor_body.y -= self.speed

        if Settings.need_gravity:
            if self.actor_body.y < self.ground:
                self.actor_body.y += gravity
            else:
                self.is_jump = False

    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.actor_body.y -= self.jump_force

    def use_attack(self, enemy):
        self.action -= 1
        enemy.get_hit()

    def use_heal(self):
        self.action -= 1
        self.health += 5
        if self.health >= 100:
            self.health = 100


