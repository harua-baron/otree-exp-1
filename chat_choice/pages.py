from otree.api import Page, WaitPage
from .models import Group, check_timeout_and_missing_e, check_timeout_and_missing_q


class CooperationPage(Page):
    form_model = "player"
    form_fields = ["chat_choice"]
    timeout_seconds = 30

    def before_next_page(self):
        if self.timeout_happened and not self.player.chat_choice:
            self.player.chat_choice = "N"


# チャットの前の待機ページ
# 全員がC or N　を選択した上でChatのページを開く必要がある
class CooperationChoiceWaitPage(WaitPage):
    # 処理なし
    pass

class ChatPage(Page):
    form_model = "player"
    form_fields = []
    timeout_seconds = 60
    live_method = "live_chat"

    # テンプレート（〜.html）に渡す変数
    def vars_for_template(self):
        is_cooperation = self.group.is_cooperation_established_for_team(
            self.player.team()
        )

        return {
            # チームの協力が確立されているかどうかを判定
            "is_cooperation_established_for_team": is_cooperation,
            "chat_log": (
                self.player.group.chat_log_team1 
                if self.player.team() == 1
                else self.player.group.chat_log_team2
            ),
        }

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timed_out = True


class EChoice(Page):
    form_model = "player"
    form_fields = ["e"]
    timeout_seconds = 30  # 任意で制限時間を設定


    def vars_for_template(self):
        # チームの協力状況やチャットログも表示しても良い
        is_cooperation = self.group.is_cooperation_established_for_team(self.player.team())
        chat_log = (
            self.player.group.chat_log_team1 if self.player.team() == 1 else self.player.group.chat_log_team2
        )
        return {
            "is_cooperation_established_for_team": is_cooperation,
            "chat_log": chat_log,
            "team": self.player.team(),
        }

    def before_next_page(self):
        if self.timeout_happened or self.player.e == 0:
            self.player.timed_out = True


class ResultsWaitPage1(WaitPage):
    wait_for_all_groups = True  # 全グループが揃うのを待つ（任意）

    # wait_for_all_groups = Trueを実装すると引数はGroupではなくsubsessionになる
    @staticmethod
    def after_all_players_arrive(subsession):
        # Subsession内のグループごとにpayoffを設定
        for group in subsession.get_groups():
            # eを選択した後にGroupごとに計算したい処理を呼び出す
            # TODO: e選択後の処理を実装する（sample_calculate_after_select_eはサンプルの実装なので適宜削除してください）
            group.sample_calculate_after_select_e
            # group.set_payoffs() set_payoffsメソッドはQを選択したあとに実行する関数だからここでは実行しないはず

    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate


class MarketShare(Page):
    def vars_for_template(self):
        team_e_total = self.group.get_team_e_total(self.player.team())
        group_e_total = self.group.get_group_e_total()
        market_share = (
            (36 * team_e_total / group_e_total) if group_e_total != 0 else 0
        )

        # 小数第2位で四捨五入
        market_share = (
            round(36 * team_e_total / group_e_total) if group_e_total != 0 else 0
        )

        return {"market_share": market_share}

    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate

    timeout_seconds = 10  # 時間制限あり


class QChoice(Page):
    form_model = "player"
    form_fields = ["q"]
    timeout_seconds = 30
    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate

    def before_next_page(self):
        if self.timeout_happened or self.player.q == 0:
            self.player.timed_out = True


class ResultsWaitPage2(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate


# E値を未選択&タイムアウトしていないかチェックする
class CheckTimeoutAndMissingE(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        for group in subsession.get_groups():
            # e値が未選択またはタイムアウトした人がいる場合、強制終了する
            check_timeout_and_missing_e(group)

    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate


# Q値を未選択&タイムアウトしていないかチェックする
class CheckTimeoutAndMissingQ(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        for group in subsession.get_groups():
            # q値が未選択またはタイムアウトした人がいる場合、強制終了する
            check_timeout_and_missing_q(group)

    # 前のページで未選択＆強制終了した人がいたらこのページは表示しない
    def is_displayed(self):
        return not self.group.force_terminate


class Results(Page):
    timeout_seconds = 10

    def is_displayed(self):
        return not self.group.force_terminate

    def vars_for_template(self):
        return {
            "price": round(
                self.player.group.P1
                if self.player.market() == 1
                else self.player.group.P2
            ),
            "profit": self.player.profit,
            "chat_log": (
                self.player.group.chat_log_team1
                if self.player.team() == 1
                else self.player.group.chat_log_team2
            ),
        }


class ForcedTermination(Page):
    def is_displayed(self):
        return self.group.force_terminate

    def vars_for_template(self):
        return {
            "message": "1人以上が時間内に選択できなかったため、全員強制終了となりました。"
        }
    

class BreakPage1(Page):
    timeout_seconds = 10

    def is_displayed(self):
        return self.round_number == 7  # 7セット目の後に表示
    

page_sequence = [
    CooperationPage,
    CooperationChoiceWaitPage,
    ChatPage,
    EChoice,
    CheckTimeoutAndMissingE,  # この画面で「e値未選択&タイムアウト」のチェックを行う
    ResultsWaitPage1,
    MarketShare,
    QChoice,
    CheckTimeoutAndMissingQ,  # この画面で「q値未選択&タイムアウト」のチェックを行う
    ResultsWaitPage2,
    Results,
    ForcedTermination,
    BreakPage1,
]






