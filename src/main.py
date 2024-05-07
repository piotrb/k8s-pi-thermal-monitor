import asyncio
import signal
import os
import aiofiles
import aiofiles.base

from simple_pid import PID
from gpiozero import PWMOutputDevice

THERMAL_ZONE = os.environ.get("THERMAL_ZONE", "/sys/class/thermal/thermal_zone0/temp")
SETPOINT = float(os.environ.get("SETPOINT", "40"))

GPIO_PWN_PIN = int(os.environ.get("GPIO_PWN_PIN", "3"))
GPIO_TAC_PIN = int(os.environ.get("GPIO_TAC_PIN", "2"))

async def get_system_temp():
  async with aiofiles.open(THERMAL_ZONE) as f:
    rawTemp = await f.read()
    return float(rawTemp) / 1000

loop_running = True

async def main():
    print("Initializing PWM")
    pwm = PWMOutputDevice(pin=GPIO_PWN_PIN, frequency=25000)
    print("Setting PWM to 0")
    pwm.value = 0.0

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

def sig_handler(sig, frame):
    global loop_running
    print(f'Got signal: {sig}. Stopping loop.')
    loop_running = False

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

asyncio.run(main())
