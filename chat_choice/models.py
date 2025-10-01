from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "chat_choice"
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 7
    E_CHOICES = list(range(16, 38, 2))  # 16~36の偶数
    Q_CHOICES = [2, 4, 6, 8, 10]
    CHAT_CHOICES = [("C", "協力する"), ("N", "協力しない")]  # チャット選択肢


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            players = self.get_players()
            import random
            random.shuffle(players)

            # 2人ペアを作る
            pairs = [players[i:i+2] for i in range(0, len(players), 2)]

            # そのペアを2組まとめて4人グループにする
            groups = [pairs[i] + pairs[i+1] for i in range(0, len(pairs), 2)]

            # グループをセット
            self.set_group_matrix(groups)

        else:
            # 2〜7ラウンドは1ラウンド目と同じグループを維持
            self.group_like_round(1)


class Group(BaseGroup):
    total_e = models.IntegerField()
    chat_log_team1 = models.LongStringField(blank=True, default="")  # チーム1用チャットログ
    chat_log_team2 = models.LongStringField(blank=True, default="")  # チーム2用チャットログ
    force_terminate = models.BooleanField(initial=False)
    P1 = models.FloatField()
    P2 = models.FloatField()

    # team全員がC：協力するを選択しているか判定する
    def is_cooperation_established_for_team(self, team_number):
        team_players = [p for p in self.get_players() if p.team() == team_number]
        return all(
            p.chat_choice == "C" for p in team_players if p.chat_choice is not None
        )

    # 各市場ごとの需要を出すのにEの合計を出す
    def get_team_e_total(self, team_number):
        return sum(
            p.e
            for p in self.get_players()
            if p.team() == team_number and p.e is not None
        )

    def get_group_e_total(self):
        return sum(p.e for p in self.get_players() if p.e is not None)

    # eを選択した後にGroupごとに計算したい処理
    def calculate_market_share(self, player):
        team_e_total = self.get_team_e_total(player.team())
        group_e_total = self.get_group_e_total()
        market_share = round(36 * team_e_total / group_e_total) if group_e_total != 0 else 0
        return {"market_share": market_share}

    # 各グループのpayoffを計算するメソッド
    def set_payoffs(self):
        players = self.get_players()
        total_e = sum(p.e for p in players)

        e1, e2, e3, e4 = players[0].e, players[1].e, players[2].e, players[3].e
        q1, q2, q3, q4 = players[0].q, players[1].q, players[2].q, players[3].q

        e12 = e1 + e2
        e34 = e3 + e4
        q12 = q1 + q2
        q34 = q3 + q4

        # 価格計算（安全にゼロ除算回避）
        self.P1 = max(0, 36 - (total_e / e12) * q12) if e12 > 0 else 0
        self.P2 = max(0, 36 - (total_e / e34) * q34) if e34 > 0 else 0

        for p in players:
            price = round(self.P1) if p.market() == 1 else round(self.P2)
            raw_profit = price * p.q - p.e
            p.profit = max(0, round(raw_profit))  # 四捨五入しつつ負をゼロに
            p.payoff = p.profit


class Player(BasePlayer):
    chat_choice = models.StringField(
        choices=C.CHAT_CHOICES,
        label="以下から選択してください",
        blank=True
    )
    e = models.IntegerField(
        choices=C.E_CHOICES,
        label="以下から選択してください"
    )
    q = models.IntegerField(
        choices=C.Q_CHOICES,
        label="以下から選択してください"
    )
    profit = models.IntegerField()  # payoffに合わせて整数に変更
    chat_log = models.LongStringField(blank=True, default="")
    timed_out = models.BooleanField(initial=False)

    def market(self):
        return 1 if self.id_in_group in [1, 2] else 2

    def team(self):
        return 1 if self.id_in_group in [1, 2] else 2

    # チャットを送信するメソッド
    def live_chat(self, message):
        team = self.team()
        group = self.group
        label = self.participant.label or f"P{self.id_in_group}"
        text = f"{label}: {message}"
        print(f"[live_chat] player {self.id_in_group} (team {team}) sent message: {text}")

        # チャットログをグループで記録
        if team == 1:
            group.chat_log_team1 += f"\n{text}" if group.chat_log_team1 else text
        else:
            group.chat_log_team2 += f"\n{text}" if group.chat_log_team2 else text

        # 同じチームの全プレイヤーに送信
        return {p.id_in_group: text for p in group.get_players() if p.team() == team}


# 修正版: タイムアウトチェック
def check_timeout_and_missing_e(group: Group, **kwargs):
    group.force_terminate = any(p.timed_out or p.e is None for p in group.get_players())


def check_timeout_and_missing_q(group: Group, **kwargs):
    group.force_terminate = any(p.timed_out or p.q is None for p in group.get_players())






