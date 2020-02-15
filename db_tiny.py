from tinydb import TinyDB, Query


class BakkunDB(object):
    def __init__(self):
        # データベースの作成
        self.db = TinyDB('bakkundb.json', indent=2, ensure_ascii=False)
        self.que = Query()

        self.friendsdb = self.db.table("friends")
        self.groupdb = self.db.table("groups")

    def update_user(self, user):
        try:
            res = self.friendsdb.search(self.que.uid == user["uid"])[0]
            self.friendsdb.update(user, self.que.uid == user["uid"])
        except IndexError:
            self.friendsdb.insert(user)

    def unfollow_user(self, uid: str):
        try:
            res = self.friendsdb.search(self.que.uid == uid)[0]
            self.friendsdb.update(
                {"follow": False}, self.que.uid == uid)
        except IndexError:
            self.friendsdb.insert({"uid": uid, "follow": False})

    def add_user_to_group(self, uid: str, group: str):
        try:
            res = self.groupdb.search(self.que.name == group)[0]
            members = res.get("members", [])

            if uid in members:
                return
            else:
                self.groupdb.update(
                    {"members": members + [uid]}, self.que.name == group)
        except IndexError:
            self.groupdb.insert({"name": group, "members": [uid]})

    def get_group_from_uid(self, uid: str):
        for group in self.groupdb.all():
            if uid in group["members"]:
                return group["name"]
        return None

    def get_group_members(self, group: str):
        try:
            res = self.groupdb.search(self.que.name == group)[0]
            return res.get("members", [])
        except IndexError:
            return []

    def delete_group(self, group: str):
        try:
            self.groupdb.remove(self.que.name == group)
        except IndexError:
            pass
