![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

#  A Low-Cost Pulse Width Modulation (PWM) Controller

### Authors: Ziyi Zhao, Yuchen Ma

## Description

PWM controllers are fundamental building blocks in digital systems. It is crucial for digital designers and embedded system engineers to understand the PWM and practical experience in designing and implementing a PWM controller enhances skills in digital design and ASIC development.

## How it works

The PWM generates a 10 MHz PWM signal whose duty cycle can be adjusted using two buttons.
Uses a slow clock enable signal and a series of D flip-flops to stabilize the button inputs. 
The debounced signals then control the increase or decrease of the PWM duty cycle.
The PWM duty cycle can be increased or decreased in steps, constrained between 10% and 90%.

## How to test

Change the inputs ui_in to simulate button presses and check if the PWM duty cycle increases or decreases as expected.

## Verilog File
src/PWM.v





