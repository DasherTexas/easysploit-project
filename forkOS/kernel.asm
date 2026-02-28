[BITS 32]
[ORG 0x1000]

VIDEO equ 0xB8000
COLOR equ 0x3F
SPACE equ 0x3020

cursor_x db 0
cursor_y db 3

start:

mov ax, 0x10
mov ds, ax
mov es, ax
mov ss, ax

call clear
call ui
call prompt

main:
call get_key
cmp al, 0
je main

cmp al, 13
je enter

cmp al, 8
je backspace

call putc
jmp main

; =====================
clear:
mov edi, VIDEO
mov ecx, 80*25
mov ax, SPACE
rep stosw
ret

ui:
mov edi, VIDEO
mov esi, topbar
call print

mov edi, VIDEO+160
mov esi, title
call print
ret

prompt:
mov byte [cursor_x], 0
mov esi, text_prompt
call print_line
ret

; =====================
print_line:
call set_cursor
call print
ret

set_cursor:
movzx eax, byte [cursor_y]
imul eax, 160
add eax, VIDEO

movzx ebx, byte [cursor_x]
shl ebx, 1

mov edi, eax
add edi, ebx
ret

print:
lodsb
or al, al
jz .done
mov ah, COLOR
stosw
inc byte [cursor_x]
jmp print
.done:
ret

putc:
push eax
call set_cursor
pop eax
mov ah, COLOR
stosw
inc byte [cursor_x]
ret

backspace:
cmp byte [cursor_x],0
je main
dec byte [cursor_x]
mov al,' '
call putc
dec byte [cursor_x]
jmp main

enter:
inc byte [cursor_y]
call prompt
jmp main

; =====================
; 🔥 REAL KEYBOARD DRIVER
get_key:

.wait:
in al,0x64
test al,1
jz .no_key

in al,0x60

; ignore key release
test al,0x80
jnz .no_key

call scancode_to_ascii
ret

.no_key:
mov al,0
ret

; =====================
scancode_to_ascii:

cmp al,0x1C
je .enter

cmp al,0x0E
je .back

cmp al,0x02
jb .letters
cmp al,0x0A
jbe .numbers

.letters:
cmp al,0x10
jb .none
cmp al,0x19
ja .none
add al,'q'-0x10
ret

.numbers:
add al,'1'-2
ret

.enter:
mov al,13
ret

.back:
mov al,8
ret

.none:
mov al,0
ret

; =====================
topbar db " File Edit View Cmd Win Help ",0
title db "Fork OS - In memory of Terry A. Davis",0
text_prompt db "fos#live> ",0