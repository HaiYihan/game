import pygame.font
from pygame.sprite import Group
class Scoreboard():
	def __init__(self,ai_settings,screen,stats):
		self.screen=screen
		self.screen_rect=screen.get_rect()
		self.ai_settings=ai_settings
		self.stats=stats
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	def prep_score(self):
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		score_str = str(self.stats.score)
		self.score_image = self.font.render(score_str, True, self.text_color,self.ai_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def show_score(self):
		"""在屏幕上显示得分"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		"""将最高得分转换为渲染的图像"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.ai_settings.bg_color)
		# 将最高得分放在屏幕顶部中央
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top=self.score_rect.top


	def prep_level(self):
		"""将等级转换为渲染的图像"""
		self.level_image = self.font.render(str(self.stats.level), True,self.text_color, self.ai_settings.bg_color)
		# 将等级放在得分下
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right=self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
	def prep_ships(self):
		"""显示还余下多少艘飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x=10+ship_number*ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)


import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""表示单个外星人的类"""

	def __init__(self, ai_settings, screen):
		"""初始化外星人并设置其起始位置"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		# 加载外星人图像，并设置其rect属性
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		# 每个外星人最初都在屏幕左上角附近
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		# 存储外星人的准确位置
		self.x = float(self.rect.x)

	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		"""如果外星人位于屏幕边缘，就返回True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置

        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
		#
        self.y -= self.speed_factor
        #更新表示子弹的rect的位置
        self.rect.y = self.y
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)




from os import system
import sys
from time import sleep
import pygame
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,row_number)
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        f_out = open("archive\highest_score.txt", "w")
        f_out.write(str(stats.high_score))
        f_out.close()
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif  event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
def check_events(ai_settings, screen, stats,sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            sys.exit()
        elif event.type ==pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,bullets, mouse_x, mouse_y)
def check_play_button(ai_settings, screen, stats,sb, play_button, ship, aliens,bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
def update_screen(ai_settings, screen, stats,sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.update()
        bullet.draw_bullet()
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left>1:
        # 将ships_left减1
        stats.ships_left -= 1
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
        system("cls")
    else:
        # 将ships_left减1
        stats.ships_left -= 1
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
        system("cls")
        stats.game_active=False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats,sb, ship, aliens, bullets)
            break
def update_aliens(ai_settings,screen,stats,sb,ship, aliens,bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        for i in range(1, 4):
            print("ship hit!!!")
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)





import pygame.font


class Button():
	def __init__(self,ai_settings,screen,msg):
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center
		self.prep_msg(msg)

	def prep_msg(self, msg):
		"""将msg渲染为图像，并使其在按钮上居中"""
		self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# 绘制一个用颜色填充的按钮，再绘制文本
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)



class GameStats:
	def __init__(self,ai_settings):

		self.ai_settings=ai_settings
		self.f=open("archive\highest_score.txt","r")
		self.game_active = False
		self.reset_stats()
		self.high_score=float(self.f.read())
		self.f.close()
		self.level = 1
	def reset_stats(self):
		"""初始化在游戏运行期间可能变化的统计信息"""
		self.ships_left = self.ai_settings.ship_limit
		self.score=0






import pygame.font
from pygame.sprite import Group
class Scoreboard():
	def __init__(self,ai_settings,screen,stats):
		self.screen=screen
		self.screen_rect=screen.get_rect()
		self.ai_settings=ai_settings
		self.stats=stats
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	def prep_score(self):
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		score_str = str(self.stats.score)
		self.score_image = self.font.render(score_str, True, self.text_color,self.ai_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def show_score(self):
		"""在屏幕上显示得分"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def prep_high_score(self):
		"""将最高得分转换为渲染的图像"""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.ai_settings.bg_color)
		# 将最高得分放在屏幕顶部中央
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top=self.score_rect.top


	def prep_level(self):
		"""将等级转换为渲染的图像"""
		self.level_image = self.font.render(str(self.stats.level), True,self.text_color, self.ai_settings.bg_color)
		# 将等级放在得分下
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right=self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10
	def prep_ships(self):
		"""显示还余下多少艘飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x=10+ship_number*ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)








class Settings:
    def __init__(self,RGD):
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = RGD
        #飞船设置
        self.ship_speed_factor=1.5
        self.ship_limit=3
        #子弹设置
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed=3
        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed=10
        #速度设置
        self.fleet_direction=2
        self.speedup_scale = 1.05
        # 记分
        self.alien_points = 50
        self.score_scale = 1.5
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)
		self.moving_right = False
		self.moving_left = False

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""根据移动标志调整飞船的位置"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		self.rect.centerx = self.center
		self.blitme()

	def center_ship(self):
		"""让飞船在屏幕上居中"""
		self.center = self.screen_rect.centerx

import py2exe
import sys
import pygame
from pygame.sprite import Group
def run_game():
    pygame.init()
    screen=pygame.display.set_mode((1200,800))
    ai_settings=Settings((130,210,255))
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("game")
    play_button = Button(ai_settings, screen, "Play")
    stats=GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #创建一个飞船、一个子弹编组和一个外星人编组
    bullets=Group()
    ship=Ship(ai_settings,screen)
    aliens=Group()
    create_fleet(ai_settings, screen,ship, aliens)
    while True:
        check_events(ai_settings, screen, stats,sb, play_button, ship,aliens, bullets)
        if stats.game_active:
            ship.update()
            update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        update_screen(ai_settings, screen, stats,sb, ship, aliens, bullets, play_button)

run_game()