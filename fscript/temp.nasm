extern printf
extern exit
section .data
	numFmt: db "%d", 10, 0
	strFmt: db "%s", 10, 0
	print0: db "hello", 0
section .bss
section .text
	 global main
main:
	;Initalize variables

	push print0
	push strFmt
	call printf
	pop eax
	push 0
	call exit
