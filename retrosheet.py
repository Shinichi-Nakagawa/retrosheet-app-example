#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

from model import t_rosters as Roster
from model import t_LKUP_CD_EVENT as LookupEvent
from model import t_LKUP_CD_BATTEDBALL as LookupBattedBall
from model import Game, Event

from pitch_seq import EN_PITCH_SEQ_DICT

from sqlalchemy import *
from sqlalchemy.orm import *


class RetroSheet(object):

    def __init__(self, connection, encoding):
        self.engine = create_engine(connection, encoding=encoding)
        Session = sessionmaker(bind=self.engine, autoflush=True)
        Session.configure(bind=self.engine)
        self.session = Session()

    def batted_ball_pie_data(self, player_id, from_date, to_date):
        """
        :param player_id:
        :param from_date:
        :param to_date:
        :return: labels, values
        """
        battedball =\
            {
                "Fly Ball": 0,
                "Ground Ball": 0,
                "Line Drive": 0,
                "Pop Up": 0
            }
        for event in self.find_events_batting_by_player_id_year(player_id, from_date, to_date):
            at_bat_batted = self.find_cd_batted_ball(event.BATTEDBALL_CD)
            if at_bat_batted is None:
                continue
            else:
                battedball[at_bat_batted.LONGNAME_TX] = battedball[at_bat_batted.LONGNAME_TX] + 1
        labels, values = [], []
        for k, v in battedball.items():
            labels.append("{k}({v})".format(k=k, v=v))
            values.append(v)
        return labels, values

    def pitch_seq(self, seq):
        pitch_seq = []
        i = 1
        for pitch in seq:
            pitch_seq.append(
                """
                {cnt} Pitch:{pitch}
                """.format(
                    cnt=i,
                    pitch=EN_PITCH_SEQ_DICT.get(pitch, "Unknown")
                )
            )
            i = i + 1
        return "\n".join(pitch_seq)

    def result_at_bat(self, event, batter, cnt):
        pitcher = self.find_player_by_player_id_year(event.PIT_ID, batter.YEAR)
        at_bat_event = self.find_cd_event(event.EVENT_CD)
        at_bat_batted = self.find_cd_batted_ball(event.BATTEDBALL_CD)
        if at_bat_batted is None:
            batted = ""
        else:
            batted = at_bat_batted.LONGNAME_TX
        return """
        At Bat({cnt})
        Batter  :{b_first_name} {b_last_name}
        Pitcher :{p_first_name} {p_last_name}
        At Bat  :{atbat}
        Batted  :{batted}
        Pitching:
        {pitch}
        """.format(
            cnt=cnt,
            b_first_name=batter.FIRST_NAME_TX,
            b_last_name=batter.LAST_NAME_TX,
            p_first_name=pitcher.FIRST_NAME_TX,
            p_last_name=pitcher.LAST_NAME_TX,
            atbat=at_bat_event.LONGNAME_TX,
            batted=batted,
            pitch=self.pitch_seq(event.PITCH_SEQ_TX)
        )

    def find_cd_event(self, cd):
        return self._find_cd(LookupEvent, cd)

    def find_cd_batted_ball(self, cd):
        return self._find_cd(LookupBattedBall, cd)

    def find_player_by_player_id_year(self, player_id, year):
        query = self.session.query(Roster)
        return query.filter_by(PLAYER_ID=player_id).filter_by(YEAR=year).first()

    def find_player_by_fullname_year(self, first_name, last_name, year):
        query = self.session.query(Roster)
        return query.filter_by(FIRST_NAME_TX=first_name).filter_by(LAST_NAME_TX=last_name).filter_by(YEAR=year).first()

    def find_events_batting_by_player_id_year(self, player_id, from_date, to_date):
        return self._find_events_batting_by_player_id_and_lexer(player_id, Game.GAME_DT.between(from_date, to_date))

    def find_events_batting_by_player_id_date(self, player_id, game_dt):
        return self._find_events_batting_by_player_id_and_lexer(player_id, Game.GAME_DT == game_dt)

    def _find_events_batting_by_player_id_and_lexer(self, player_id, lexer):
        query = self.session.query(Event).select_from(join(Event, Game, Event.GAME_ID == Game.GAME_ID))
        return query.\
            filter(Event.BAT_ID == player_id).\
            filter(lexer).\
            order_by(Game.GAME_DT).\
            order_by(Game.GAME_CT).\
            order_by(Event.INN_CT).\
            all()

    def _find_cd(self, table, cd):
        query = self.session.query(table)
        return query.filter_by(VALUE_CD=cd).first()
