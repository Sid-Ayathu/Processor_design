#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "	
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t2
move $s7,$zero	#i = 0
loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	addi $t2,$t2,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t2,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
bubblesort: addi $s1,$0,0 #$s1=0
	    addi $s2,$t1,0 #s2=n where n is the number of numbers

copy: beq $s1,$s2,sort #copying all the entered numbers to the memory assigned to the output
      sll $t4,$s1,2
      add $s4,$t4,$t2
      add $s5,$t4,$t3
      lw $s3,0($s4)
      sw $s3,0($s5)
      addi $s1,$s1,1
      j copy
	
sort: addi $s1,$0,0 #initialising outer loop counter (say i)
      addi $s2,$t1,-1 #s2=n-1 
      addi $s1,$s1,-1 

outer_loop: addi $s1,$s1,1 #incrementing i
	    beq $s1,$s2,escape #checks if (i< n-1)
	    addi $s3,$0,0 #initialising inner loop counter (say j)
	    sub $s4,$s2,$s1 #$s4=n-1-i
	    addi $s3,$s3,-1
	    
inner_loop: addi $s3,$s3,1 #incrementing j
	    beq $s3,$s4,outer_loop #checks if (j < n-1-i)
	    
	    sll $t4,$s3,2 #$t4=4*$s3
       	    add $t5,$t4,$t3 #t5=(4*$s3)+$t3
       	    
       	    addi $t6,$t4,4 #t6=$t4+4
       	    add $t7,$t6,$t3 #t7=($t4+4)+$t3
       	    
       	    lw $s5,0($t5) #A[j]=M[(4*$s3)+$t3]
       	    lw $s6,0($t7) #A[j+1]=M[($t4+4)+$t3]

	    sub $t8,$s5,$s6
       	    bgtz $t8,inner_loop #swapping the values if A[j] < A[j+1]
       	    
       	    addi $s7,$s5,0
       	    sw $s6,0($t5)
       	    sw $s7,0($t7)
       	    j inner_loop

escape:
#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
#end
end:  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
