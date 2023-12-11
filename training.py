import pygame
import sys
import os
from Scripts.Logic import gameLogicFunctions
from Scripts.Player.Player import Player
from Scripts.Logic import Collision
import hp


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Training Level")

enemies = []

clock = pygame.time.Clock()
FPS = 60
frame_count = 0
spawn_wave = False

# adds background 
# Load a single background image
background_image_path = os.path.join("Assets", "nature_3", "origbig.png")
background_image = pygame.image.load(background_image_path).convert_alpha()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw ground image
ground_image_path = os.path.join("Assets", "nature_3", "ground.png")
ground_image = pygame.image.load(ground_image_path).convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Character initialization with starting position and correct image paths
main_character = Player((200, 650))
# calls player hp class
player_hp = hp.HP((0,0))

# Define the new width and height for the player
new_width = 200
new_height = 200

# Resize the player's image
main_character.image = pygame.transform.scale(main_character.image, (new_width, new_height))

# Update the player's rect to match the new dimensions
main_character.rect = main_character.image.get_rect()
main_character.rect.topleft = (400, 350)

# Define hitboxes for player and goblin
player_hitbox = Collision.collisionBox(main_character.rect, 0)
def player_collision_detection():
    global spawn_wave
    for enemy in enemies:
        if main_character.rect.colliderect(enemy.rect):
            # Collision detected between player and enemy (overlap)
            enemy.Gob_take_damage(20)  # Handle the hit
            if enemy.should_die and enemy.state != "DEATH":
                enemy.play_death_animation()
                if enemy.state == "CLEANUP" and enemy.timer >= enemy.get_duration():
                    enemies_to_remove.append(enemy)

groundDimensions = pygame.Rect(-100,600,SCREEN_WIDTH + 200, 120)
groundCollision = Collision.collisionBox(groundDimensions, 0)
def draw_collision_boxes():
    for p_hitbox in gameLogicFunctions.playerHitBoxGroup:
        box_surface = pygame.Surface(p_hitbox.rect.size, pygame.SRCALPHA)
        box_surface.fill((0, 0, 255))
        screen.blit(box_surface, p_hitbox.rect.topleft)

    for p_hurtbox in gameLogicFunctions.playerHurtBoxGroup:
        box_surface = pygame.Surface(p_hurtbox.rect.size, pygame.SRCALPHA)
        box_surface.fill((0, 255, 0))
        screen.blit(box_surface, p_hurtbox.rect.topleft)

    for e_hitbox in gameLogicFunctions.enemyHitBoxGroup:
        box_surface = pygame.Surface(e_hitbox.rect.size, pygame.SRCALPHA)
        box_surface.fill((255, 0, 0))
        screen.blit(box_surface, e_hitbox.rect.topleft)

    for e_hurtbox in gameLogicFunctions.enemyHurtBoxGroup:
        box_surface = pygame.Surface(e_hurtbox.rect.size, pygame.SRCALPHA)
        box_surface.fill((0, 255, 0))
        screen.blit(box_surface, e_hurtbox.rect.topleft)

