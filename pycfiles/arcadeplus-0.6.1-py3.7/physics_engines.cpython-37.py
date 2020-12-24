# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\physics_engines.py
# Compiled at: 2020-04-07 19:56:23
# Size of source mod 2**32: 14118 bytes
"""
Physics engines for top-down or platformers.
"""
from arcadeplus import check_for_collision_with_list
from arcadeplus import check_for_collision
from arcadeplus import Sprite
from arcadeplus import SpriteList

def _circular_check(player, walls):
    """
    This is a horrible kludge to 'guess' our way out of a collision
    Returns:

    """
    original_x = player.center_x
    original_y = player.center_y
    vary = 1
    while True:
        try_list = [
         [
          original_x, original_y + vary],
         [
          original_x, original_y - vary],
         [
          original_x + vary, original_y],
         [
          original_x - vary, original_y],
         [
          original_x + vary, original_y + vary],
         [
          original_x + vary, original_y - vary],
         [
          original_x - vary, original_y + vary],
         [
          original_x - vary, original_y - vary]]
        for my_item in try_list:
            x, y = my_item
            player.center_x = x
            player.center_y = y
            check_hit_list = check_for_collision_with_list(player, walls)
            if len(check_hit_list) == 0:
                return

        vary *= 2


def _move_sprite(moving_sprite: Sprite, walls: SpriteList, ramp_up: bool):
    moving_sprite.angle += moving_sprite.change_angle
    hit_list = check_for_collision_with_list(moving_sprite, walls)
    if len(hit_list) > 0:
        _circular_check(moving_sprite, walls)
    moving_sprite.center_y += moving_sprite.change_y
    hit_list_x = check_for_collision_with_list(moving_sprite, walls)
    complete_hit_list = hit_list_x
    if len(hit_list_x) > 0:
        if moving_sprite.change_y > 0:
            while len(check_for_collision_with_list(moving_sprite, walls)) > 0:
                moving_sprite.center_y -= 1

        else:
            if moving_sprite.change_y < 0:
                for item in hit_list_x:
                    while check_for_collision(moving_sprite, item):
                        moving_sprite.center_y += 0.25

                    if item.change_x != 0:
                        moving_sprite.center_x += item.change_x

            else:
                moving_sprite.change_y = min(0.0, hit_list_x[0].change_y)
    moving_sprite.center_y = round(moving_sprite.center_y, 2)
    moving_sprite.center_x += moving_sprite.change_x
    check_again = True
    while check_again:
        check_again = False
        hit_list_y = check_for_collision_with_list(moving_sprite, walls)
        complete_hit_list = hit_list_x
        for sprite in hit_list_y:
            if sprite not in complete_hit_list:
                complete_hit_list.append(sprite)

        if len(hit_list_y) > 0:
            change_x = moving_sprite.change_x
            if change_x > 0:
                if ramp_up:
                    for _ in hit_list_y:
                        moving_sprite.center_y += change_x
                        if len(check_for_collision_with_list(moving_sprite, walls)) > 0:
                            moving_sprite.center_y -= change_x
                            moving_sprite.center_x -= 1
                            check_again = True
                            break

                else:
                    while len(check_for_collision_with_list(moving_sprite, walls)) > 0:
                        moving_sprite.center_x -= 1

            elif change_x < 0:
                if ramp_up:
                    for item in hit_list_y:
                        moving_sprite.center_y -= change_x
                        if len(check_for_collision_with_list(moving_sprite, walls)) > 0:
                            moving_sprite.center_y += change_x
                            moving_sprite.left = max(item.right, moving_sprite.left)
                            check_again = True
                            break

                else:
                    while len(check_for_collision_with_list(moving_sprite, walls)) > 0:
                        moving_sprite.center_x += 1

            else:
                print("Error, x collision while player wasn't moving.\nMake sure you aren't calling multiple updates, like a physics engine update and an all sprites list update.")

    return complete_hit_list


class PhysicsEngineSimple:
    __doc__ = '\n    Simplistic physics engine for use in games without gravity, such as top-down\n    games. It is easier to get\n    started with this engine than more sophisticated engines like PyMunk. Note, it\n    does not currently handle rotation.\n    '

    def __init__(self, player_sprite: Sprite, walls: SpriteList):
        """
        Create a simple physics engine.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList walls: The sprites it can't move through
        """
        assert isinstance(player_sprite, Sprite)
        assert isinstance(walls, SpriteList)
        self.player_sprite = player_sprite
        self.walls = walls

    def update(self):
        """
        Move everything and resolve collisions.

        :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
        """
        complete_hit_list = _move_sprite((self.player_sprite), (self.walls), ramp_up=False)
        return complete_hit_list


