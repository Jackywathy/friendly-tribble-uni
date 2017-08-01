; main.asm
global main

section .text
main:
    push 1234567
    
    add esp, 4

    xor eax, eax
    ret