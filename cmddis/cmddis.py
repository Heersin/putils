#!/usr/bin/env python

import argparse
import capstone

# 定义架构选项
ARCH_X86 = 1
ARCH_ARM = 2

# 定义指令格式
FORMAT_INTEL = 1
FORMAT_ATT = 2

def disassemble(code, arch, format):
    """使用Capstone库反汇编机器码"""
    # 创建Capstone反汇编器
    if arch == ARCH_X86:
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    elif arch == ARCH_ARM:
        md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
    else:
        raise ValueError("Unsupported architecture")

    # 设置指令格式
    if format == FORMAT_INTEL:
        md.syntax = capstone.CS_OPT_SYNTAX_INTEL
    elif format == FORMAT_ATT:
        md.syntax = capstone.CS_OPT_SYNTAX_ATT
    else:
        raise ValueError("Unsupported format")

    # 反汇编机器码
    disassembled = []
    for i in md.disasm(code, 0):
        disassembled.append(i.mnemonic + " " + i.op_str)

    # 返回反
    # 返回反汇编结果
    return "\n".join(disassembled)

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--arch", choices=["x86", "arm"], default="x86", help="specify the architecture")
    parser.add_argument("-f", "--format", choices=["intel", "att"], default="intel", help="specify the format")
    parser.add_argument("filename", help="the file containing the binary code")
    args = parser.parse_args()

    # 根据指定的架构选项设置参数
    if args.arch == "x86":
        arch = ARCH_X86
    elif args.arch == "arm":
        arch = ARCH_ARM

    if args.format == "intel":
        format = FORMAT_INTEL
    elif args.format == "att":
        format = FORMAT_ATT

    # 读取机器码
    with open(args.filename, "rb") as f:
        code = f.read()

    # 使用Capstone库进行反汇编
    disassembled = disassemble(code, arch, format)

    # 输出结果
    print(disassembled)

if __name__ == "__main__":
    main()

