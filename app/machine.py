#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import queue
import json
from enum import Enum

class Role(Enum):
    Merlin = 0
    Percival = 1
    Loyalist = 2
    Assassin = 3
    Morgana= 4
    Modred = 5
    Oberon = 6
    Minion = 7

class AvalonMachine(object):

    config = {
        'role' : {
            5 : [0, 1, 2, 3, 4],
            6 : [0, 1, 2, 2, 3, 4],
            7 : [0, 1, 2, 2, 3, 4, 6],
            8 : [0, 1, 2, 2, 2, 3, 4, 7],
            9 : [0, 1, 2, 2, 2, 2, 3, 4, 5],
            10: [0, 1, 2, 2, 2, 2, 3, 4, 5, 6]
        },
        'mission' : {
            5 : [2, 3, 2, 3, 3],
            6 : [2, 3, 4, 3, 4],
            7 : [2, 3, 3, 4, 4],
            8 : [3, 4, 4, 5, 5],
            9 : [3, 4, 4, 5, 5],
            10: [3, 4, 4, 5, 5]
        },
    }
    
    def __init__(self, num):
        self.mission_player_num = AvalonMachine.config['mission']
        roles = AvalonMachine.config['role'][num][:]
        random.shuffle(roles)
        self.players = [Role(i) for i in roles]
        self.player_num = num

        self.status = 'make_team'
        self.current_round = 0
        self.current_try = 0
        self.current_team = []
        self.current_team_vote = []
        self.current_task_vote = []
        self.mission_result = [-1] * 5
        self.mq = queue.Queue()

        print("New game starting...")
        for i in range(num):
            print(i, self.players[i])

    def get_roles(self):
        return self.players[:]
    
    def init_notify(self, player):
        content = []
        if self.players[player] == Role.Merlin:
            for i in range(self.player_num):
                if self.players[i] in [Role.Morgana, Role.Assassin, Role.Oberon, Role.Minion]:
                    content.append(i)
        elif self.players[player] == Role.Percival:
            for i in range(self.player_num):
                if self.players[i] in [Role.Merlin, Role.Morgana]:
                    content.append(i)
        elif self.players[player] in [Role.Morgana, Role.Assassin, Role.Modred, Role.Minion]:
            for i in range(self.player_num):
                if self.players[i] in [Role.Morgana, Role.Assassin, Role.Modred, Role.Minion]:
                    content.append(i)
        return { 'role': self.players[player].value, 'target': player, 'content': content }

    def make_team(self, player_list):
        self.current_try += 1
        self.current_team = player_list
        self.current_team_vote = [-1] * self.player_num
        self.status = 'team_vote'

    def team_vote(self, player, agree):
        self.current_team_vote[player] = 1 if agree else 0
        if -1 not in self.current_team_vote:
            if self.current_team_vote.count(1) > self.player_num // 2:
                self.current_task_vote = [-1] * self.mission_player_num[self.current_round]
                self.status = 'task_vote'
            else:
                if self.current_try == 5:
                    self.task_end(False)
                else:
                    self.current_try += 1
                    self.status = 'make_team'

    def task_vote(self, player, success):
        self.current_task_vote[player] = 1 if success else 0
        if -1 not in self.current_task_vote:
            good_vote_num = self.current_task_vote.count(1)
            bad_vote_num = self.current_task_vote.count(0)
            result = self.is_mission_success(bad_vote_num)
            self.task_end(result)

    def task_end(self, success):
        self.mission_result[self.current_round] = 1 if success else 0
        if self.mission_result.count(1) == 3:
            self.status = 'assassin'
        elif self.mission_result.count(0) == 3:
            self.status = 'end'

    def assassin(self, target):
        self.status = 'end'
        return self.players[target] == 'Merlin'

    def undo(self):
        if self.current_try > 0:
            self.current_try -= 1
        elif self.current_round > 0:
            self.current_round -= 1
            self.mission_result[self.current_round] = -1
            self.current_try = 4
        self.status = 'make_team'

    def is_mission_success(self, bad_vote_num):
        if (bad_vote_num == 0):
            return True
        elif (self.player_num >= 7 and self.current_round == 4 and bad_vote_num <= 1):
            return True
        else:
            return False

class MachineControl(object):
    
    def __init__(self, num):
        self.machine = AvalonMachine(num)
        self.message_queues = [queue.Queue() for i in range(num)]

    
