#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import queue

class AvalonMachine(object):

    config = {
        'roles' : ( 'Merlin', 'Percival', 'Loyalist', 'Assassin', 'Morgana', 'Modred', 'Oberon', 'Minion' ),
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
    
    def __init__(self, num, **args):
        self.mission_player_num = AvalonMachine.config['mission']
        roles = AvalonMachine.config['role'][num][:]
        random.shuffle(roles)
        self.player_num = num
        self.players = [AvalonMachine.config['roles'][i] for i in roles]

        self.status = 'make_team'
        self.current_round = 0
        self.current_try = 0
        self.mission_result = [-1] * 5

        print("New game starting...")
        for i in range(num):
            print(i, self.players[i])

    def get_roles(self):
        return self.players[:]
    
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
                    self.status = 'make_team'

    def task_vote(self, player, success):
        pass

    def task_end(self, success):
        pass

    def assassin(self, target):
        self.status = 'end'
        return self.players[target] == 'Merlin'

    def is_mission_success(self, bad_vote_num):
        if (bad_vote_num == 0):
            return True
        elif (self.player_num >= 7 && self.current_round == 4 && bad_vote_num <= 1):
            return True
        else:
            return False

class MachineControl(object):
    
    def __init__(self, num, **args):
        self.machine = AvalonMachine(num, **args)
        self.message_queues = [queue.Queue() for i in range(num)]

    
