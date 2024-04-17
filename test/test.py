
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
    """Test PWM output reacts correctly to increase and decrease inputs by counting high states in uio_out[0]."""
    dut._log.info("Starting test: PWM Duty Cycle Changes")

    # Setup the clock
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the device
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)  # Allow some time after reset

    # Ensure PWM starts in a known state
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 10)  # Allow the PWM to stabilize

    # Test incrementing the duty cycle
    dut.ui_in.value = 0b00000001  # Press the 'increase duty' button
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0b00000000  # Release the button
    await ClockCycles(dut.clk, 20)  # Wait for changes to propagate

    # Count the number of high states over the next 10 cycles
    high_count = 0
    for _ in range(10):
        await RisingEdge(dut.clk)
        if dut.uio_out[0].value:
            high_count += 1

    # Check if the high count matches the expected new duty cycle
    expected_highs = 6  # Assuming duty cycle should now be 60%
    assert high_count == expected_highs, f"Expected {expected_highs} highs, got {high_count} after increase"

    # Test decrementing the duty cycle
    dut.ui_in.value = 0b00000010  # Press the 'decrease duty' button
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0b00000000  # Release the button
    await ClockCycles(dut.clk, 20)  # Wait for changes to propagate

    # Count the number of high states over the next 10 cycles again
    high_count = 0
    for _ in range(10):
        await RisingEdge(dut.clk)
        if dut.uio_out[0].value:
            high_count += 1

    # Check if the high count matches the expected decreased duty cycle
    expected_highs = 5  # Assuming duty cycle should now be back to 50%
    assert high_count == expected_highs, f"Expected {expected_highs} highs, got {high_count} after decrease"

    dut._log.info("All assertions passed. PWM duty cycle changes correctly affect the output.")
