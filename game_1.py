import pygame
from game_settings import Settings
from actor_script import Actor
from item_script import Weapon, weapon_body_list


main_screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))

actor_1 = Actor(color=(255, 192, 203), x=150, y=400, speed=10)

actor_enemy_1 = Actor(x=300, y=350, speed=0)
actor_enemy_2 = None

weapon_1 = Weapon(x=200, y=480)

button_skill_1 = pygame.Rect(100, 400, 50, 50)

block_1 = pygame.Rect(300, 450, 100, 25)
block_2 = pygame.Rect(600, 450, 100, 25)
block_3 = pygame.Rect(100, 100, 600, 25)

ladder = pygame.Rect(10, 100, 10, 400)

direction = 0

while True:

    main_screen.fill((52, 98, 223))

    actor_1.rendering(rendering_surf=main_screen)
    weapon_1.rendering(rendering_surf=main_screen)
    if actor_enemy_1:
        actor_enemy_1.rendering(rendering_surf=main_screen)
    if actor_enemy_2:
        actor_enemy_2.rendering(rendering_surf=main_screen)


    pygame.draw.rect(main_screen, color=(255, 255, 255), rect=block_1)
    pygame.draw.rect(main_screen, color=(255, 255, 255), rect=block_2)
    pygame.draw.rect(main_screen, color=(255, 255, 255), rect=block_3)
    pygame.draw.rect(main_screen, color=(184, 134, 11), rect=ladder)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction = 1
            elif event.key == pygame.K_a:
                direction = -1
            elif event.key == pygame.K_f:  # Стрельба по клавише 'f'
                if len(actor_1.backpack) > 0:
                    actor_1.backpack[0].fire()


            elif event.key == pygame.K_SPACE:
                actor_1.jump()

            

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                direction = 0
            elif event.key == pygame.K_a:
                direction = 0





    if len(actor_1.backpack) > 0:
        actor_1.backpack[0].projectile.check_hit()

    actor_1.take_item(item_list=weapon_body_list)

    # Проверка на смерть первого врага
    if actor_enemy_1 and actor_enemy_1.dead:
        actor_enemy_1 = None  # Удаляем первого врага
        actor_enemy_2 = Actor(x=300, y=5, speed=0)  # Создаем второго на верхней платформе
        # actor_enemy_2.health = 5 # можно добавить больший запас здоровья второму врагу



    pygame.time.delay(60)

    actor_1.moving(direction, [block_1, block_2,block_3,ladder])

    pygame.display.update()
