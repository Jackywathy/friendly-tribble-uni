SYS_EXIT equ 1
SYS_WRITE equ 4
SYS_READ equ 3


STDIN equ 0
STDOUT equ 1
STDERR equ 2





section .data
   msg1 db "Enter a digit ", 0xA,0xD 
   len1 equ $- msg1 

   msg2 db "Please enter a second digit", 0xA,0xD 
   len2 equ $- msg2 

   msg3 db "The sum is: "
   len3 equ $- msg3


section .bss
   num1 resb 2
   num2 resb 2
   res resb 1
   ; reserve 2 bytes
section .text
   global _start

_start:

   ; print a ask msg
   mov eax, SYS_WRITE
   mov ebx, STDOUT
   mov ecx, msg1
   mov edx, len1
   int 0x80

   ; ask for a msg
   mov eax, SYS_READ
   mov ebx, STDIN
   mov ecx, num1
   mov edx, 2
   int 0x80


   ; print a ask msg
   mov eax, SYS_WRITE
   mov ebx, STDOUT
   mov ecx, msg2
   mov edx, len2
   int 0x80

   ; ask for a msg
   mov eax, SYS_READ
   mov ebx, STDIN
   mov ecx, num2
   mov edx, 2
   int 0x80

   ; print sumLen
   mov eax, SYS_WRITE
   mov ebx, STDOUT
   mov ecx, msg3
   mov edx, len3
   int 0x80 


   mov eax, [num1]
   sub eax, '0'
   
   mov ebx, [num2]
   sub ebx, '0'

   ; add eax and ebx
   add eax, ebx
   ; add '0' to to convert the sum from decimal to ASCII
   add eax, '0'

   ; storing the sum in memory location res
   mov [res], eax

   ; print the sum 
   mov eax, SYS_WRITE        
   mov ebx, STDOUT
   mov ecx, res         
   mov edx, 1        
   int 0x80

   
   ;mov eax, SYS_EXIT   
   ;xor ebx, ebx 
   ;int 0x80