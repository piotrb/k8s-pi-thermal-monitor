import asyncio
import signal
import os
import aiofiles
import aiofiles.base

from simple_pid import PID

THERMAL_ZONE = os.environ.get("THERMAL_ZONE", "/sys/class/thermal/thermal_zone0/temp")
SETPOINT = float(os.environ.get("SETPOINT", "40"))

async def get_system_temp():
  async with aiofiles.open(THERMAL_ZONE) as f:
    rawTemp = await f.read()
    return float(rawTemp) / 1000

loop_running = True

async def main():
    print("Starting update loop")
    await update_loop(setpoint=SETPOINT)
    print("Exiting update loop")

async def update_loop(setpoint: float):
    pid = PID(1, 0.1, 0.05, setpoint=setpoint)
    while loop_running:
        temp = await get_system_temp()
        v = pid(temp)
        print(f"temp: {temp} v: {v}")
        await asyncio.sleep(1)

def sigint_handler(sig, frame):
    global loop_running
    print('You pressed Ctrl+C!')
    loop_running = False

signal.signal(signal.SIGINT, sigint_handler)

asyncio.run(main())
