extern printf
extern exit


section .data
	msg: db "Hello, world!", 0
	fmt: db "eax=%d, var1=%d", 10, 0 ; The printf format, "\n", '0'
	fmt2: db "string=%s", 10, 0;

section .bss
	var1: resb 4
	var2: resb 4



section .text
	global main

main:
	mov eax, 300
	mov ebx, 200

	mov [var2], dword 123

	mov [var1], dword 100


	mov eax, [var1]
	add eax, -1023490123

	mov [var1], eax	sc

	; make new stack from - push last paramenter first
	; fmt, int, int
	push dword [var1]
	push eax
	push fmt
	; 
	call printf
	; pop return val
	pop eax

	;make new sstack from -
	; fmt, string
	push msg
	push fmt2
	; call print
	call printf
	; pop return val
	pop eax

	mov eax, dword 9999




	push 0
	call exit
