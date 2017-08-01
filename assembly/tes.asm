SYS_EXIT equ 1
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1


global _start

section .data
   helloMsg db 'Helloasdf!', 0x0A
   length equ $ - helloMsg 


_start:
   mov eax, SYS_WRITE
   mov ebx, STDOUT
   mov ecx, helloMsg
   mov edx, length
   int 0x80


   mov eax, SYS_EXIT
   mov ebx, 0
   int 0x80
