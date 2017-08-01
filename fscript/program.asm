SYS_EXIT equ 1
SYS_WRITE equ 4
SYS_READ equ 3
STDIN equ 0
STDOUT equ 1
STDERR equ 2

section .data
	msg db "Hello world!", 0x0A
	len equ $ - msg

section .text

global _start

_start:
	push dword len
	push dword msg
	
	call print

	mov eax, SYS_EXIT
	mov ebx, 0
	int 80h


print: ; *char (message), int (len) -> push len, then message
	mov eax, SYS_WRITE
	mov ebx, STDOUT
	pop ecx
	pop edx
	int 80h
	ret


