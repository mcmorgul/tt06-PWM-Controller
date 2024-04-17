`default_nettype none 
`timescale 1ns / 1ps

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
   reg [7:0] ui_in=0;
   reg [7:0] uio_in=0;
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

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
     .rst_n  (rst_n)     // not reset
  );
   initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  // Input stimuli
 initial begin
    ena = 1;
    ui_in[0] = 0;
    ui_in[1] = 0;
    forever begin
        #100 ui_in[0] = 1;  // After 100 cycles, set ui_in[0] to 1
        #100 ui_in[0] = 0;  // After another 100 cycles, set ui_in[0] to 0
        #100 ui_in[1] = 1;  // After another 100 cycles, set ui_in[1] to 1
        #100 ui_in[1] = 0;  // After another 100 cycles, set ui_in[1] to 0
    end
end

endmodule
