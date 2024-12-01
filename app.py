import pygame
import pygame_gui
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 2540

# Set up the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Parachute Descent Simulation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GOLD = (255, 215, 0)

# Physics constants
g = 9.8  # Gravitational acceleration (m/s^2)
air_density = 1.2  # kg/m^3, constant for air
time_step = 0.05  # Simulation time step (seconds)

# Conversion factor from meters to pixels
METER_TO_PIXEL = 50  # 1 meter equals 50 pixels

# Initialize Pygame GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Timer class for the stopwatch feature
class Timer:
    def __init__(self):
        self.elapsed_time = 0.0
        self.running = False

    def start(self):
        self.running = True
        self.last_update_time = pygame.time.get_ticks()

    def pause(self):
        if self.running:
            self.elapsed_time += (pygame.time.get_ticks() - self.last_update_time) / 1000.0
            self.running = False

    def reset(self):
        self.elapsed_time = 0.0
        self.running = False

    def update(self):
        if self.running:
            current_time = pygame.time.get_ticks()
            self.elapsed_time += (current_time - self.last_update_time) / 1000.0
            self.last_update_time = current_time

    def get_time(self):
        return self.elapsed_time

# Parachute class
class Parachute:
    def __init__(self, shape: str, size: float, mass: float, x: float, y: float, coin_size: float):
        self.shape = shape
        self.size = size          # Size of parachute in meters
        self.payload_mass = mass  # Mass in kg (excluding coin)
        self.x = x                # Position in meters
        self.y = y                # Position in meters
        self.velocity = 0.0       # Velocity in m/s
        self.is_paused = True     # Simulation starts paused

        self.coin_size = coin_size  # Diameter of the coin in meters
        self.coin_mass = self.calculate_coin_mass()
        self.total_mass = self.payload_mass + self.coin_mass

        self.area = self.calculate_area()
        self.drag_coefficient = self.get_drag_coefficient()

    def calculate_coin_mass(self) -> float:
        # Assuming coin is a cylinder: volume = π * r^2 * h
        # For simplicity, assume height is 10% of the diameter
        coin_density = 8000  # kg/m^3, approximate density of steel
        coin_radius = self.coin_size / 2
        coin_height = self.coin_size * 0.1  # Height is 10% of diameter
        coin_volume = math.pi * coin_radius ** 2 * coin_height
        coin_mass = coin_density * coin_volume
        return coin_mass

    def calculate_area(self) -> float:
        if self.shape == "Circle":
            return math.pi * (self.size / 2) ** 2
        elif self.shape == "Square":
            return self.size ** 2
        elif self.shape == "Triangle":
            return (math.sqrt(3) / 4) * (self.size ** 2)
        else:
            raise ValueError(f"Invalid shape: {self.shape}")

    def get_drag_coefficient(self) -> float:
        if self.shape == "Circle":
            return 1.2  # Typical drag coefficient for a circular parachute
        elif self.shape == "Square":
            return 1.05
        elif self.shape == "Triangle":
            return 0.8  # Slightly lower drag for triangles
        else:
            raise ValueError(f"Invalid shape: {self.shape}")

    def update(self):
        if not self.is_paused:
            weight = self.total_mass * g  # Positive downward

            # Calculate drag force
            if self.velocity != 0:
                drag_force = -0.5 * air_density * self.velocity * abs(self.velocity) * self.area * self.drag_coefficient
            else:
                drag_force = 0.0

            # Net force
            net_force = weight + drag_force  # drag_force is negative when velocity is positive

            # Acceleration
            acceleration = net_force / self.total_mass

            # Update velocity and position
            self.velocity += acceleration * time_step
            self.y += self.velocity * time_step

    def draw(self, screen):
        # Convert physical position (meters) to screen position (pixels)
        screen_x = int(self.x * METER_TO_PIXEL)
        screen_y = int(self.y * METER_TO_PIXEL)

        # Adjust the coin's radius based on coin_size
        coin_radius = int((self.coin_size / 2) * METER_TO_PIXEL)
        # Adjust the coin's vertical position to lengthen the strings
        string_length = (self.size * METER_TO_PIXEL) / 2  # Adjust this multiplier to lengthen strings
        coin_y = screen_y + int(self.size * METER_TO_PIXEL / 2) + int(string_length)

        pygame.draw.circle(screen, GOLD, (screen_x, coin_y), coin_radius)

        # Draw the strings (suspension lines)
        num_lines = 4  # Number of suspension lines
        for i in range(num_lines):
            # Evenly distribute lines along the bottom edge of the canopy
            if self.shape == "Circle":
                angle = (math.pi / (num_lines - 1)) * i  # Angles from left to right
                canopy_x = screen_x + int((self.size / 2) * METER_TO_PIXEL * math.cos(angle + math.pi))
                canopy_y = screen_y + int((self.size / 2) * METER_TO_PIXEL * math.sin(angle + math.pi))
            elif self.shape == "Square":
                # Positions along the bottom edge of the square
                size_in_pixels = int(self.size * METER_TO_PIXEL)
                canopy_x = screen_x - size_in_pixels // 2 + (size_in_pixels // (num_lines - 1)) * i
                canopy_y = screen_y + size_in_pixels // 2
            elif self.shape == "Triangle":
                # Positions along the bottom edge of the triangle
                half_size = (self.size / 2) * METER_TO_PIXEL
                canopy_x = screen_x - int(half_size) + int((self.size * METER_TO_PIXEL) / (num_lines - 1)) * i
                canopy_y = screen_y + int(half_size)
            else:
                raise ValueError(f"Invalid shape: {self.shape}")

            pygame.draw.line(screen, GRAY, (canopy_x, canopy_y), (screen_x, coin_y), 2)

        # Draw the parachute canopy based on its shape
        if self.shape == "Circle":
            radius_in_pixels = int((self.size / 2) * METER_TO_PIXEL)
            pygame.draw.circle(screen, BLUE, (screen_x, screen_y), radius_in_pixels)
        elif self.shape == "Square":
            size_in_pixels = int(self.size * METER_TO_PIXEL)
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    screen_x - size_in_pixels // 2,
                    screen_y - size_in_pixels // 2,
                    size_in_pixels,
                    size_in_pixels,
                ),
            )
        elif self.shape == "Triangle":
            half_size = (self.size / 2) * METER_TO_PIXEL
            points = [
                (screen_x, screen_y - half_size),
                (screen_x - half_size, screen_y + half_size),
                (screen_x + half_size, screen_y + half_size),
            ]
            pygame.draw.polygon(screen, BLUE, points)
        else:
            raise ValueError(f"Invalid shape: {self.shape}")

    def reset(self, x: float, y: float):
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.is_paused = True
        self.total_mass = self.payload_mass + self.coin_mass

    def set_parameters(self, shape: str, size: float, mass: float):
        self.shape = shape
        self.size = size
        self.payload_mass = mass
        self.coin_mass = self.calculate_coin_mass()
        self.total_mass = self.payload_mass + self.coin_mass
        self.area = self.calculate_area()
        self.drag_coefficient = self.get_drag_coefficient()

