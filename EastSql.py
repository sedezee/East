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
    __columns__ = ("guild_id", "show_admins", "time_zone", "military_time", "prefix", "scoreboard_pl", "date_format", "show_neg_points", "complex_scoring")


class OptionsTable(sql.Table):
    ROW_TYPE = OptionsRow


class ScoreboardRow(sql.Row):
    TABLE_NAME = "scoreboard"
    __columns__ = ("guild_id", "user_id", "neg_points", "pos_points", "points")


class ScoreboardTable(sql.Table):
    ROW_TYPE = ScoreboardRow


class ScoreStore(sql.Row):
    TABLE_NAME = "ScoreStore"
    __columns__ = ("guild_id", "title", "description", "price", "pos")


class ScoreStoreTable(sql.Table):
    ROW_TYPE = ScoreStore


class StoreItem:
    def __init__(self, guild_id, title, desc, price, positive):
        self.guild_id = guild_id
        self.title = title
        self.desc = desc
        self.price = price
        self.positive = positive

    @staticmethod
    def from_row(row):
        return StoreItem(getattr(row, "guild_id"), getattr(row, "title"), getattr(row, "description"), getattr(row, "price"), getattr(row, "pos"))

    def to_row(self):
        return ScoreStore(f"'{self.guild_id}'", f"'{self.title}'", f"'{self.desc}'", self.price, self.positive)

    def __str__(self):
        return f"Title: {self.title}\nDesc: {self.desc}\nPrice: {self.price}"


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

    def manage_user_points(self, table_data, row_data, give = True):
        """
        Searches by user_id and guild_id to determine if user is already in db.
        :param table_data: the table to search
        :param row_data: the row to search for
        """
        user_id = getattr(row_data, "user_id")
        guild_id = getattr(row_data, "guild_id")
        pos_points = getattr(row_data, "pos_points")
        neg_points = getattr(row_data, "neg_points")

        for row in table_data:
            getattr_uid = getattr(row, "user_id")
            getattr_gid = getattr(row, "guild_id")
            if user_id == f"'{getattr_uid}'" and guild_id == f"'{getattr_gid}'":
                tot_neg = getattr(row, "neg_points") + neg_points if give else getattr(row, "neg_points") - neg_points
                tot_pos = getattr(row, "pos_points") + pos_points if give else getattr(row, "pos_points") - pos_points
                setattr(row, "neg_points", tot_neg)
                setattr(row, "pos_points", tot_pos)
                setattr(row, "points", tot_neg + tot_pos)

                self.update_item(row, guild_id = guild_id, user_id = user_id)
                return
        setattr(row_data, "points", pos_points + neg_points)
        self.sort_table(OptionsRow, "points")
        self.insert_item(row_data)

    def sort_table(self, t_type, *args):
        """
        :param t_type: type of table/row to order
        :param args: what to order it by
        """
        query = f"SELECT * FROM {self._schema}.{t_type.table_name()} ORDER BY"
        for arg in args:
            query += f" {arg} ASC,"

        print(query[:-1])
        self.execute("SELECT * FROM east_schema.scoreboard ORDER BY points DESC;")

