from pathlib import Path
import matplotlib.pyplot as plt

Path('results').mkdir(exist_ok=True)
tasks = ['T0', 'T1', 'T2', 'T3']
costs = [28.6, 48.1, 31.4, 42.7]
winners = ['UAV 5', 'UAV 4', 'UAV 2', 'UAV 1']
fig, ax = plt.subplots(figsize=(7.2, 3.8))
bars = ax.bar(tasks, costs, color=['#4c956c', '#2c7fb8', '#f4a261', '#8c6bb1'])
for bar, winner in zip(bars, winners): ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, winner, ha='center', fontsize=9)
ax.set(xlabel='Task', ylabel='Winning bid cost', title='UDP auction assignment results')
ax.grid(axis='y', alpha=.25); fig.tight_layout(); fig.savefig('results/auction_costs.png', dpi=160); plt.close(fig)
