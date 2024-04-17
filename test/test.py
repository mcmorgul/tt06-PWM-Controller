
# SPDX-FileCopyrightText: © 2023 Uri Shaked <uri@tinytapeout.com>
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_loopback(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1

    # ui_in[0] == 0: Copy bidirectional pins to outputs
    dut.ui_in.value = 0b0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    for i in range(256):
        dut.uio_in.value = i
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i


@cocotb.test()
async def test_counter(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # ui_in[0] == 1: bidirectional outputs enabled, put a counter on both output and bidirectional pins
    dut.ui_in.value = 0b1
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)
"""
    dut._log.info("Testing counter")
    for i in range(256):
        assert dut.uo_out.value == dut.uio_out.value
        assert dut.uo_out.value == i
        await ClockCycles(dut.clk, 1)
"""

@cocotb.test()
async def test_pwm_duty_cycle_changes(dut):
    """Test PWM output reacts correctly to increase and decrease inputs."""
    dut._log.info("Starting test: PWM Duty Cycle Changes")
    
    # Generate a clock with a period of 10ns (100MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the device
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # Initial conditions
    dut.ui_in.value = 0b00000000  # Both increase and decrease buttons are not pressed

    # Ensure PWM output starts at the initial condition
    await RisingEdge(dut.clk)
    initial_duty_cycle = int(dut.DUTY_CYCLE.value)
    assert initial_duty_cycle == 5, f"Expected initial duty cycle to be 5, got {initial_duty_cycle}"

    # Press the 'increase duty' button
    dut.ui_in.value = 0b00000001  # Set increase_duty bit
    await ClockCycles(dut.clk, 2)  # Wait for a couple of clock cycles
    dut.ui_in.value = 0b00000000  # Release the button
    await ClockCycles(dut.clk, 10) # Wait for the PWM output to potentially update

    # Check if the duty cycle has increased
    increased_duty_cycle = int(dut.DUTY_CYCLE.value)
    assert increased_duty_cycle == 6, f"Expected duty cycle to increase to 6, got {increased_duty_cycle}"

    # Press the 'decrease duty' button
    dut.ui_in.value = 0b00000010  # Set decrease_duty bit
    await ClockCycles(dut.clk, 2)  # Wait for a couple of clock cycles
    dut.ui_in.value = 0b00000000  # Release the button
    await ClockCycles(dut.clk, 10) # Wait for the PWM output to potentially update

    # Check if the duty cycle has decreased
    decreased_duty_cycle = int(dut.DUTY_CYCLE.value)
    assert decreased_duty_cycle == 5, f"Expected duty cycle to decrease to 5, got {decreased_duty_cycle}"

    dut._log.info("All assertions passed. Duty cycle changes as expected.")
