"""Global constants. All magic numbers live here."""

# Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"

# Colors (named constants, no raw tuples in game code)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 70)
COLOR_RED = (255, 50, 50)
COLOR_CYAN = (0, 220, 255)
COLOR_YELLOW = (255, 230, 0)

# Tags (string constants, mirrors Unity tags)
TAG_PLAYER = "Player"
TAG_ENEMY = "Enemy"
TAG_BULLET_P = "BulletPlayer"
TAG_BULLET_E = "BulletEnemy"
TAG_BARRIER = "Barrier"
TAG_UFO = "UFO"

# Layers (render order)
LAYER_BG = 0
LAYER_BARRIER = 1
LAYER_ENTITY = 2
LAYER_BULLET = 3
LAYER_UI = 10

# Player
PLAYER_SPEED = 220.0  # pixels/second
PLAYER_SHOOT_COOLDOWN = 0.5  # seconds
PLAYER_LIVES = 3
PLAYER_Y = SCREEN_HEIGHT - 50
PLAYER_MARGIN_X = 24
PLAYER_RESPAWN_GUARD = 1.0  # seconds of invulnerability after a hit

# Invader formation
INVADER_COLS = 11
INVADER_ROWS = 5
INVADER_H_SPACING = 55
INVADER_V_SPACING = 45
INVADER_STEP_X = 12
INVADER_STEP_DOWN = 16
INVADER_BASE_INTERVAL = 0.8  # seconds between steps
INVADER_MIN_INTERVAL = 0.1
INVADER_SHOOT_CHANCE = 0.002  # per invader per frame
INVADER_START_Y = 90
INVADER_EDGE_MARGIN = 20
INVADER_LOSE_Y = SCREEN_HEIGHT - 80
INVADER_WAVE_SPEEDUP = 0.85  # base interval multiplier per wave
INVADER_POINTS = [10, 20, 30]  # by invader_type

# UFO
UFO_SPEED = 140.0
UFO_SPAWN_INTERVAL = 25.0  # seconds
UFO_POINTS = [50, 100, 150, 300]
UFO_Y = 45

# Bullet
BULLET_SPEED_PLAYER = 480.0
BULLET_SPEED_ENEMY = 200.0
BULLET_WIDTH = 3
BULLET_HEIGHT = 12

# Barriers
BARRIER_COUNT = 4
BARRIER_COLS = 20
BARRIER_ROWS = 14
BARRIER_CELL = 4
BARRIER_Y = SCREEN_HEIGHT - 140
BARRIER_BLAST_RADIUS = 2

# Sprites
SPRITE_CELL = 3  # pixel-grid cell size for invaders/UFO
PLAYER_SPRITE_CELL = 2

# UI
UI_FONT_SIZE = 20
UI_TITLE_FONT_SIZE = 48
UI_MARGIN = 10
