import mj
import random
import numpy as np
import torch
num_actions = 35


class SimplifiedMahjongEnv:
    def __init__(self, model):
        self.state = None
        self.done = False
        self.model = model
        self.hist_fan = []

    def reset(self):
        self.initialize_state()
        self.done = False
        self.buffer = []
        self.step_count = 0
        return self.state

    def step(self, discard_by=None):
        self.step_count += 1
        if not discard_by:
            discard_by = self.discard_by_model
        if self.done:
            raise ValueError("Episode has ended, please reset the environment.")

        p = self.state['hand']
        if len(p) < 14:
            reward = 0
            self.this_fan = 0
            self.this_fans = []
        else:
            reward = mj.quick_calc(p)
            reward, fans = mj.quick_calc_detail(p)
            self.this_fan = reward
            #if reward > 0:
            #    print(reward, fans)
            for fan in fans:
                if fan not in self.hist_fan:
                    self.hist_fan.append(fan)
            self.this_fans = fans
        self.done = reward >= 8 or self.is_deck_empty()

        reward /= (min(len(self.state['discarded']), 10) + 10)
        last_state = self.state2array()
        if not self.done:

            # discard
            discard_tile = discard_by()
            self.state['hand'].remove(discard_tile)
            self.state['discarded'].append(discard_tile)
            self.state['hand'].sort()

            # draw
            self.state['hand'].append(self.draw_tile())
            self.state['hand'].sort()
        else:
            # 回溯奖励
            if self.this_fan ==0:
                step_reward = 0
            reward = (reward - 8) + 10 *(21 - self.step_count) 
            step_reward = reward / 100
            for i in range(len(self.buffer) - 1):
                self.buffer[i][2] = step_reward
            discard_tile = 0

        self.buffer.append([last_state, discard_tile, reward, self.state2array(), self.done, reward])

    def render(self):
        print(len(self.state['pool']), self.state['hand'])

    def initialize_state(self):
        pool = [i for i in range(1, 35) for _ in range(4)]
        random.shuffle(pool)
        ret = {'hand': [], 'pool': pool, 'discarded': []}
        while len(ret['hand']) <14:
            ret['hand'].append(pool.pop())
        self.state = ret

    def discard_strategy1 (self):
        hand = self.state['hand']
        tile_counts = [0] * 34
        for tile in hand:
            tile_counts[tile - 1] += 1
        
        # 优先丢弃字牌（风牌和箭牌）
        discard_candidates = [i + 1 for i in range(27, 34) if tile_counts[i] > 0]

        # 找出手中的数牌
        for i in range(27):
            if tile_counts[i] > 0:
                # 判断是否是孤张
                is_isolated = True
                if i > 1 and tile_counts[i - 2] > 0:  # i-2
                    is_isolated = False
                if i > 0 and tile_counts[i - 1] > 0:  # i-1
                    is_isolated = False
                if i < 26 and tile_counts[i + 1] > 0:  # i+1
                    is_isolated = False
                if i < 25 and tile_counts[i + 2] > 0:  # i+2
                    is_isolated = False
                if is_isolated:
                    discard_candidates.append(i + 1)

        # 如果有候选牌，随机选择一个丢弃
        if discard_candidates:
            return random.choice(discard_candidates)
        else:
            # 如果没有孤张或字牌，随机丢弃一张牌
            return random.choice(hand)

    def discard_rand (self, hand):
        hand = self.state['hand']
        return random.choice(hand)

    def discard_by_model(self):
        hand = self.state['hand']
        q_values = self.model(self.state2array()).detach().numpy().flatten()
        discard_tile = min(hand, key=lambda x: q_values[x])
        return discard_tile

    def discard_by_model_reverse (self):
        hand = self.state['hand']
        q_values = self.model(self.state2array()).detach().numpy().flatten()
        discard_tile = max(hand, key=lambda x: q_values[x])
        return discard_tile

    def state2array (self):
        next_hand_array = torch.zeros(num_actions)
        for tile in self.state['hand']:
            next_hand_array[tile-1] += 1
        return next_hand_array

    def draw_tile(self):
        return self.state['pool'].pop()

    def is_deck_empty(self):
        return len(self.state['pool']) == 0


if __name__ == '__main__':
    # 使用示例
    env = SimplifiedMahjongEnv()
    state = env.reset()
    done = False
    best_reward = 0
    while best_reward == 0:
        while not done:
            action = env.action_space.sample(state)
            next_state, reward, done = env.step(action)
            #env.render()
        print(f"Action: {action}, Reward: {reward}, Done: {done}")
        best_reward = max(reward, best_reward)