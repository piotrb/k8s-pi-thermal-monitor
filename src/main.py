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

Kp = float(os.environ.get("PID_KP", "-1"))
Ki = float(os.environ.get("PID_KI", "0.1"))
Kd = float(os.environ.get("PID_KD", "0.05"))

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
    print("Initializing PWM")
    pwm = PWMOutputDevice(pin=GPIO_PWN_PIN, frequency=25000)

    print("Setting PWM to 0")
    pwm.value = 0.0

    print(f"Starting PID, setpoint={setpoint}")
    pid = PID(Kp, Ki, Kd, setpoint=setpoint)
    pid.output_limits = (0, 100)

    while loop_running:
        temp = await get_system_temp()
        v = pid(temp)
        print(f"temp: {temp}/{setpoint} v: {v}")
        pwm.value = v/100.0
        await asyncio.sleep(1)

def sig_handler(sig, frame):
    global loop_running
    print(f'Got signal: {sig}. Stopping loop.')
    loop_running = False

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)

asyncio.run(main())
