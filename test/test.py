
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
    
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    async def count_high_cycles(num_cycles):
        high_count = 0
        for _ in range(num_cycles):
            await RisingEdge(dut.clk)
            if dut.uio_out.value.integer:
                high_count += 1
        return high_count

    initial_high_count = await count_high_cycles(10)
    assert initial_high_count == 5, f"Expected initial 50% duty cycle, got {initial_high_count/10:.0%}"

    dut.ui_in.value = BinaryValue("00000001") 
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    increased_high_count = await count_high_cycles(10)
    assert increased_high_count == 6, f"Expected 60% duty cycle, got {increased_high_count/10:.0%}"

    dut.ui_in.value = BinaryValue("00000010") 
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    decreased_high_count = await count_high_cycles(10)
    assert decreased_high_count == 4, f"Expected 40% duty cycle, got {decreased_high_count/10:.0%}"