class GoblinBerserker(pygame.sprite.Sprite):
    def __init__(self, position, idle_images_left, run_images_left, attack_images_left,
                death_images_left, idle_images_right=None, run_images_right=None,
                attack_images_right=None, death_images_right=None, hurt_left_images=None,
                hurt_right_images=None, is_running=False):
        super().__init__()
        
        # Initialize the Goblin Berserker
        self.idle_images_left = idle_images_left
        self.run_images_left = run_images_left

        self.attack_images_left = attack_images_left
        self.death_images_left = death_images_left  

        self.idle_images_right = idle_images_right
        self.run_images_right = run_images_right

        self.attack_images_right = attack_images_right
        self.death_images_right = death_images_right 

        # New attributes for hurt images
        self.hurt_left_images = hurt_left_images
        self.hurt_right_images = hurt_right_images 

        # New flag to indicate whether the goblin should perform the death animation
        self.should_die = False

        # Add a death_frames_played attribute
        self.death_frames_played = 0

        self.direction = -1  # Default direction is left
        self.set_images()  # Set initial images based on the direction

        # Movement variables for goblins
        self.speed = 2 
        self.direction = 1  # 1 for moving right, -1 for moving left

        # Initialize image and rect attributes
        self.index = 0
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(topleft=position)

        # Frame delay
        self.frame_delay = 10 
        self.frame_counter = 0

        # Frame delay for attack animation
        self.attack_frame_delay = 1  
        self.attack_frame_counter = 0

        # Duration for attack animation (in frames)
        self.attack_duration_left = 10 * len(attack_images_left)  # 10 seconds (60 FPS * 10 seconds)
        self.attack_duration_right = 10 * len(attack_images_right)  # 10 seconds (60 FPS * 10 seconds)


        # Duration for death animation (in frames)
        self.death_duration_left = 10 * len(death_images_left)  
        self.death_duration_right = 10 * len(death_images_right)  

        # Set the initial death duration based on direction
        self.death_duration = 10 * len(death_images_left)  # or death_images_right 

        # Flag to determine animation type
        self.is_running = is_running

        # New state and timing variables
        self.state = "IDLE"  # Initial state
        self.idle_duration = 180  # 3 seconds (60 FPS * 3 seconds)
        self.run_duration = 120  # 2 seconds (60 FPS * 2 seconds)

        # Set the initial attack duration based on direction
        self.attack_duration = self.attack_duration_left if self.direction == -1 else self.attack_duration_right
        self.timer = 0

        # Add max_health attribute with a default value
        self.max_health = 60
        # Set initial health to max_health
        self.health = self.max_health  

        # Add a counter for collisions with the player
        self.collision_counter = 0

    def set_images(self):
        # facing left
        if self.direction == -1: 
            self.idle_images = self.idle_images_left
            self.run_images = self.run_images_left

            self.attack_images = self.attack_images_left
            self.attack_duration = len(self.attack_images_left) * 10  

            self.death_images = self.death_images_left
        # facing right
        elif self.direction == 1: 
            self.idle_images = self.idle_images_right
            self.run_images = self.run_images_right

            self.attack_images = self.attack_images_right
            self.attack_duration = len(self.attack_images_right) * 10 
            self.death_images = self.death_images_right

    def update(self):
        # Increment the frame counter
        self.frame_counter += 1

        # Set the images based on the direction
        self.set_images()

        # Check if it's time to switch frames
        if self.frame_counter >= self.frame_delay:
            # Update animation frames based on the current state
            if self.state == "IDLE":
                self.idle_update()
            elif self.state == "RUN":
                self.run_update()
            elif self.state == "ATTACK":
                self.attack_update()
            elif self.state == "DEATH": 
                self.death_update()
            elif self.state == "HURT":  # New state for hurt
                self.hurt_update()

            # Reset the frame counter
            self.frame_counter = 0

        # Resize the goblin's image to match the player's dimensions
        new_width = 200  
        new_height = 200  
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Move the goblin based on the current state
        if self.state == "RUN":
            self.rect.x += self.direction * self.speed

            # Change direction if reaching the screen edges
            if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
                self.direction *= -1

            # Check if goblin has passed a certain point to turn around
            # Adjust the X-coordinate as needed
            if self.rect.x > 1000:
                self.direction = -1  # Turns around

        # Check if it's time to switch to the next state
        self.timer += 1
        if self.timer >= self.get_duration():
            self.timer = 0
            self.switch_state()

    def death_update(self):
        # Increment the frame counter
        self.frame_counter += 1

        # Update animation frames for death state
        self.index += 1
        if self.index >= len(self.death_images):
            self.index = 0
            self.timer += 1

        self.image = self.death_images[self.index]

        # Increment the death frames played
        self.death_frames_played += 1

        # Check if it's time to switch to the next state or cleanup
        if self.death_frames_played >= num_frames_death:
            self.cleanup()

        elif self.timer >= self.death_duration:
            self.timer = 0
            self.cleanup()

    def cleanup(self):
        # Switch to a cleanup state to remove the goblin
        self.state = "CLEANUP"
        # Set images to an empty list or provide cleanup images if needed
        self.images = []  
        # Reset the timer for the new state
        self.timer = 0  
        # Add the goblin to the list of enemies to be removed
        enemies_to_remove.append(self)
        # Reset the collision counter after cleanup
        self.collision_counter = 0

    def idle_update(self):
        # Update animation frames for idle state
        self.index += 1

        if self.index >= len(self.idle_images):
            self.index = 0

        self.image = self.idle_images[self.index]

    def run_update(self):
        # Update animation frames for run state
        self.index += 1

        if self.index >= len(self.run_images):
            self.index = 0

        self.image = self.run_images[self.index]

    def attack_update(self):
        # Increment the attack frame counter
        self.attack_frame_counter += 1

        # Check if it's time to switch frames for the attack animation
        if self.attack_frame_counter >= self.attack_frame_delay:

            # Update animation frames for attack
            self.index += 1

            if self.index >= len(self.attack_images):
                self.index = 0

            self.image = self.attack_images[self.index]

            # Reset the attack frame counter
            self.attack_frame_counter = 0

        # Move the goblin (if needed during attack)
        self.rect.x += self.direction * self.speed

    def switch_state(self):
        # Switch to the next state based on the current state
        if self.state == "IDLE":
            self.state = "RUN"
            self.images = self.run_images
        elif self.state == "RUN":
            self.state = "ATTACK"
            self.images = self.attack_images
        elif self.state == "ATTACK":
            self.state = "IDLE"
            self.images = self.idle_images
        elif self.state == "DEATH":
            # pass so the goblin won't get stuck in death loop
            pass

    def get_duration(self):
        # Return the duration based on the current state
        if self.state == "IDLE":
            return self.idle_duration
        elif self.state == "RUN":
            return self.run_duration
        elif self.state == "ATTACK":
            return self.attack_duration
        elif self.state == "DEATH":
            return self.death_duration
        else:
            return 0  # Return a default value if the state is not recognized

    def Gob_take_damage(self, damage):
        # Handle damage to the Goblin Berserker
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.collision_counter += 1  # Increment the collision counter
            if self.collision_counter >= 2:
                self.hurt_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/hurt/', f"GoblinLeftHurt4.png"))]
                self.should_die = True
            
        else:
            
            #if self.collision_counter == 5:
             self.switch_to_hurt_state()
              #  self.should_die = True 
            
    
    def switch_to_hurt_state(self):
        # Switch to the hurt state and set the images accordingly
        self.state = "HURT"
        self.images = self.hurt_left_images if self.direction == -1 else self.hurt_right_images
        self.timer = 0  # Reset the timer for the new state
        self.index = 0  # Reset the animation index


    def hurt_update(self):
        # Increment the frame counter
        self.frame_counter += 1

        # Update animation frames for hurt state
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[self.index]

        # Check if it's time to switch to the next state or cleanup
        if self.timer >= self.get_duration():
            self.timer = 0
            self.state = "IDLE"  # Switch back to idle state after hurt

    def play_death_animation(self):
        # Switch to the death state and set the images accordingly
        self.state = "DEATH"
        self.images = self.death_images

        # Reset the flag after playing the death animation
        self.should_die = False  

        # Set the correct death duration based on direction
        self.death_duration = 10 * len(self.death_images_left) if self.direction == -1 else 10 * len(self.death_images_right)

        # New variable to track the number of frames played during death animation
        self.death_frames_played = 0