# Main simulation loop
def main():
    clock = pygame.time.Clock()

    # Initial positions in meters
    initial_x = (WIDTH / 2) / METER_TO_PIXEL  # Center of the screen
    initial_y = 0.0                            # Start at the top of the screen
    ground_y = HEIGHT / METER_TO_PIXEL         # Ground position in meters

    # Create a parachute
    initial_coin_size = 0.3  # Initial coin size in meters
    parachute = Parachute("Circle", 5.0, 80.0, initial_x, initial_y, initial_coin_size)

    # Create a timer
    timer = Timer()

    # UI Elements
    mass_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 20), (200, 30)),
        start_value=parachute.payload_mass,
        value_range=(0, 150),
        manager=manager,
    )

    size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 60), (200, 30)),
        start_value=parachute.size,
        value_range=(1, 10),
        manager=manager,
    )

    coin_size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((20, 100), (200, 30)),
        start_value=parachute.coin_size,
        value_range=(0.1, 1.0),  # Coin size range from 0.1 m to 1.0 m
        manager=manager,
    )

    shape_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=["Circle", "Square", "Triangle"],
        starting_option=parachute.shape,
        relative_rect=pygame.Rect((20, 140), (200, 30)),
        manager=manager,
    )

    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 180), (80, 30)),
        text="Start",
        manager=manager,
    )

    pause_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((110, 180), (80, 30)),
        text="Pause",
        manager=manager,
    )

    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((200, 180), (80, 30)),
        text="Reset",
        manager=manager,
    )

    # Labels
    mass_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((230, 20), (100, 30)),
        text=f"Mass: {parachute.payload_mass:.1f} kg",
        manager=manager,
    )

    size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((230, 60), (100, 30)),
        text=f"Size: {parachute.size:.1f} m",
        manager=manager,
    )

    coin_size_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((230, 100), (100, 30)),
        text=f"Coin Size: {parachute.coin_size:.2f} m",
        manager=manager,
    )

    # Text Box to Display Velocity, Position, Drag Coefficient, and Time
    info_box = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((600, 20), (180, 150)),  # Increased height to accommodate extra info
        html_text="",
        manager=manager,
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle UI events
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        parachute.is_paused = False
                        timer.start()
                    elif event.ui_element == pause_button:
                        parachute.is_paused = True
                        timer.pause()
                    elif event.ui_element == reset_button:
                        parachute.reset(initial_x, initial_y)
                        timer.reset()
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == mass_slider:
                        parachute.payload_mass = mass_slider.get_current_value()
                        mass_label.set_text(f"Mass: {parachute.payload_mass:.1f} kg")
                        parachute.total_mass = parachute.payload_mass + parachute.coin_mass
                    elif event.ui_element == size_slider:
                        parachute.size = size_slider.get_current_value()
                        size_label.set_text(f"Size: {parachute.size:.1f} m")
                        # Update area after changing size
                        parachute.area = parachute.calculate_area()
                    elif event.ui_element == coin_size_slider:
                        parachute.coin_size = coin_size_slider.get_current_value()
                        coin_size_label.set_text(f"Coin Size: {parachute.coin_size:.2f} m")
                        parachute.coin_mass = parachute.calculate_coin_mass()
                        parachute.total_mass = parachute.payload_mass + parachute.coin_mass
                elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == shape_dropdown:
                        # Use event.text to get the selected option
                        parachute.shape = event.text
                        parachute.drag_coefficient = parachute.get_drag_coefficient()
                        parachute.area = parachute.calculate_area()

            manager.process_events(event)

        # Update the parachute
        parachute.update()

        # Update the timer
        timer.update()

        # Stop the parachute when it reaches the ground
        if parachute.y + (parachute.size / 2) >= ground_y:
            parachute.y = ground_y - (parachute.size / 2)
            parachute.velocity = 0.0
            parachute.is_paused = True
            timer.pause()

        # Update the info box with current velocity, position, drag coefficient, time, and coin mass
        elapsed_time = timer.get_time()
        info_box.set_text(
            f"<b>Velocity:</b> {parachute.velocity:.2f} m/s<br>"
            f"<b>Position:</b> {parachute.y:.2f} m<br>"
            f"<b>Drag Coeff:</b> {parachute.drag_coefficient:.2f}<br>"
            f"<b>Time:</b> {elapsed_time:.2f} s<br>"
            f"<b>Coin Mass:</b> {parachute.coin_mass:.2f} kg"
        )

        # Update the UI manager
        manager.update(time_delta)

        # Drawing
        screen.fill(WHITE)

        # Draw the ground
        pygame.draw.line(
            screen,
            BLACK,
            (0, int(ground_y * METER_TO_PIXEL)),
            (WIDTH, int(ground_y * METER_TO_PIXEL)),
            2,
        )

        # Draw the parachute
        parachute.draw(screen)

        # Draw UI elements
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

# Run the simulation
if __name__ == "__main__":
    main()
