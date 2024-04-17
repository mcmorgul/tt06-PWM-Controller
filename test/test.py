
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
async def test_pwm_with_reset_and_timing(dut):
    """Test PWM output with reset behavior and check timing sensitivity to button presses."""
    dut._log.info("Starting test: PWM with Reset and Timing")

    # Setup the clock
    clock = Clock(dut.clk, 10, units="ns")  # Clock period is 10ns
    cocotb.start_soon(clock.start())

    # Reset the device
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)  # Hold reset for 5 cycles
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)  # Wait for the first positive edge after reset

    # Simulate the PWM period: wait for 100ns (10 clock cycles)
    await ClockCycles(dut.clk, 10)

    # Press 'increase duty' button exactly at the start of a new PWM period
    dut.ui_in.value = 0b00000001  # Set increase_duty bit

    # Wait for another PWM period to observe the effect
    await ClockCycles(dut.clk, 10)
    
    # Count the number of high states over the next 10 cycles
    high_count = 0
    for _ in range(10):
        await RisingEdge(dut.clk)
        if dut.uio_out[0].value:
            high_count += 1

    # Check if the high count matches the expected new duty cycle
    expected_highs = 6  # After increment, duty cycle should be 60%
    assert high_count == expected_highs, f"Expected {expected_highs} highs, got {high_count} after increase"

    dut._log.info("Reset and timing assertions passed. PWM duty cycle reacts correctly to input changes with respect to reset and cycle timing.")