# Load sprite sheets for Goblin Idle
num_frames_idle = 6

idle_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/idle/', f"GoblinLeftIdle{i}.png")) for i in range(1, num_frames_idle + 1)]
idle_right_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Right/Png/idle/', f"GoblinRightIdle{i}.png")) for i in range(1, num_frames_idle + 1)]


# Load sprite sheets for Goblin Run
num_frames_run = 6

run_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/run/',  f"GoblinLeftRun{i}.png")) for i in range(1, num_frames_run + 1)]
run_right_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Right/Png/run/',  f"GoblinRightRun{i}.png")) for i in range(1, num_frames_run + 1)]

# Load sprite sheets for Goblin Hurt
num_frames_hurt = 4

hurt_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/hurt/', f"GoblinLeftHurt{i}.png")) for i in range(1, num_frames_hurt + 1)]
hurt_right_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Right/Png/hurt/', f"GoblinRightHurt{i}.png")) for i in range(1, num_frames_hurt + 1)]

# Load sprite sheets for Goblin Attack
num_frames_attack = 11

attack_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/attack/',  f"GoblinLeftAttack{i}.png")) for i in range(1, num_frames_run + 1)]
attack_right_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Right/Png/attack/',  f"GoblinRightAttack{i}.png")) for i in range(1, num_frames_run + 1)]


