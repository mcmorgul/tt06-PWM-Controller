module tb_PWM_Generator_Verilog;

 reg clk;
 reg increase_duty;
 reg decrease_duty;
 reg reset; // added reset signal
 wire PWM_OUT;

 PWM_Generator_Verilog PWM_Generator_Unit(
	.clk(clk),
	.increase_duty(increase_duty),
	.decrease_duty(decrease_duty),
	.reset(reset), // added reset signal
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