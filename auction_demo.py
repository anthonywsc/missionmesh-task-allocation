import argparse
import asyncio
import json
import math
import random


class Station(asyncio.DatagramProtocol):
    def __init__(self, expected): self.expected, self.bids = expected, []
    def connection_made(self, transport): self.transport = transport
    def datagram_received(self, data, _addr): self.bids.append(json.loads(data.decode()))


async def run(args):
    loop = asyncio.get_running_loop(); rng = random.Random(args.seed)
    station = Station(args.tasks)
    station_transport, _ = await loop.create_datagram_endpoint(lambda: station, local_addr=("127.0.0.1", args.station_port))
    tasks = [{"task_id": i, "x": rng.uniform(-50, 50), "y": rng.uniform(-50, 50), "payload": 1 + i % 3} for i in range(args.tasks)]
    vehicles = [{"agent_id": i, "x": i * 12 - 30, "y": (i % 2) * 20, "battery": 55 + i * 7, "payload": 1 + i % 3} for i in range(args.agents)]
    try:
        for task in tasks:
            candidates = []
            for v in vehicles:
                if v["payload"] < task["payload"] or v["battery"] < 20: continue
                distance = math.hypot(v["x"] - task["x"], v["y"] - task["y"])
                candidates.append({"type": "BID", "task_id": task["task_id"], "agent_id": v["agent_id"], "cost": round(distance + (100 - v["battery"]) * 0.08, 3)})
            for bid in candidates:
                station_transport.sendto(json.dumps(bid).encode(), ("127.0.0.1", args.station_port))
            await asyncio.sleep(0.01)
            bids = [b for b in station.bids if b["task_id"] == task["task_id"]]
            winner = min(bids, key=lambda b: b["cost"], default=None)
            print(f"task={task['task_id']} payload={task['payload']} winner=" + (f"UAV {winner['agent_id']} cost={winner['cost']:.3f}" if winner else "none"))
    finally:
        station_transport.close()


def main():
    p = argparse.ArgumentParser(); p.add_argument("--agents", type=int, default=6); p.add_argument("--tasks", type=int, default=4)
    p.add_argument("--station-port", type=int, default=18000); p.add_argument("--seed", type=int, default=23)
    asyncio.run(run(p.parse_args()))


if __name__ == "__main__": main()
