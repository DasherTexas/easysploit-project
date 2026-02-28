[ORG 0x7C00]
[BITS 16]

KERNEL_OFFSET equ 0x1000

start:
    mov [BOOT_DRIVE], dl

    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

; load kernel (10 sectors)
    mov ah, 0x02
    mov al, 10
    mov ch, 0
    mov cl, 2
    mov dh, 0
    mov dl, [BOOT_DRIVE]
    mov bx, KERNEL_OFFSET
    int 0x13
    jc disk_error

; enter protected mode
    cli
    lgdt [gdt_descriptor]

    mov eax, cr0
    or eax, 1
    mov cr0, eax

    jmp CODE_SEG:protected_mode

disk_error:
    mov si, err
    call print
    jmp $

print:
    mov ah, 0x0E
.next:
    lodsb
    or al, al
    jz .done
    int 0x10
    jmp .next
.done:
    ret

err db "Disk error",0
BOOT_DRIVE db 0

; ---------------- GDT ----------------

gdt_start:
dq 0
dq 0x00CF9A000000FFFF
dq 0x00CF92000000FFFF
gdt_end:

gdt_descriptor:
dw gdt_end - gdt_start - 1
dd gdt_start

CODE_SEG equ 0x08
DATA_SEG equ 0x10

[BITS 32]
protected_mode:
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov esp, 0x90000

    jmp KERNEL_OFFSET

times 510-($-$$) db 0
dw 0xAA55