import sys

import psycopg2

sys.path.append('C:\\Dev\\SedezCompendium')

import tokens_and_pswds as tap
import sedezcompendium.common as sql

class AdminRow(sql.Row):
    TABLE_NAME = "admins"
    __columns__ = ("guild_id", "user_id")


class AdminTable(sql.Table):
    ROW_TYPE = AdminRow


class OptionsRow(sql.Row):
    TABLE_NAME = "options"
    __columns__ = ("guild_id", "show_admins", "time_zone", "military_time", "prefix", "scoreboard_pl")


class OptionsTable(sql.Table):
    ROW_TYPE = OptionsRow


class ScoreboardRow(sql.Row):
    TABLE_NAME = "scoreboard"
    __columns__ = ("guild_id", "user_id", "points")


class ScoreboardTable(sql.Table):
    ROW_TYPE = ScoreboardRow


class EastDatabase(sql.GenericDatabase):
    def get_all_admins(self):
        """
        Get a list of all of the admins from every server.
        """
        try:
            return self.get_items(AdminTable)
        except psycopg2.ProgrammingError:
            return None

    def get_admins(self, guild_id):
        """
        Get the admins from a particular guild
        """
        try:
            return self.get_items(AdminTable, guild_id = f"'{guild_id}'")
        except psycopg2.ProgrammingError:
            return None

    def get_admin(self, guild_id, user_id):
        try:
            return self.get_item(AdminTable, guild_id = f"'{guild_id}'", user_id = f"'{user_id}'")
        except psycopg2.ProgrammingError:
            return None