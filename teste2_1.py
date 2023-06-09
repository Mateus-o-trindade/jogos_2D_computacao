
import os
import time

import arcade

TILE_SPRITE_SCALING = 0.5
PLAYER_SCALING = 0.6

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Tiled Map with Levels Example"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SPRITE_SCALING


VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270


MOVEMENT_SPEED = 5
JUMP_SPEED = 23
GRAVITY = 1.1


class MyGame(arcade.Window):


    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        self.tile_map = None


        self.player_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None

        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None

        self.level = 1
        self.max_level = 2

    def setup(self):



        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png",
            PLAYER_SCALING,
        )

        # Starting position of the player
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        self.load_level(self.level)

        self.game_over = False

    def load_level(self, level):


        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(
            f":resources:tiled_maps/level_{level}.json", scaling=TILE_SPRITE_SCALING
        )




        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.tile_map.sprite_lists["Platforms"],
            gravity_constant=GRAVITY,
        )


        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)


        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):

        self.frame_count += 1


        self.clear()


        self.player_list.draw()
        self.tile_map.sprite_lists["Platforms"].draw()

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        if self.fps_message:
            arcade.draw_text(
                self.fps_message,
                self.view_left + 10,
                self.view_bottom + 40,
                arcade.color.BLACK,
                14,
            )

        if self.frame_count % 60 == 0:
            self.last_time = time.time()


        distance = self.player_sprite.right
        output = f"Distance: {distance:.0f}"
        arcade.draw_text(
            output, self.view_left + 10, self.view_bottom + 20, arcade.color.BLACK, 14
        )

        if self.game_over:
            arcade.draw_text(
                "Game Over",
                self.view_left + 200,
                self.view_bottom + 200,
                arcade.color.BLACK,
                30,
            )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):


        if self.player_sprite.right >= self.end_of_map:
            if self.level < self.max_level:
                self.level += 1
                self.load_level(self.level)
                self.player_sprite.center_x = 128
                self.player_sprite.center_y = 64
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
            else:
                self.game_over = True


        if not self.game_over:
            self.physics_engine.update()


        changed = False


        left_bndry = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True


        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_TOP
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN_BOTTOM
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True


        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(
                self.view_left,
                SCREEN_WIDTH + self.view_left,
                self.view_bottom,
                SCREEN_HEIGHT + self.view_bottom,
            )


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()