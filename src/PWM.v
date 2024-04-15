module tt_um_Ziyi_Yuchen
 (
	input  wire [7:0] ui_in,	// Dedicated inputs
	output wire [7:0] uo_out,	// Dedicated outputs
	input  wire [7:0] uio_in,	// IOs: Input path
	output wire [7:0] uio_out,	// IOs: Output path
	output wire [7:0] uio_oe,	// IOs: Enable path (active high: 0=input, 1=output)
	input  wire       ena,
	input  wire       clk,
	input  wire       rst_n
    );

 wire increase_duty = ui_in[0];
 wire decrease_duty = ui_in[1];
 reg PWM_OUT;
 wire slow_clk_enable; // slow clock enable signal for debouncing FFs
 reg[27:0] counter_debounce=28'd0000000000000000000000000000;// counter for creating slow clock enable signals 
 wire tmp1,tmp2,duty_inc;// temporary flip-flop signals for debouncing the increasing button
 wire tmp3,tmp4,duty_dec;// temporary flip-flop signals for debouncing the decreasing button
 reg[3:0] counter_PWM=4'b0000;// counter for creating 10Mhz PWM signal
 reg[3:0] DUTY_CYCLE=4'b0101; // initial duty cycle is 50%
  // Debouncing 2 buttons for inc/dec duty cycle 
  // Firstly generate slow clock enable for debouncing flip-flop (4Hz)
 assign uo_out = ui_in + uio_in;
 assign uio_out = {7'b0, PWM_OUT};
 assign uio_oe = 8'b0;
 always @(posedge clk or posedge rst_n) // added reset condition
 begin
   if (!rst_n) // if reset is high
   begin
     counter_debounce <= 28'd0000000000000000000000000000;
     counter_PWM <= 4'b0000;
     DUTY_CYCLE <= 4'b0101;
   end
   else
   begin
     counter_debounce <= counter_debounce + 28'd0000000000000000000000000001;
     if(counter_debounce>=28'd0000000000000000000000000001) 
      counter_debounce <= 4'b0000;
   end
 end

 assign slow_clk_enable = counter_debounce == 1 ?1:0;

 DFF_PWM PWM_DFF1(clk,slow_clk_enable,increase_duty,tmp1);
 DFF_PWM PWM_DFF2(clk,slow_clk_enable,tmp1, tmp2); 
 assign duty_inc =  tmp1 & (~ tmp2) & slow_clk_enable;

 DFF_PWM PWM_DFF3(clk,slow_clk_enable,decrease_duty, tmp3);
 DFF_PWM PWM_DFF4(clk,slow_clk_enable,tmp3, tmp4); 
 assign duty_dec =  tmp3 & (~ tmp4) & slow_clk_enable;

 always @(posedge clk or posedge rst_n) // added reset condition
 begin
   if (!rst_n) // if reset is high
     DUTY_CYCLE <= 4'b0101;
   else
   begin
     if(duty_inc==1 && DUTY_CYCLE <= 4'b1001) 
      DUTY_CYCLE <= DUTY_CYCLE + 4'b0001;// increase duty cycle by 10%
	   else if(duty_dec==1 && DUTY_CYCLE>=4'b0001) 
      DUTY_CYCLE <= DUTY_CYCLE - 4'b0001;//decrease duty cycle by 10%
   end
 end 

 always @(posedge clk)
 begin
   if (!rst_n)
     counter_PWM <= 4'b0000;
   else if (counter_PWM >= 9)
     counter_PWM <= 4'b0000;
   else
     counter_PWM <= counter_PWM + 4'b0001;
 end


 assign PWM_OUT = counter_PWM < DUTY_CYCLE ? 1:0;
endmodule

module DFF_PWM(clk,en,D,Q);
input clk,en,D;
output reg Q;
always @(posedge clk)
begin 
 if(en==1) // slow clock enable signal 
  Q <= D;
end 
endmodule

