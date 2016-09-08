#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import queue
from enum import Enum

class Role(Enum):
    Merlin = 0
    Percival = 1
    Loyalist = 2
    Assassin = 3
    Morgana = 4
    Mordred = 5
    Oberon = 6
    Minion = 7

class Status(Enum):
    wait = 0
    make_team = 1
    team_vote = 2
    task_vote = 3
    assassin = 4
    end = 5

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
    
    def __init__(self, num, controller):
        self.mission_player_num = AvalonMachine.config['mission'][num]
        roles = AvalonMachine.config['role'][num][:]
        random.shuffle(roles)
        self.players = [Role(i) for i in roles]
        self.player_num = num
        self.controller = controller

        self.status = Status.wait
        self.current_round = 0
        self.current_try = 0
        self.current_team = []
        self.current_team_vote = []
        self.current_task_vote = []
        self.mission_result = [-1] * 5

        print("New game starting...")
        for i in range(num):
            print(i, self.players[i].name)
    
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
        elif self.players[player] in [Role.Morgana, Role.Assassin, Role.Mordred, Role.Minion]:
            for i in range(self.player_num):
                if self.players[i] in [Role.Morgana, Role.Assassin, Role.Mordred, Role.Minion]:
                    content.append(i)
        return {
            'role': self.players[player].value,
            'player_num': self.player_num,
            'content': content }

    def make_team(self, player_list):
        self.current_try += 1
        self.current_team = player_list
        self.current_team_vote = [-1] * self.player_num
        self.status = Status.team_vote
        self.controller.notify([], {
            'type': 'team-vote',
            'content': self.current_team
        })

    def team_vote(self, player, agree):
        self.current_team_vote[player] = 1 if agree else 0
        if -1 not in self.current_team_vote:
            self.controller.notify([], {
                'type': 'team-result',
                'content': self.current_team_vote
            })
            if self.current_team_vote.count(1) > self.player_num // 2:
                self.current_task_vote = [-1] * self.mission_player_num[self.current_round]
                self.status = Status.task_vote
                self.controller.notify(self.current_team, {
                    'type': 'task-vote',
                })
            else:
                if self.current_try == 5:
                    self.controller.notify([], {
                        'type': 'mission-result',
                        'result': False,
                        'good_vote_num': 0,
                        'bad_vote_num': 0
                    })
                    self.task_end(False)
                else:
                    self.current_try += 1
                    self.status = Status.make_team
                    self.controller.notify([], {
                        'type': 'make-team',
                        'num': self.mission_player_num[self.current_round]
                    })

    def task_vote(self, player, success):
        self.current_task_vote[player] = success
        if -1 not in self.current_task_vote:
            good_vote_num = self.current_task_vote.count(1)
            bad_vote_num = self.current_task_vote.count(0)
            result = self.is_mission_success(bad_vote_num)
            self.controller.notify([], {
                'type': 'mission-result',
                'result': result,
                'good_vote_num': good_vote_num,
                'bad_vote_num': bad_vote_num
            })
            self.task_end(result)

    def task_end(self, success):
        self.mission_result[self.current_round] = 1 if success else 0
        if self.mission_result.count(1) == 3:
            self.status = Status.assassin
            self.controller.notify([self.players.index(Role.Assassin)], {
                'type': 'assassin',
            })
        elif self.mission_result.count(0) == 3:
            self.status = Status.end
            self.controller.notify([], {
                'type': 'end',
                'result': False,
                'roles': [r.value for r in self.players]
            })
        else:
            self.current_round += 1
            self.status = Status.make_team
            self.controller.notify([], {
                'type': 'make-team',
                'num': self.mission_player_num[self.current_round]
            })

    def assassin(self, target):
        self.status = Status.end
        self.controller.notify([], {
            'type': 'end',
            'result': self.players[target] == Role.Merlin,
            'roles': [r.value for r in self.players]
        })

    def undo(self):
        if self.current_try > 0:
            self.current_try -= 1
        elif self.current_round > 0:
            self.current_round -= 1
            self.mission_result[self.current_round] = -1
            self.current_try = 4
        self.status = Status.make_team
        self.controller.notify([], {
            'type': 'make-team',
            'num': self.mission_player_num[self.current_round]
        })

    def is_mission_success(self, bad_vote_num):
        if (bad_vote_num == 0):
            return True
        elif (self.player_num >= 7 and self.current_round == 4 and bad_vote_num <= 1):
            return True
        else:
            return False

class Player(object):

    def __init__(self, player_id, name):
        self.mqueue = queue.Queue()
        self.player_id = player_id
        self.name = name

class MachineControl(object):
    
    def __init__(self, num):
        self.player_num = num
        self.machine = AvalonMachine(num, self)
        self.players = [Player(i, 'unknown') for i in range(num)]
        self.player_status = [0] * num

    def register(self, name, player_id = -1):
        if (player_id == -1):
            random_list = list(range(self.player_num))
            random.shuffle(random_list)
            for i in random_list:
                if self.player_status[i] == 0:
                    player_id = i
                    break
        else:
            if player_id < 0 or player_id >= self.player_num:
                raise Exception('Player id error.')
        self.player_status[player_id] = 1
        self.players[player_id].name = name
        self.notify([], {
            'type': 'register',
            'player_id': player_id,
            'name': name
        })
        if self.player_status.count(0) == 0 and self.machine.status == Status.wait:
            self.start()
        return player_id

    def start(self):
        self.machine.status = Status.make_team
        self.notify([], {
            'type': 'player-info',
            'content': [p.name for p in self.players]
        })
        self.notify([], {
            'type': 'make-team',
            'num': self.machine.mission_player_num[self.machine.current_round]
        })

    def unregister(self, player_id):
        if player_id < 0 or player_id >= self.player_num:
            raise Exception('Player id error.')
        self.player_status[player_id] = 0

    def get_init_info(self, player_id):
        init_info = self.machine.init_notify(player_id)
        init_info['type'] = 'init_info'
        return init_info

    def get_mq(self, player_id):
        return self.players[player_id].mqueue
    
    def notify(self, player_list, content):
        if player_list == []:
            player_list = list(range(self.player_num))
        for i in player_list:
            self.get_mq(i).put_nowait(content)
    
    def message(self, content):
        content['type'] = 'message'
        self.notify([], content)
    
    def make_team(self, player_id, team_list):
        self.machine.make_team(player_id, team_list)

    def team_vote(self, player_id, agree):
        self.machine.team_vote(player_id, agree)
        self.notify([], {
            'type': 'vote',
            'player_id': player_id
        })

    def task_vote(self, player_id, success):
        if player_id not in self.machine.current_team:
            return
        self.machine.task_vote(player_id, success)
        self.notify([], {
            'type': 'vote',
            'player_id': player_id
        })
    
    def assassin(self, player_id, target):
        if self.machine.players[player_id] is not Role.Assassin:
            return
        self.machine.assassin(target)
