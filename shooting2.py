import pygame
import random
import math


# 画面サイズ
WIDTH, HEIGHT = 650, 660

# 色定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW=(255,255,0)




# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("東方風シューティング")
clock = pygame.time.Clock()



# プレイヤークラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.lives = 3
        self.last_shot_time = pygame.time.get_ticks() 
        self.last_barrier_shot_time = pygame.time.get_ticks()
        self.last_power_shot_time=pygame.time.get_ticks()


    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_RSHIFT] and not keys[pygame.K_RCTRL]:
            self.speed=10
        if keys[pygame.K_RCTRL] and not keys[pygame.K_RSHIFT]:
            self.speed=3
        if not keys[pygame.K_RSHIFT] and not keys[pygame.K_RCTRL]:
            self.speed=5

# 弾クラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

#  バリア弾クラス
class BarrierBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((42, 4)) 
        self.image.fill(YELLOW) 
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -4
        self.lifetime = 120 
        self.frame_count = 0

    def update(self):
        self.rect.y += self.speed
        self.frame_count += 1
        if self.rect.bottom < 0 or self.frame_count > self.lifetime:
            self.kill()

class Power_Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.Surface((40,50))
        self.image.fill(WHITE)
        self.rect=self.image.get_rect(center=(x,y))
        self.speed=-4
        self.lifetime=60
        self.frame_count=0

    def update(self):
        self.rect.y+=self.speed
        self.frame_count+=1
        if self.rect.bottom < 0 or self.frame_count > self.lifetime:
            self.kill()

   
        

# 敵クラス
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
        self.speed = 3
        self.direction = 1
        self.health = 50
        self.shoot_timer = 0

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        
    def shoot(self, enemy_bullets):
        for angle in range(15, 375, 30):
            radian = math.radians(angle)
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, math.cos(radian) * 3, math.sin(radian) * 3)
            enemy_bullets.add(bullet)

# 敵弾クラス
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction=1
        self.dx = dx
        self.dy = dy

    def update(self):
        self.rect.x += self.dx*self.direction
        self.rect.y += self.dy
        if self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()
        if self.rect.left <= 1 or self.rect.right >= WIDTH-1:
            self.direction *= -1

# 体力バーを描画
def draw_health_bar(surface, x, y, health, max_health):
    bar_length = 100
    bar_height = 10
    fill = (health / max_health) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# ゲームループ
def game():
    player = Player()
    enemy = Enemy()
    bullets = pygame.sprite.Group()
    barrier_bullets = pygame.sprite.Group()
    power_bullets=pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player, enemy)
    running = True
    last_shot_time = pygame.time.get_ticks()
    last_barrier_shot_time = pygame.time.get_ticks()
    last_power_shot_time = pygame.time.get_ticks()
    
    while running:
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - player.last_shot_time > 150: 
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet) 
                player.last_shot_time = current_time 

        if keys[pygame.K_b]:
            barrier_current_time = pygame.time.get_ticks()
            if barrier_current_time - player.last_barrier_shot_time > 1000: 
                barrier_bullet = BarrierBullet(player.rect.centerx, player.rect.top)
                barrier_bullets.add(barrier_bullet)
                all_sprites.add(barrier_bullet)
                player.last_barrier_shot_time = barrier_current_time

        if keys[pygame.K_v]:
            power_current_time=pygame.time.get_ticks()
            if power_current_time - player.last_power_shot_time > 3000:
                power_bullet = Power_Bullet(player.rect.centerx,player.rect.top)
                power_bullets.add(power_bullet)
                all_sprites.add(power_bullet)
                player.last_power_shot_time = power_current_time


        

                

        player.update(keys)
        enemy.update()
        bullets.update()
        barrier_bullets.update() 
        power_bullets.update()
        enemy_bullets.update()
        
        # 敵の弾発射
        if pygame.time.get_ticks() - last_shot_time > 600:
            enemy.shoot(enemy_bullets)
            last_shot_time = pygame.time.get_ticks()
        
        # 弾と敵の衝突判定
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                enemy.health -= 1
                bullet.kill()
                if enemy.health <= 0:
                    return "win"
        pygame.sprite.groupcollide(barrier_bullets, enemy_bullets, False, True)

        for power_bullet in power_bullets:
            if enemy.rect.colliderect(power_bullet.rect):
                enemy.health-=4
                power_bullet.kill()
                if enemy.health<=0:
                    return "win"
     

        
        # プレイヤーと敵弾の衝突判定
        for bullet in enemy_bullets:
            if player.rect.colliderect(bullet.rect):
                player.lives -= 1
                bullet.kill()
                if player.lives <= 0:
                    return "lose"
        
        all_sprites.draw(screen)
        enemy_bullets.draw(screen)
        barrier_bullets.draw(screen)
        power_bullets.draw(screen)
        draw_health_bar(screen, 10, 10, player.lives, 3)
        draw_health_bar(screen, WIDTH - 110, 10, enemy.health, 50)
        pygame.display.flip()
        clock.tick(60)

# メインループ
def main():
    while True:
        # スタート画面
        screen.fill(BLACK)
        font = pygame.font.Font(None, 50)
        text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        pygame.display.flip()
        
        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting_for_start = False

        start_time = pygame.time.get_ticks()
        result = game()
        end_time = pygame.time.get_ticks()
        elapsed_time_sec = int(end_time - start_time) //1000

        # リザルト画面
        while True:
            screen.fill(BLACK)
            large_font = pygame.font.Font(None, 80)
            font = pygame.font.Font(None, 50)

            if result == "win":
                win_text = large_font.render("YOU WIN!", True, WHITE)
                clear_time_text = font.render(f"You completed in {elapsed_time_sec} seconds!", True, WHITE)
                restart_text = font.render("Press ENTER to Restart", True, WHITE)
                screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200)))
                screen.blit(clear_time_text, clear_time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))
            else:
                game_over_text = large_font.render("GAME OVER!", True, WHITE)
                survived_text = font.render(f"You survived for {elapsed_time_sec} seconds!", True, WHITE)
                restart_text = font.render("Press ENTER to Restart", True, WHITE)
                screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200)))
                screen.blit(survived_text, survived_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
                screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    break
            else:
                continue
            break
                
if __name__ == "__main__":
    main()