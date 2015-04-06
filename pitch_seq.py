#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Shinichi Nakagawa'

'''
    +  following pickoff throw by the catcher
    *  indicates the following pitch was blocked by the catcher
    .  marker for play not involving the batter
    1  pickoff throw to first
    2  pickoff throw to second
    3  pickoff throw to third
    >  Indicates a runner going on the pitch

    B  ball
    C  called strike
    F  foul
    H  hit batter
    I  intentional ball
    K  strike (unknown type)
    L  foul bunt
    M  missed bunt attempt
    N  no pitch (on balks and interference calls)
    O  foul tip on bunt
    P  pitchout
    Q  swinging on pitchout
    R  foul ball on pitchout
    S  swinging strike
    T  foul tip
    U  unknown or missed pitch
    V  called ball because pitcher went to his mouth
    X  ball put into play by batter
    Y  ball put into play on pitchout
'''


EN_PITCH_SEQ_DICT = {
    '+': 'following pickoff throw by the catcher',
    '*': 'indicates the following pitch was blocked by the catcher',
    '.': 'marker for play not involving the batter',
    '1': 'pickoff throw to first',
    '2': 'pickoff throw to second',
    '3': 'pickoff throw to third',
    '>': 'Indicates a runner going on the pitch',
    'B': 'ball',
    'C': 'called strike',
    'F': 'foul',
    'H': 'hit batter',
    'I': 'intentional ball',
    'K': 'strike (unknown type)',
    'L': 'foul bunt',
    'M': 'missed bunt attempt',
    'N': 'no pitch (on balks and interference calls)',
    'O': 'foul tip on bunt',
    'P': 'pitchout',
    'Q': 'swinging on pitchout',
    'R': 'foul ball on pitchout',
    'S': 'swinging strike',
    'T': 'foul tip',
    'U': 'unknown or missed pitch',
    'V': 'called ball because pitcher went to his mouth',
    'X': 'ball put into play by batter',
    'Y': 'ball put into play on pitchout',
}

JA_PITCH_SEQ_DICT = {
    '+': 'following pickoff throw by the catcher',
    '*': 'indicates the following pitch was blocked by the catcher',
    '.': 'marker for play not involving the batter',
    '1': '一塁牽制',
    '2': '二塁牽制',
    '3': '三塁牽制',
    '>': 'ランナースタート',
    'B': 'ボール',
    'C': '見逃し',
    'F': 'ファール',
    'H': '安打',
    'I': '四球',
    'K': 'ストライク',
    'L': 'ファウルバント',
    'M': 'missed bunt attempt',
    'N': 'no pitch (on balks and interference calls)',
    'O': 'foul tip on bunt',
    'P': 'アウト',
    'Q': '空振り三振',
    'R': 'ファウルフライ',
    'S': '空振り',
    'T': 'ファウルチップ',
    'U': 'unknown or missed pitch',
    'V': 'called ball because pitcher went to his mouth',
    'X': 'インプレー(ノーアウト)',
    'Y': 'インプレー(アウト)',
}

