import pygame
import os

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y,width, height, move_range,speed):
        super().__init__()

        # Load and set up idle animation
        self.idle_frames = []
        for i in range(1, 10):  # Assuming you have idle1.png to idle9.png
            frame_path = os.path.join('Assets/Eleonore/idle', f"Idle{i}.png")
            frame = pygame.image.load(frame_path).convert_alpha()
            self.idle_frames.append(frame)

        self.current_frame = 0

        # Initialize the size of the NPC
        self.width = width
        self.height = height
        # initialize the first image to the first frame
        self.image = pygame.transform.scale(self.idle_frames[0], (width, height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # Animation variables
        self.animation_speed = 0.2  # Adjust as needed
        self.animation_timer = 0

        #cut for now 
        self.dialog = [
            "Hello there!",
            "I have some information for you.",
            "Press 'E' to talk to me."
        ]

        # Initialize NPC's movement attributes
        self.current_position = x
        self.move_range = move_range
        self.speed = speed

        # 1 for moving right, -1 for moving left
        self.direction = 1 

    def update(self, FPS):
        # Animate the idle animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed * FPS:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

        # Move the NPC within its defined range
        self.current_position += self.direction * self.speed
        if self.current_position > self.rect.x + self.move_range:
            self.direction = -1
        elif self.current_position < self.rect.x - self.move_range:
            self.direction = 1

        self.rect.x = self.current_position

    def talk(self):
        # Implement NPC dialog logic 
        pass