class PhysicsEnginePlatformer:
    __doc__ = '\n    Simplistic physics engine for use in a platformer. It is easier to get\n    started with this engine than more sophisticated engines like PyMunk. Note, it\n    does not currently handle rotation.\n    '

    def __init__(self, player_sprite: Sprite, platforms: SpriteList, gravity_constant: float=0.5, ladders: SpriteList=None):
        """
        Create a physics engine for a platformer.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList platforms: The sprites it can't move through
        :param float gravity_constant: Downward acceleration per frame
        :param SpriteList ladders: Ladders the user can climb on
        """
        if ladders is not None:
            if not isinstance(ladders, SpriteList):
                raise TypeError('Fourth parameter should be a SpriteList of ladders')
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.gravity_constant = gravity_constant
        self.jumps_since_ground = 0
        self.allowed_jumps = 1
        self.allow_multi_jump = False
        self.ladders = ladders

    def is_on_ladder(self):
        if self.ladders:
            hit_list = check_for_collision_with_list(self.player_sprite, self.ladders)
            if len(hit_list) > 0:
                return True
        return False

    def can_jump(self, y_distance=5) -> bool:
        """
        Method that looks to see if there is a floor under
        the player_sprite. If there is a floor, the player can jump
        and we return a True.

        :returns: True if there is a platform below us
        :rtype: bool
        """
        self.player_sprite.center_y -= y_distance
        hit_list = check_for_collision_with_list(self.player_sprite, self.platforms)
        self.player_sprite.center_y += y_distance
        if len(hit_list) > 0:
            self.jumps_since_ground = 0
        if (len(hit_list) > 0 or self).allow_multi_jump:
            if self.jumps_since_ground < self.allowed_jumps:
                return True
        return False

    def enable_multi_jump(self, allowed_jumps: int):
        """
        Enables multi-jump.
        allowed_jumps should include the initial jump.
        (1 allows only a single jump, 2 enables double-jump, etc)

        If you enable multi-jump, you MUST call increment_jump_counter()
        every time the player jumps. Otherwise they can jump infinitely.

        :param int allowed_jumps:
        """
        self.allowed_jumps = allowed_jumps
        self.allow_multi_jump = True

    def disable_multi_jump(self):
        """
        Disables multi-jump.

        Calling this function also removes the requirement to
        call increment_jump_counter() every time the player jumps.
        """
        self.allow_multi_jump = False
        self.allowed_jumps = 1
        self.jumps_since_ground = 0

    def jump(self, velocity: int):
        self.player_sprite.change_y = velocity
        self.increment_jump_counter()

    def increment_jump_counter(self):
        """
        Updates the jump counter for multi-jump tracking
        """
        if self.allow_multi_jump:
            self.jumps_since_ground += 1

    def update(self):
        """
        Move everything and resolve collisions.

        :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
        """
        if not self.is_on_ladder():
            self.player_sprite.change_y -= self.gravity_constant
        complete_hit_list = _move_sprite((self.player_sprite), (self.platforms), ramp_up=True)
        for platform in self.platforms:
            if not platform.change_x != 0:
                if platform.change_y != 0:
                    platform.center_x += platform.change_x
                    if platform.boundary_left is not None:
                        if platform.left <= platform.boundary_left:
                            platform.left = platform.boundary_left
                            if platform.change_x < 0:
                                platform.change_x *= -1
                    if platform.boundary_right is not None:
                        if platform.right >= platform.boundary_right:
                            platform.right = platform.boundary_right
                            if platform.change_x > 0:
                                platform.change_x *= -1
                    if check_for_collision(self.player_sprite, platform):
                        if platform.change_x < 0:
                            self.player_sprite.right = platform.left
                        if platform.change_x > 0:
                            self.player_sprite.left = platform.right
                    platform.center_y += platform.change_y
                    if platform.boundary_top is not None and platform.top >= platform.boundary_top:
                        platform.top = platform.boundary_top
                        if platform.change_y > 0:
                            platform.change_y *= -1
                if platform.boundary_bottom is not None and platform.bottom <= platform.boundary_bottom:
                    platform.bottom = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1

        return complete_hit_list