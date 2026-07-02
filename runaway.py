import pygame
import random
import sys

# 1. เริ่มต้น Pygame
pygame.init()

# 2. ตั้งค่าหน้าจอ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemies! - เกมวิ่งหลบศัตรู")

# ตั้งค่าสี
WHITE = (240, 248, 255) # สีพื้นหลัง (ขาวอมฟ้า)
BLACK = (30, 30, 30)
PLAYER_COLOR = (0, 128, 255) # สีผู้เล่น (สีน้ำเงิน)
ENEMY_COLOR = (255, 69, 0)   # สีศัตรู (สีแดงส้ม)

# 3. ตั้งค่าตัวละคร (ผู้เล่น)
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 8

# 4. ตั้งค่าศัตรู (สิ่งกีดขวาง)
enemy_size = 50
enemies = [] # เก็บรายการศัตรูบนหน้าจอ
enemy_speed = 5
spawn_rate = 30 # ยิ่งค่าน้อย ศัตรูยิ่งเกิดเร็ว (อิงตามเฟรมเรต)
frame_count = 0

# 5. ตั้งค่าคะแนนและฟอนต์
score = 0
# พยายามใช้ฟอนต์มาตรฐานที่เครื่องส่วนใหญ่มี
font = pygame.font.SysFont("impact", 36) 
game_over_font = pygame.font.SysFont("impact", 64)

# ตั้งค่า Frame Rate
clock = pygame.time.Clock()
FPS = 60

# สถานะของเกม
game_over = False

# 6. ลูปหลักของเกม
while True:
    # ตรวจสอบการกดปุ่มต่างๆ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # ถ้าระบบ Game Over และผู้เล่นกดปุ่ม Spacebar ให้เริ่มเกมใหม่
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_over = False
                enemies.clear() # เคลียร์ศัตรูทั้งหมด
                player_x = WIDTH // 2 - player_size // 2 # กลับจุดศูนย์กลาง
                score = 0 # รีเซ็ตคะแนน
                enemy_speed = 5 # รีเซ็ตความเร็ว
                spawn_rate = 30

    if not game_over:
        # ระบบการเดินของผู้เล่น (ซ้าย-ขวา)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # ระบบสุ่มเกิดศัตรู
        frame_count += 1
        if frame_count >= spawn_rate:
            # สุ่มตำแหน่งแกน X ที่ศัตรูจะตกลงมา
            spawn_x = random.randint(0, WIDTH - enemy_size)
            enemies.append([spawn_x, -enemy_size]) # เพิ่มศัตรูที่จุดเหนือขอบจอบน
            frame_count = 0
            
            # เพิ่มความยาก: ยิ่งคะแนนเยอะ ศัตรูยิ่งตกเร็วและเกิดถี่ขึ้น
            if score % 10 == 0 and score > 0:
                enemy_speed += 0.2
                spawn_rate = max(10, int(spawn_rate - 0.5))

        # สร้างกรอบสี่เหลี่ยมของผู้เล่นเพื่อเตรียมเช็คการชน
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        
        # ระบบอัปเดตตำแหน่งศัตรู
        for enemy in enemies[:]: # ใช้ก๊อปปี้ของลิสต์เพื่อป้องกันบั๊กเวลาลบข้อมูล
            enemy[1] += enemy_speed # ให้ศัตรูตกลงมาด้านล่าง
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
            
            # ตรวจสอบการชน (ถ้าผู้เล่นโดนศัตรู)
            if player_rect.colliderect(enemy_rect):
                game_over = True
            
            # ถ้าศัตรูตกหลุดขอบจอด้านล่างไปแล้ว ให้ลบทิ้งและเพิ่มคะแนน
            if enemy[1] > HEIGHT:
                enemies.remove(enemy)
                score += 1

        # 7. วาดภาพลงบนหน้าจอ (สถานะกำลังเล่น)
        screen.fill(WHITE) # พื้นหลัง
        
        # วาดผู้เล่น
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
        
        # วาดศัตรูทั้งหมด
        for enemy in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, (enemy[0], enemy[1], enemy_size, enemy_size))
        
        # วาดคะแนน
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    else:
        # 8. หน้าจอตอน Game Over
        screen.fill(BLACK)
        
        # สร้างข้อความต่างๆ
        title_text = game_over_font.render("GAME OVER", True, ENEMY_COLOR)
        score_text = font.render(f"Final Score: {score}", True, PLAYER_COLOR)
        restart_text = font.render("Press SPACE to Restart", True, WHITE)
        
        # จัดตำแหน่งให้อยู่ตรงกลางหน้าจอ
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//1.5))

    # อัปเดตหน้าจอและตั้งค่าความเร็วของลูป
    pygame.display.update()
    clock.tick(FPS)