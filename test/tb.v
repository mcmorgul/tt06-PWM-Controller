`default_nettype none `timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a VCD file. You can view it with gtkwave.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [7:0] ui_in;
  reg [7:0] uio_in;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  reg increase_duty;
  reg decrease_duty;
  wire PWM_OUT;

  // Replace tt_um_factory_test with your module name:
  tt_um_Ziyi_Yuchen user_project (

      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(1'b1),
      .VGND(1'b0),
`endif

      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n),     // not reset

      .increase_duty(increase_duty),
	   .decrease_duty(decrease_duty),
	   .PWM_OUT(PWM_OUT)
     
  );

    initial begin
 clk = 0;
 forever #5 clk = ~clk;
 end
 initial begin
  increase_duty = 0;
  decrease_duty = 0;
  reset = 0; // initialize reset to low
  #100;
	increase_duty = 1;
  #100;
	increase_duty = 0;
  #100;
	increase_duty = 1; 
  #100;
	increase_duty = 0;
  #100;
	increase_duty = 1;
  #100;
	increase_duty = 0;

  #100;
	decrease_duty = 1;
  #100;
	decrease_duty = 0;
  #100;
	decrease_duty = 1;
  #100;
	decrease_duty = 0;
  #100;
	decrease_duty = 1;
  #100;
	decrease_duty = 0;

//Debouncing test
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;
  #5;
	increase_duty = 1;
  #5;
	increase_duty = 0;

//Keep pressing test

  #100;
	increase_duty = 1;
  #900;
	increase_duty = 0;

  #100;
  reset = 1; // set reset high to reset the program
  #100;
  reset = 0; // set reset low to allow the program to run normally
  end


endmodule
