import json
import pandas as pd

with open('gameData.json', 'r') as file:
    game_data = json.load(file)

df = pd.DataFrame(game_data)
print(df)

# 计算胜率、失败率和平局率
# win_rate = df[df['result'].str.contains('Wins')].shape[0] / df.shape[0]
# lose_rate = df[df['result'].str.contains('Busted') | df['result'].str.contains('Dealer Wins')].shape[0] / df.shape[0]
# draw_rate = df[df['result'].str.contains('Ties')].shape[0] / df.shape[0]
# soft_hand_rate = df[df['isSoft']].shape[0] / df.shape[0]

# # 打印结果
# print(f'Win Rate: {win_rate:.2%}')
# print(f'Lose Rate: {lose_rate:.2%}')
# print(f'Draw Rate: {draw_rate:.2%}')
# print(f'Soft Hand Rate: {soft_hand_rate:.2%}')

# # 显示更多统计信息
# print("\nDetailed Results:")
# print(df['result'].value_counts())

