import pygame
import random

pygame.init()

screen = pygame.display.set_mode((500, 500))

font = pygame.font.Font("freesansbold.ttf", 20)

class Snake:
    width = 25 # Width of the snake

    def __init__(self):
        self.x = [225]
        self.y = [225]
        self.x_change = 0
        self.y_change = 0
        self.length = 1

    def increase_length(self):
        self.x.append(self.x[self.length - 1])
        self.y.append(self.y[self.length - 1])
        self.length += 1

    def create_snake(self):
        for i in range(self.length):
            pygame.draw.rect(screen, (255, 0, 0), (self.x[i], self.y[i], self.width, self.width))

        # Update the position of the snakes body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


class Food:

    def __init__(self):
        self.x = random.randint(0, 19) * 25
        self.y = random.randint(0, 19) * 25
        self.width = 25

    def create_food(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.width))


def main():
    snake = Snake()
    play_game = True
    clock = pygame.time.Clock()
    food = Food()
    food_exists = True
    running = True
    instr = "DEAD! Press RETURN/ENTER to play again"
    instruction = font.render(instr, True, (255, 255, 255))
    score_value = 0
    game_over = pygame.image.load("game_over.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    food = Food()
                    food_exists = True
                    snake = Snake()
                    play_game = True
                    score_value = 0

        while play_game:
            screen.fill((0, 0, 0))

            # Controlling the FPS
            clock.tick(8)
            score = font.render("Score: " + str(score_value), True, (255, 255, 255))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                # Snake Movement
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        snake.x_change = snake.width # Makes sure that snake moves 1 snake_width at a time
                        snake.y_change = 0
                    if event.key == pygame.K_LEFT:
                        snake.x_change = - snake.width # Makes sure that snake moves 1 snake_width at a time
                        snake.y_change = 0
                    if event.key == pygame.K_UP:
                        snake.y_change = - snake.width # Makes sure that snake moves 1 snake_width at a time
                        snake.x_change = 0
                    if event.key == pygame.K_DOWN:
                        snake.y_change = snake.width # Makes sure that snake moves 1 snake_width at a time
                        snake.x_change = 0

            # Moving the snake
            snake.x[0] += snake.x_change
            snake.y[0] += snake.y_change

            # Checking if food is eaten
            if snake.x[0] == food.x and snake.y[0] == food.y:
                food_exists = False
                snake.increase_length()
                del food
                score_value += 1

            # Create new food if old food has been eaten
            if not food_exists:
                food = Food()
                food_exists = True

            # If the snake crosses boundary, make it reappear from the other end
            if snake.x[0] > 499:
                snake.x[0] = 0
            elif snake.x[0] < 0:
                snake.x[0] = 500 - snake.width

            if snake.y[0] > 499:
                snake.y[0] = 0
            elif snake.y[0] < 0:
                snake.y[0] = 500 - snake.width

            # Draw the food and snake
            food.create_food()
            snake.create_snake()
            screen.blit(score, (200, 30))

            # Death detection
            for i in range(2, snake.length):
                if snake.x[0] == snake.x[i] and snake.y[0] == snake.y[i]:
                    del snake
                    del food
                    #screen.blit(instruction, (10, 80))
                    screen.blit(game_over, (60, 250))
                    play_game = False
                    break

            pygame.display.update();

main()