# Load sprite sheets for Goblin Death
num_frames_death = 9  

death_left_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Left/Png/death/', f"GoblinLeftDeath{i}.png")) for i in range(1, num_frames_death + 1)]
death_right_images = [pygame.image.load(os.path.join('Assets/mobs/goblin_berserker/goblin/Right/Png/death/', f"GoblinRightDeath{i}.png")) for i in range(1, num_frames_death + 1)]

# Function to spawn enemies
def spawn_enemies():

    global spawn_wave

    # Logic to determine the number of enemies and their positions
    if spawn_wave:
        start_x_position = 900 
        y_position = 500 

        # Create a single instance of GoblinBerserker
        goblin = GoblinBerserker(
            (start_x_position, y_position),
            idle_left_images, run_left_images, attack_left_images, death_left_images,
            idle_right_images, run_right_images, attack_right_images, death_right_images,
            is_running=False,
            hurt_left_images=hurt_left_images,
            hurt_right_images=hurt_right_images
        )


        # Add the goblin to the enemies list
        enemies.append(goblin)

        # Reset the spawn_wave flag to avoid continuous spawning
        spawn_wave = False

# Main game loop
running = True
while running:
    enemies_to_remove = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                spawn_wave = True  # Press 's' to spawn enemies
            elif event.key == pygame.K_u:
                # Press 'u' to kill all goblins and trigger death animations
                for enemy in enemies:
                    enemy.should_die = True  # Set the flag for each goblin
                    enemy.play_death_animation() # Triggers the death animation

        # Handle player input inside the event loop
        main_character.handle_event(event)

    currentPlayerHP = player_hp
    player_collision_detection()
    #checks if player current health decreased 
    if currentPlayerHP.get_health() > player_hp.get_health() and currentPlayerHP.get_health() > 0:
        player_hp.take_damage(screen)

    # Draw the background first
    screen.blit(background_image, (0, 0))
    screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))

    # Draw the player character
    screen.blit(main_character.image, main_character.rect)

    # Draw the player's health bar
    screen.blit(player_hp.image, (0, 0))

    # Spawn enemies when the wave is requested
    spawn_enemies()

    # Update entities
    main_character.update()

    # Handle collisions and remove entities
    for enemy in enemies:
        # Handle enemy-specific logic
        enemy.update()
        if enemy.should_die and enemy.state != "DEATH":
            enemy.play_death_animation()
            enemy.Gob_take_damage(20)

            if enemy.state == "CLEANUP" and enemy.timer >= enemy.get_duration():
                enemies_to_remove.append(enemy)

    # Remove enemies that have completed their cleanup
    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    # Render entities and background

    for enemy in enemies:
        screen.blit(enemy.image, enemy.rect)

        # Display goblin health above their heads
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"Health: {enemy.health}", True, (255, 255, 255))
        health_rect = health_text.get_rect(center=(enemy.rect.centerx, enemy.rect.y - 20))
        screen.blit(health_text, health_rect)

    # Display a notification when the wave is finished
    if not enemies and spawn_wave == False:
        # Display a message on the screen
        font = pygame.font.Font(None, 36)
        message_text = font.render("Get Ready! Press 's' to spawn new enemies or move right to proceed. Press 'u' to kill all goblins.", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(message_text, message_rect)

    # Display controls on the top right of the screen
    controls_font = pygame.font.Font(None, 24)
    controls_text = [
        "CONTROLS",
        "Left/Right Arrow: Move Left/Right",
        "Down Arrow: Crouch",
        "Z: Jump",
        "X: Saber",
        "C: Dash",
        "T: Advance Text",
        "Protective spell on*"
    ]

    for i, line in enumerate(controls_text):
        controls_surface = controls_font.render(line, True, (255, 255, 255))
        controls_rect = controls_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10 + i * 20))
        screen.blit(controls_surface, controls_rect)

    # Check if the player reaches the right end to move to the boss level
    if main_character.rect.right > SCREEN_WIDTH - 50:
        # Transition to the new file (mainScript.py for the boss level)
        import mainScript
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()