@echo off

nasm -f bin boot.asm -o boot.bin
nasm -f bin kernel.asm -o kernel.bin

copy /b boot.bin + kernel.bin forkos.img

qemu-system-x86_64 -fda forkos.img